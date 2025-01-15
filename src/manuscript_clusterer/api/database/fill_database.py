"""Download the data from the NTVMR and fill the Mongo Database with it.
"""

import unicodedata
from xml.etree import ElementTree
import httpx
import time
from loguru import logger

from manuscript_clusterer.api.database.db_manipulator import ManuscriptDB
from manuscript_clusterer.engine.get_profiles import evaluate_manuscript_profile, evaluate_manuscript_readings
from manuscript_clusterer.engine.utils import expand_nomina_sacra


def parse_chapter(chap_str: str):
    """Parse the chapter number.
    """
    if "incip" in chap_str.lower():
        return "Incipit"
    return chap_str.split("K")[1]


def parse_verse(verse_str: str):
    """Parse the verse number.
    """
    return verse_str.split("V")[1]


def parse_manuscript(response_str: str,
                     book_id: str = "B20",
                     variant: str = "corr",
                     use_reconstructed: bool = True):
    """Given the a NTVMR request response, parse the manuscript into
    a Python dictioinary.
    """
    et = ElementTree.fromstring(response_str.replace(
        '<lb break="no"/>', "").replace('<lb/>', ''))
    title = et.find(".//{http://www.tei-c.org/ns/1.0}title").attrib["n"]
    flat_text = {}

    for elem in et.iter():
        if elem.tag == "{http://www.tei-c.org/ns/1.0}div":
            if elem.attrib["type"] == "book":
                book = elem.attrib["n"]
                if book != book_id:
                    break
            if elem.attrib["type"] == "chapter":
                chapter = parse_chapter(elem.attrib["n"])
                if chapter not in flat_text:
                    flat_text[chapter] = {}
            if elem.attrib["type"] == "incipit":
                chapter = parse_chapter(elem.attrib["n"])
                if chapter not in flat_text:
                    flat_text[chapter] = {}

        if elem.tag == "{http://www.tei-c.org/ns/1.0}ab":
            if elem.attrib.get("n"):
                verse = parse_verse(elem.attrib["n"])
            try:
                verse
            except UnboundLocalError:
                verse = "0"
            if verse not in flat_text[chapter]:
                flat_text[chapter][verse] = ""

            for subelem in list(elem):
                if subelem.tag == "{http://www.tei-c.org/ns/1.0}w":
                    # Nested words structure (nominem sacrum, abbreviation, etc)
                    if not subelem.text:
                        for subsubelem in subelem.iter():
                            if subsubelem.text:
                                flat_text[chapter][verse] += subsubelem.text
                        flat_text[chapter][verse] += " "
                    else:
                        # Get all texts, including abbreviation and unclear texts if
                        # use reconstructed is enabled
                        if not use_reconstructed:
                            flat_text[chapter][verse] += subelem.text + " "
                        else:
                            flat_text[chapter][verse] += ' '.join(
                                subelem.itertext()) + " "
                if subelem.tag == "{http://www.tei-c.org/ns/1.0}app":
                    for subsubelem in subelem.iter():
                        if subsubelem.tag == "{http://www.tei-c.org/ns/1.0}rdg":
                            if subsubelem.attrib["type"] == variant:
                                for subsubsubelem in subsubelem.iter():
                                    if subsubsubelem.tag == "{http://www.tei-c.org/ns/1.0}w":
                                        if subsubsubelem.text:
                                            flat_text[chapter][verse] += subsubsubelem.text + " "
                                        # Check if again a nested structure
                                        else:
                                            for subsubsubsubelem in subsubsubelem.iter():
                                                if subsubsubsubelem.text:
                                                    flat_text[chapter][verse] += subsubsubsubelem.text + " "
                                flat_text[chapter][verse] += " "
    # Expand nomina sacra for all content
    flat_text = {chapter: {verse: expand_nomina_sacra(flat_text[chapter][verse]) for verse in flat_text[chapter]} for chapter in flat_text}
    return title, flat_text


def remove_control_characters(s: str):
    """
    Remove control characters from a string.
    """
    return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C")


def get_manuscripts_id(uncials_range=(1, 326),
                       papyri_range=(1, 135),
                       miniscules_range=(1, 500)):
    """Get the list of manuscripts to retrieve from the NTVMR.
    """
    if uncials_range:
        oncials = [f"2{str(i).zfill(4)}" for i in range(*uncials_range)]
    else:
        oncials = []
    if papyri_range:
        papyrus = [f"1{str(i).zfill(4)}" for i in range(*papyri_range)]
    else:
        papyrus = []
    if miniscules_range:
        miniscules = [f"3{str(i).zfill(4)}" for i in range(*miniscules_range)]
    else:
        miniscules = []
    return oncials + papyrus + miniscules


def generate_manuscript_id(manuscript_type: str, manuscript_number: str):
    """Generate a manuscript ID."""
    if manuscript_type == "papyri":
        return f"1{str(manuscript_number).zfill(4)}"
    elif manuscript_type == "uncials":
        return f"2{str(manuscript_number).zfill(4)}"
    elif manuscript_type == "miniscules":
        return f"3{str(manuscript_number).zfill(4)}"


def retrieve_manuscript_content(manuscript_id: str,
                                tradition_name: str,
                                timer: int = 30):
    """Retrieve the content of a manuscript from the NTVMR.
    """
    base_url = "https://ntvmr.uni-muenster.de/community/vmr/api/transcript/get/"
    request = f"?docID={manuscript_id}&indexContent={
        tradition_name}&format=xml"
    logger.info(f"Submitting request to retrieve manuscript {manuscript_id}")
    response = httpx.get(base_url + request, timeout=60)
    if response.status_code == 200:
        if "No Transcription Available" in response.text:
            logger.info(f"No transcription available for manuscript"
                        f"{manuscript_id}")
            return None
        logger.info(f"Downloaded manuscript {manuscript_id}")
        # Avoid reset by peer errors by sleeping at the end of the request
        time.sleep(timer)
        return remove_control_characters(response.text)
    else:
        logger.error(f"No data available for manuscript {manuscript_id}")
        # Avoid reset by peer errors by sleeping at the end of the request
        time.sleep(timer)
        return None


