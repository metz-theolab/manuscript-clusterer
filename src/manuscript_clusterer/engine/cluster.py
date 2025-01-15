"""Apply clustering to the manuscript data.
"""
from sklearn.base import ClusterMixin
from sklearn.metrics import silhouette_score
import numpy as np
import pandas as pd
from textdistance import jaccard


def cluster_profiles(profiles: dict[str, dict[str, str]],
                     clusterer_class: ClusterMixin,
                     **kwargs):
    """Cluster the manuscript according to their profile.
    """
    profile_df = pd.DataFrame(profiles).T
    best_n_cluster = find_best_n_clusters(clusterer_class, profile_df, **kwargs)
    clusterer = clusterer_class(n_clusters=best_n_cluster, **kwargs)
    clusterer.fit(profile_df)
    return {
        manuscript_id: str(cluster_id) for manuscript_id, cluster_id in
        zip(profile_df.index, clusterer.labels_)
    }


def compute_distance_matrix_text(clustered_content: dict[str, dict[str, str]],
                                 distance_function: callable = jaccard):
    """
    Compute the distance matrix between manuscripts based on their variant readings.
    """
    # Get the manuscript keys
    manuscript_keys = list(clustered_content.keys())
    num_manuscripts = len(manuscript_keys)

    # Initialize a distance matrix with zeros
    distance_matrix = np.zeros((num_manuscripts, num_manuscripts))

    # Iterate over all pairs of manuscripts
    for i, key1 in enumerate(manuscript_keys):
        for j, key2 in enumerate(manuscript_keys):
            if i < j:  # Avoid redundant computations (matrix is symmetric)
                total_distance = 0
                text1 = clustered_content[key1]
                text2 = clustered_content[key2]

                # Compute distances for each verse and sum them
                for verse in set(text1.keys()).union(set(text2.keys())):
                    # Default to empty string if verse is missing
                    reading_text1 = text1.get(verse, "")
                    reading_text2 = text2.get(verse, "")
                    dist = 1 - distance_function(reading_text1, reading_text2)
                    total_distance += dist

                # Fill in the symmetric entries of the distance matrix
                distance_matrix[i, j] = total_distance
                distance_matrix[j, i] = total_distance

    return manuscript_keys, distance_matrix


def compute_distance_matrix_verse_text(verses: dict[str, dict[str, str]],
                                  distance_function: callable = jaccard):
    """
    Compute the distance between manuscripts on a verse level.

    The format of the verses dictionary is as follows:
    {
        "manuscript_id2": {
            "1": "text",
            "2": "text",
        },
        manuscript_id2: {
            "1": "text",
            "2": "text"
            }
    }
    """
    # Get the verse keys and sort them in ascending order
    verse_keys = sorted(set(int(key) for ms in verses.values()
                        for key in ms.keys()))
    verse_keys = [str(key) for key in verse_keys]
    num_verses = len(verse_keys)

    # Get the manuscript IDs
    manuscript_ids = list(verses.keys())

    # Initialize distance matrix
    distance_matrix = np.zeros((num_verses, 1))

    # Compute pairwise Jaccard distances for verses
    for i, verse in enumerate(verse_keys):
        # Collect texts from all manuscripts for these verse keys
        
        text1 = verses[manuscript_ids[0]].get(verse, "")
        text2 = verses[manuscript_ids[1]].get(verse, "")

        # Compute Jaccard distance
        dist = 1 - distance_function(text1, text2)
        distance_matrix[i, 0] = dist

    return verse_keys, distance_matrix


def cluster_texts(clustered_content: dict[str, dict[str, str]],
                  clusterer_class: ClusterMixin,
                  **kwargs):
    """
    Cluster the manuscripts according to their distance matrix.
    The selected method must be distance based.
    """
    manuscript_keys, distance_matrix = compute_distance_matrix_text(
        clustered_content)
    #TODO: remove hardcoding
    best_n_cluster = find_best_n_clusters(clusterer_class, distance_matrix, metric="precomputed", **kwargs)
    #####
    best_n_cluster = 5
    clusterer = clusterer_class(metric="precomputed", n_clusters=best_n_cluster, **kwargs)
    clusterer.fit(distance_matrix)
    return {
        manuscript_id: str(cluster_id) for manuscript_id, cluster_id in zip(manuscript_keys, clusterer.labels_)
    }


def compute_distance_matrix_profiles(profiles: dict[str, dict[str, str]]):
    """
    Compute the distance matrix between manuscripts based on their profiles.
    """
    # Extract profile IDs and corresponding data
    profile_ids = list(profiles.keys())
    distance_matrix = {pid: {} for pid in profile_ids}

    # Iterate through all pairs of profiles to calculate distances
    for i, id1 in enumerate(profile_ids):
        profile1 = profiles[id1]
        for j, id2 in enumerate(profile_ids):
            if j < i:
                # Use symmetry to save computation
                distance_matrix[id1][id2] = distance_matrix[id2][id1]
            elif j == i:
                # Distance to self is 0
                distance_matrix[id1][id2] = 0
            else:
                # Compute Hamming distance
                profile2 = profiles[id2]
                if set(profile1.keys()) != set(profile2.keys()):
                    raise ValueError(f"Profiles {id1} and {
                                     id2} have different keys.")
                distance_matrix[id1][id2] = sum(
                    profile1[key] != profile2[key] for key in profile1
                )
    return distance_matrix


def find_best_n_clusters(clustering_class, X, min_clusters=2, max_clusters=10, **kwargs):
    """
    Finds the optimal number of clusters for a given clustering class based on the silhouette score.

    Parameters:
    - clustering_class: The clustering class from scikit-learn (e.g., KMeans).
    - X: The data to be clustered.
    - min_clusters: Minimum number of clusters to consider (default is 2).
    - max_clusters: Maximum number of clusters to consider (default is 10).

    Returns:
    - best_n_clusters: The number of clusters with the highest silhouette score.
    - sil_score_max: The maximum silhouette score achieved.
    """
    sil_score_max = -1  # Minimum possible score
    
    for n_clusters in range(min_clusters, max_clusters):
        model = clustering_class(n_clusters=n_clusters, **kwargs)
        labels = model.fit_predict(X)
        sil_score = silhouette_score(X, labels)
        print(f"The average silhouette score for {n_clusters} clusters is {sil_score:.2f}")
        
        if sil_score > sil_score_max:
            sil_score_max = sil_score
            best_n_clusters = n_clusters

    return best_n_clusters





