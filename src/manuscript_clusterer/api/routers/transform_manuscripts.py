"""Router to get the transformed manuscripts.
"""
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query


from manuscript_clusterer.api.routers import db_manipulator
from manuscript_clusterer.engine import profile_readings
from . import STUDIED_CHAPTER


router = APIRouter(prefix="/manuscripts/transform",
                   tags=["manuscripts_transform"])


@router.get("/projections/")
async def get_projection_manuscripts(manuscript_lists: Annotated[list[str] | None, Query()] = None,
                                     all_manuscripts: Annotated[bool, Query(
                                     )] = False,
                                     experimental: Annotated[bool, Query()] = False):
    """Get the coordinates of the manuscripts using MCA applied to their profile.
    """
    try:
        if experimental:
            _, manuscripts_projected = db_manipulator.get_content_projected(manuscripts_list=manuscript_lists,
                                                                            all_manuscripts=all_manuscripts,
                                                                            chapter=STUDIED_CHAPTER)
        else:
            _, manuscripts_projected = db_manipulator.get_manuscripts_projected(manuscripts_list=manuscript_lists,
                                                                                all_manuscripts=all_manuscripts)
        profiles_clustered = db_manipulator.get_profile_clustered(manuscripts_list=manuscript_lists,
                                                                    all_manuscripts=all_manuscripts)
        content_clustered = db_manipulator.get_content_clustered(manuscripts_list=manuscript_lists,
                                                                    all_manuscripts=all_manuscripts,
                                                                    chapter=STUDIED_CHAPTER)
        final_data = {}
        for manuscript_id in manuscripts_projected.keys():
            final_data[manuscript_id] = {
                'coordinates': manuscripts_projected[manuscript_id],
                'clustered_profile': profiles_clustered.get(manuscript_id, None),
                'clustered_content': content_clustered.get(manuscript_id, None),
                **db_manipulator.get_manuscript_info(manuscript_id)[0]
            }
        final_values = list(final_data.values())
        return {
            "labels": list(final_data.keys()),
            "x": [values["coordinates"][0] for values in final_values],
            "y": [values["coordinates"][1] for values in final_values],
            "z": [values["coordinates"][2] for values in final_values],
            "clustered-profile": [label["clustered_profile"] for label in final_values],
            "clustered-content": [label["clustered_content"] for label in final_values],
            "aland-cat": [label["aland-cat"] for label in final_values],
            "wisse": [label["wisse"] for label in final_values],
            "von-soden": [label["von-soden"] for label in final_values],
            "text-type": [label["text-type"] for label in final_values],
            "date": [label["date"] for label in final_values]
        }
    except ValueError as e:
        raise HTTPException(status_code=500,
                            detail="Unable to compute the projection") from e


@router.get("/profiles/")
async def get_manuscripts_profiles(manuscript_1: Annotated[str, Query()],
                                   manuscript_2: Annotated[str, Query()],
                                   format_heatmap: Annotated[bool, Query()] = False):
    """Get the profile of two manuscripts.
    """
    try:
        profiles = db_manipulator.get_manuscripts_profiles(manuscripts_list=[manuscript_1, manuscript_2])
        profiles_dict = {profile["id"]: profile["profile"] for profile in profiles}
        if format_heatmap:
            return {
                "z": [list(manuscript_profile.values()) for manuscript_profile in profiles_dict.values()],
                "x": list(profiles_dict[manuscript_1].keys()),
                "y": list(profiles_dict.keys())
            }
    except ValueError as e:
        raise HTTPException(status_code=500,
                            detail="Unable to cluster the profiles") from e


@router.get("/readings/")
async def get_manuscripts_clusters_readings(manuscript_lists: Annotated[list[str] | None, Query()] = None,
                                            all_manuscripts: Annotated[bool, Query()] = False):
    """Cluster the profiles of the manuscripts.
    """
    try:
        return db_manipulator.get_readings_clustered(manuscripts_list=manuscript_lists,
                                                     all_manuscripts=all_manuscripts)
    except ValueError as e:
        raise HTTPException(status_code=500,
                            detail="Unable to cluster the readings") from e


@router.get("/content/")
async def get_manuscripts_clusters_content(manuscript_lists: Annotated[list[str] | None, Query()] = None,
                                           all_manuscripts: Annotated[bool, Query(
                                           )] = False,
                                           chapter: Annotated[str, Query()] = STUDIED_CHAPTER):
    """Cluster the content of the manuscripts.
    """
    try:
        return db_manipulator.get_content_clustered(manuscripts_list=manuscript_lists,
                                                    all_manuscripts=all_manuscripts,
                                                    chapter=chapter)
    except ValueError as e:
        raise HTTPException(status_code=500,
                            detail="Unable to cluster the content") from e


