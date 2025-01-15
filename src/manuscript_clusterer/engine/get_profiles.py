"""Perform Wisse method for profile classification.
Additionally include the application of a PCA for silhouette reduction.
"""
from pathlib import Path
import re
import pandas as pd
from manuscript_clusterer.engine.utils import expand_nomina_sacra


PROFILE_RULES = pd.read_csv(str(Path(__file__).absolute().parent) + "/data/profile_rules.csv")


def evaluate_manuscript_profile(manuscript: dict[str, any],
                                chapters: list[int],
                                rule: pd.DataFrame = PROFILE_RULES):
    """Evaluate a given manuscript and compute its profile.

    #TODO: this is set to 0 if the alternative is present, otherwise 1
    """
    readings = {}
    # Extract the profile for the given chapter
    subrule = rule[rule.chapter.isin(chapters)]
    for profile in subrule.iterrows():
        try:
            content = expand_nomina_sacra(
                manuscript[str(profile[1]["chapter"])][str(profile[1]["verse"])])
            reading = expand_nomina_sacra(str(profile[1]["reading"]))
            alternative_reading = expand_nomina_sacra(str(profile[1]["alternative_reading"]))
            # Check which one is longer and start with the longer one
            if len(reading) >= len(alternative_reading):
                if re.search(reading, content):
                    readings[f'{profile[1]["chapter"]}:{str(profile[1]["verse"])}:{profile[1]["reading_id"]}'] = 1
                elif ("omit" in reading) and (not re.search(alternative_reading, content)):
                    readings[f'{profile[1]["chapter"]}:{str(profile[1]["verse"])}:{profile[1]["reading_id"]}'] = 1
                else:
                    readings[f'{profile[1]["chapter"]}:{str(profile[1]["verse"])}:{profile[1]["reading_id"]}'] = 0
            else:
                if re.search(alternative_reading, content):
                    readings[f'{profile[1]["chapter"]}:{str(profile[1]["verse"])}:{profile[1]["reading_id"]}'] = 0
                elif ("omit" in reading):
                    readings[f'{profile[1]["chapter"]}:{str(profile[1]["verse"])}:{profile[1]["reading_id"]}'] = 1
                elif re.search(reading, content):
                    readings[f'{profile[1]["chapter"]}:{str(profile[1]["verse"])}:{profile[1]["reading_id"]}'] = 1
                else:
                    readings[f'{profile[1]["chapter"]}:{str(profile[1]["verse"])}:{profile[1]["reading_id"]}'] = 0
        except KeyError:
            readings[f'{profile[1]["chapter"]}:{str(profile[1]["verse"])}:{profile[1]["reading_id"]}'] = -1
    return readings


def evaluate_manuscript_readings(manuscript: dict[str, any],
                                chapters: list[int],
                                rule: pd.DataFrame = PROFILE_RULES):
    """Evaluate the readings value of a given manuscript.
    """
    readings = {}
    # Extract the profile for the given chapter
    subrule = rule[rule.chapter.isin(chapters)]
    for profile in subrule.iterrows():
        try:
            content = expand_nomina_sacra(
                manuscript[str(profile[1]["chapter"])][str(profile[1]["verse"])])
            reading = expand_nomina_sacra(str(profile[1]["reading"]))
            alternative_reading = expand_nomina_sacra(str(profile[1]["alternative_reading"]))
            # Check which one is longer and start with the longer one
            if len(reading) >= len(alternative_reading):
                if re.search(reading, content):
                    readings[f'{profile[1]["chapter"]}:{profile[1]["reading_id"]}'] = reading
                elif ("omit" in reading) and (not re.search(alternative_reading, content)):
                    readings[f'{profile[1]["chapter"]}:{profile[1]["reading_id"]}'] = ""
                elif re.search(alternative_reading, content):
                    readings[f'{profile[1]["chapter"]}:{profile[1]["reading_id"]}'] = alternative_reading
                else:
                    readings[f'{profile[1]["chapter"]}:{profile[1]["reading_id"]}'] = content
            else:
                if re.search(alternative_reading, content):
                    readings[f'{profile[1]["chapter"]}:{profile[1]["reading_id"]}'] = alternative_reading
                elif ("omit" in reading):
                    readings[f'{profile[1]["chapter"]}:{profile[1]["reading_id"]}'] = ""
                elif re.search(reading, content):
                    readings[f'{profile[1]["chapter"]}:{profile[1]["reading_id"]}'] = reading
                else:
                    readings[f'{profile[1]["chapter"]}:{profile[1]["reading_id"]}'] = content
        except KeyError:
            readings[f'{profile[1]["chapter"]}:{profile[1]["reading_id"]}'] = -1

    return readings