def get_manuscripts(tradition_name: str,
                    uncials_range=None,
                    papyri_range=None,
                    miniscules_range=None,
                    manuscripts_list=None,
                    timer: int = 30):
    """Retrieve the manuscripts from the NTVMR.
    """
    if not manuscripts_list:
        manuscripts_list = get_manuscripts_id(
            uncials_range=uncials_range,
            papyri_range=papyri_range,
            miniscules_range=miniscules_range)
    responses = []
    ix = 0
    for manuscript in manuscripts_list:
        response = retrieve_manuscript_content(
            manuscript, tradition_name, timer)
        if response:
            responses.append(response)
            ix += 1
    logger.info(f"Retrieved {ix} manuscripts")
    return responses


if __name__ == "__main__":
    import pandas as pd

    db = ManuscriptDB()

    # Setup wanted chapter of luke
    chapter = "10"
    GET_ALL_MANUSCRIPTS = False

    if GET_ALL_MANUSCRIPTS:
        # Define ranges for each manuscript type
        miniscules_chunks = [
            (1, 10), (11, 20), (21, 30), (31, 40), (41, 50),
            (51,
             60), (61, 70), (71, 80), (81, 90), (91, 100),
            (101, 110), (111, 120), (121, 130), (131, 140), (141, 150), (151,
                                                                         160), (161, 170), (171, 180), (181, 190), (191, 200),
            (201, 210), (211, 220), (221, 230), (231, 240), (241, 250), (251,
                                                                         260), (261, 270), (271, 280), (281, 290), (291, 300),
            (301, 310), (311, 320), (321, 330), (331, 340), (341,
                                                             350), (351, 360), (361, 370), (371, 380), (381, 390), (391, 400)
        ]
        papyri_chunks = [
            (1, 10), (11, 20), (21, 30), (31, 40), (41, 50), (51,
                                                              60), (61, 70), (71, 80), (81, 90), (91, 100),
            (101, 110), (111, 120), (121, 130), (131, 140), (141, 150), (151,
                                                                         160), (161, 170), (171, 180), (181, 190), (191, 200),
            (201, 210), (211, 220), (221, 230), (231, 240), (241, 250)]
        uncials_chunks = [
            (1, 10),
            (11, 20), (21, 30), (31, 40), (41, 50), (51,
                                                     60), (61, 70), (71, 80), (81, 90), (91, 100),
            (101, 110), (111, 120), (121, 130), (131, 140), (141, 150), (151,
                                                                         160), (161, 170), (171, 180), (181, 190), (191, 200),
            (201, 210), (211, 220), (221, 230), (231, 240), (241,
                                                             250), (251, 260), (261, 270), (271, 280), (281, 290), (291, 300)
        ]

        # Combine all chunks into a single list for processing
        all_chunks = [
            ("uncials", chunk) for chunk in uncials_chunks
        ] + [("miniscules", chunk) for chunk in miniscules_chunks
             ] + [
            ("papyri", chunk) for chunk in papyri_chunks
        ]
    else:
        manucripts_list = ['20001',
                           '20002',
                           '20003',
                           '20004',
                           '20005',
                           '20019',
                           '20032',
                           '20038',
                           '30001',
                           '30013',
                           '30018',
                           '30022',
                           '30033',
                           '30069',
                           '30079',
                           '30343',
                           '100P4',
                           '10P42']
        
    # Load CSV file with manuscript data
    info_data = pd.read_csv("datasets/classification.csv", index_col=0).fillna("").to_dict(orient="index")

    # Process manuscripts for each chunk
    if GET_ALL_MANUSCRIPTS:
        for manuscript_type, manuscript_range in all_chunks:
                manuscript_content = get_manuscripts(
                    f"Luke{chapter}",
                    **{f"{manuscript_type}_range": manuscript_range},
                    timer=30
                )                
        for manuscript in manuscript_content:
            title, flat_text = parse_manuscript(manuscript, book_id="B03")
            if flat_text.get(chapter):
                db.insert_document(
                    collection_name="manuscripts",
                    document={
                        "id": generate_manuscript_id(manuscript_type, title),
                        "type": manuscript_type,
                        "name": title,
                        "content": flat_text,
                        "profile": evaluate_manuscript_profile(flat_text, [int(chapter)]),
                        "readings": evaluate_manuscript_readings(flat_text, [int(chapter)]),
                        **info_data[title]
                    },
                )
                logger.info(f"Inserted manuscript {title} into the database")
    else:
        manuscript_content = get_manuscripts(
                f"Luke{chapter}",
                manuscripts_list=manucripts_list,
                timer=30
            )
        for id, manuscript in zip(manucripts_list, manuscript_content):
            title, flat_text = parse_manuscript(manuscript, book_id="B03")
            if id.startswith("1"):
                manuscript_type = "papyri"
            elif id.startswith("2"):
                manuscript_type = "uncials"
            elif id.startswith("3"):
                manuscript_type = "miniscules"
            if flat_text.get(chapter):
                db.insert_document(
                    collection_name="manuscripts",
                    document={
                        "id": id,
                        "type": manuscript_type,
                        "name": title,
                        "content": flat_text,
                        "profile": evaluate_manuscript_profile(flat_text,  [int(chapter)]),
                        "readings": evaluate_manuscript_readings(flat_text,  [int(chapter)]),
                        **info_data[id]
                    },
                )
                logger.info(f"Inserted manuscript {title} into the database")