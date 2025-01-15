"""Router for manipulation of several manuscripts.
"""

from fastapi import APIRouter, HTTPException, Query, Response
from bs4 import BeautifulSoup
from manuscript_clusterer.api.routers import db_manipulator
from collatex import Collation, collate
from collatex.core_classes import create_table_visualization
from . import STUDIED_CHAPTER

router = APIRouter(prefix="/manuscripts", tags=["manuscripts"])


@router.get("/")
async def get_manuscripts():
    """Get all manuscripts from the database.
    """
    manuscripts = db_manipulator.get_manuscripts()
    if not manuscripts:
        raise HTTPException(status_code=404, detail="No manuscripts found")
    return [manuscript["id"] for manuscript in manuscripts]


@router.get("/profiles/")
async def get_manuscripts_profiles(format_heatmap: bool = Query(False)):
    """Get the profiles of the manuscripts.
    """
    profiles = db_manipulator.get_all_manuscripts_profiles()
    if not profiles:
        raise HTTPException(status_code=404, detail="No profiles found")
    profiles_dict = {profile["id"]: profile["profile"] for profile in profiles}
    if not format_heatmap:
        return profiles_dict
    else:
        return {
            "z": [list(manuscript_profile.values()) for manuscript_profile in profiles_dict.values()],
            "x": list(range(0, len(list(profiles_dict.values())[0]))),
            "y": list(profiles_dict.keys())
        } 

@router.get("/readings/")
async def get_manuscripts_readings():
    """Get the profiles of the manuscripts.
    """
    readings = db_manipulator.get_all_manuscripts_readings()
    if not readings:
        raise HTTPException(status_code=404, detail="No profiles found")
    return {profile["id"]: profile["readings"] for profile in readings}


@router.get("/content/")
async def get_manuscripts_content():
    """Get the content of the manuscripts.
    """
    content = db_manipulator.get_all_manuscripts_content()
    if not content:
        raise HTTPException(status_code=404, detail="No content found")
    return {profile["id"]: profile["content"] for profile in content}


@router.get("/collation/")
async def get_verses_collation(manuscript_1: str,
                                manuscript_2: str,
                                verse: str,
                                chapter: str = Query(STUDIED_CHAPTER)):
    """Get the distances between the manuscripts.
    """
    verse_1 = db_manipulator.get_manuscript_content(
        manuscript_id=manuscript_1)["content"][chapter][verse]
    verse_2 = db_manipulator.get_manuscript_content(
        manuscript_id=manuscript_2)["content"][chapter][verse]
    if not verse_1 or not verse_2:
        raise HTTPException(
            status_code=404, detail="Manuscript content not found")
    collation = Collation()
    collation.add_plain_witness(manuscript_1, verse_1)
    collation.add_plain_witness(manuscript_2, verse_2)
    html_string = create_table_visualization(collate(collation, output="table", segmentation=True, near_match=False)).get_html_string(formatting=True)

    # Format the HTML string to output borders and padding
    soup = BeautifulSoup(html_string, "html.parser")
    for cell in soup.find_all("td"):
        cell.attrs.update({"style": "border: 1px solid black; padding: 5px;"})
    return soup.prettify()
