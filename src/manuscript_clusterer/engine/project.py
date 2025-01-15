"""Various functions to perform the clustering of the functions.
"""
import pandas as pd
from umap import UMAP
from manuscript_clusterer.engine.cluster import compute_distance_matrix_text


def perform_projection_profiles(profile: list[dict[str, any]]):
    """Perform a projection given profiles, i.e. binary values for a given manuscript.

    #TODO: think about -1 data!!!
    """
    profile_df = pd.DataFrame(profile).T
    # Remove -1 data
    profile_df = profile_df[~(profile_df == -1).any(axis=1)]
    transformer = UMAP(n_components=3,
                       random_state=42)
    transformed = transformer.fit_transform(profile_df)
    return profile_df.to_dict(orient="index"), pd.DataFrame(transformed, index=profile_df.index).to_dict(orient="index")


def perform_projection_content(content: list[dict[str, any]]):
    """Perform a projection using textual distances between textual content.
    """
    manuscript_keys, distance_matrix = compute_distance_matrix_text(content)
    transformer = UMAP(n_components=3,
                       random_state=42,
                       metric="precomputed")
    transformed = transformer.fit_transform(distance_matrix)
    return distance_matrix, pd.DataFrame(transformed, index=manuscript_keys).to_dict(orient="index")