@router.get("/distances/")
async def get_manuscripts_distances(manuscript_lists: Annotated[list[str] | None, Query()] = None,
                                    all_manuscripts: Annotated[bool, Query(
                                    )] = False,
                                    chapter: Annotated[str,
                                                       Query()] = STUDIED_CHAPTER,
                                    distance_scheme: Annotated[str, Query(
                                    )] = "wisse",
                                    format_heatmap: Annotated[bool, Query()] = False):
    """Get the distances between the manuscripts using different schemes.
    """
    try:
        if distance_scheme == "wisse":
            distances = db_manipulator.get_profile_distance(manuscripts_list=manuscript_lists,
                                                            all_manuscripts=all_manuscripts,
                                                            chapter=chapter)
            if format_heatmap:
                return {
                    "z": [list(distance_value.values()) for distance_value in distances.values()],
                    "x": list(distances.keys()),
                    "y": list(distances.keys())
                }
            else:
                return distances
        elif distance_scheme == "all":
            manuscript_keys, distances = db_manipulator.get_content_distances(manuscripts_list=manuscript_lists,
                                                             all_manuscripts=all_manuscripts,
                                                             chapter=chapter)
            if format_heatmap:
                return {
                    "z": distances.tolist(),
                    "x": list(manuscript_keys),
                    "y": list(manuscript_keys)
                }
            else:
                return distances
        # return db_manipulator.get_content_distances(manuscripts_list=manuscript_lists,
        #                                             all_manuscripts=all_manuscripts,
        #                                             chapter=chapter,
        #                                             distance_scheme=distance_scheme)

    except ValueError as e:
        raise HTTPException(status_code=500,
                            detail="Unable to compute the distances") from e


@router.get("/versedistances/")
async def get_manuscripts_verse_distances(manuscript_1: Annotated[str, Query()],
                                          manuscript_2: Annotated[str, Query()],
                                          chapter: Annotated[str, Query(
                                          )] = STUDIED_CHAPTER,
                                          format_heatmap: Annotated[bool, Query()] = False):
    """Get the distances between the manuscripts using different schemes.
    """
    try:
        verses, distances = db_manipulator.get_verse_distance_content(manuscript_1=manuscript_1,
                                                       manuscript_2=manuscript_2,
                                                       chapter=chapter)
        if format_heatmap:
            return {
                "z": distances.tolist(),
                "x": [""],
                "y": list(verses)
            }
        else:
            return distances
        
    except ValueError as e:
        raise HTTPException(status_code=500,
                            detail="Unable to compute the distances") from e
    
@router.get("/homogeneity/")
async def get_classification_homogeneity():
    """
    Get the homogeneity between the classifications.
    """
    try:
        profiles_clustered = db_manipulator.get_profile_clustered(all_manuscripts=True)
        content_clustered = db_manipulator.get_content_clustered(all_manuscripts=True,
                                                                    chapter=STUDIED_CHAPTER)

        # Sort the data
        final_data = {}
        for manuscript_id in profiles_clustered.keys():
            final_data[manuscript_id] = {
                'clustered_profile': profiles_clustered.get(manuscript_id, None),
                'clustered_content': content_clustered.get(manuscript_id, None),
                **db_manipulator.get_manuscript_info(manuscript_id)[0]
            }
        final_values = list(final_data.values())
        clustered_profile = [label["clustered_profile"] for label in final_values]
        clustered_content = [label["clustered_content"] for label in final_values]
        aland_cat = [label["aland-cat"] for label in final_values]
        text_type = [label["text-type"] for label in final_values]
        wisse_cat = [label["wisse"] for label in final_values]
        von_soden_cat = [label["von-soden"] for label in final_values]

        return {
            "Score profile-content": db_manipulator.measure_cluster_quality(clustered_profile, clustered_content),
            "Score profile-aland": db_manipulator.measure_cluster_quality(clustered_profile, aland_cat),
            "Score profile-wisse": db_manipulator.measure_cluster_quality(clustered_profile, wisse_cat),
            "Score profile-VS": db_manipulator.measure_cluster_quality(clustered_profile, von_soden_cat),
            "Score profile-type": db_manipulator.measure_cluster_quality(clustered_profile, text_type),
            "Score content-aland": db_manipulator.measure_cluster_quality(clustered_content, aland_cat),
            "Score content-type": db_manipulator.measure_cluster_quality(clustered_content, text_type),
            "Score content-wisse": db_manipulator.measure_cluster_quality(clustered_content, wisse_cat),
            "Score content-VS": db_manipulator.measure_cluster_quality(clustered_content, von_soden_cat)
        }
    except ValueError as e:
        raise HTTPException(status_code=500,
                            detail="Unable to compute the projection") from e

@router.get("/wissereadings/")
def get_wisse_readings():
    """Output as HTML the dataset containing the Wisse readings.
    """
    return profile_readings[profile_readings.chapter == int(STUDIED_CHAPTER)][["verse", "reading", "alternative_reading"]].to_html()