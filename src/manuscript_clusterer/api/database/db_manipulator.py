"""Set of utils for manipulating the Mongo database.
"""
from typing import Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from sklearn.cluster import DBSCAN, KMeans, AgglomerativeClustering
from sklearn.metrics import adjusted_rand_score
from manuscript_clusterer.engine.project import perform_projection_profiles, perform_projection_content
from manuscript_clusterer.engine.cluster import cluster_profiles, cluster_texts, compute_distance_matrix_text, compute_distance_matrix_profiles, compute_distance_matrix_verse_text


class MongoDB:
    """Class for the manipulation of the manuscript data.
    """

    def __init__(self,
                 host: str = "localhost",
                 port: int = 27017,
                 db_name: str = "manuscriptsDB"):
        """Initialize the connection with the database.
        """
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.check_connection()

    def check_connection(self):
        """
        Check the connection with the database.
        """
        try:
            self.client.admin.command('ping')
        except ConnectionFailure:
            print("Server not available")

    def insert_document(self,
                        collection_name: str,
                        document: dict[str, Any]):
        """Insert a document into a collection.
        """
        collection = self.db[collection_name]
        result = collection.insert_one(document)
        return result.inserted_id

    def find_document(self,
                      collection_name: str,
                      query: dict[str, Any],
                      projection: dict[str, Any] = None):
        """Find a document in a collection.
        """
        collection = self.db[collection_name]
        return collection.find_one(query, projection)

    def find_all_documents(self,
                           collection_name: str,
                           query: dict[str, Any],
                           projection: dict[str, Any] = None):
        """Find all documents in a collection.
        """
        collection = self.db[collection_name]
        return list(collection.find(query, projection))

    def update_document(self,
                        collection_name: str,
                        query: dict[str, Any],
                        update: dict[str, Any]):
        """Update a document in a collection.
        """
        collection = self.db[collection_name]
        result = collection.update_one(query,
                                       {'$set': update})
        return result.modified_count

    def delete_document(self,
                        collection_name: str,
                        query: dict[str, Any]):
        """Delete a document from a collection.
        """
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count


class ManuscriptDB(MongoDB):
    """Class for the manipulation of the manuscript data.
    """

    def __init__(self,
                 host: str = "localhost",
                 port: int = 27017,
                 db_name: str = "manuscriptsDB"):
        """Initialize the connection with the database.
        """
        super().__init__(host, port, db_name)

    def get_manuscripts(self):
        """Get all manuscripts from the database.
        """
        return list(self.db["manuscripts"].find({}, {"_id": 0, "id": 1}))

    def get_manuscript(self, manuscript_id: str):
        """Get a manuscript from the database.
        """
        return self.find_document("manuscripts",
                                  {"id": manuscript_id},
                                  {"_id": 0})

    def get_manuscript_content(self, manuscript_id: str):
        """Get the content of a manuscript from the database.
        """
        return self.find_document("manuscripts",
                                  {"id": manuscript_id,
                                   },
                                  {"_id": 0,
                                   "content": 1})

    def get_manuscript_profile(self, manuscript_id: str):
        """Get the profile of a manuscript from the database.
        """
        return self.find_document("manuscripts", {"id": manuscript_id,
                                                  },
                                  {"_id": 0,
                                   "profile": 1})

    def get_manuscripts_profiles(self, manuscripts_list: list[str]):
        """Given a list of mnuscript, return their profiles.
        """
        return self.find_all_documents("manuscripts",
                                       {"id": {"$in": manuscripts_list}},
                                       {"_id": 0,
                                        "profile": 1,
                                        "id": 1})

    def get_all_manuscripts_profiles(self):
        """Return all manuscripts profiles.
        """
        return self.find_all_documents("manuscripts",
                                       {},
                                       {"_id": 0,
                                        "profile": 1,
                                        "id": 1})

    def get_all_manuscripts_readings(self):
        """Return all manuscripts profiles.
        """
        return self.find_all_documents("manuscripts",
                                       {},
                                       {"_id": 0,
                                        "readings": 1,
                                        "id": 1})

    def get_manuscripts_content(self, manuscripts_list: list[str]):
        """Given a list of manuscripts, return their content.
        """
        return self.find_all_documents("manuscripts",
                                       {"id": {"$in": manuscripts_list}},
                                       {"_id": 0,
                                        "content": 1,
                                        "id": 1})

    def get_all_manuscripts_content(self):
        """Return all manuscripts profiles.
        """
        return self.find_all_documents("manuscripts",
                                       {},
                                       {"_id": 0,
                                        "content": 1,
                                        "id": 1})

    def get_manuscript_info(self, manuscript_id: str):
        """Get the profile and content of a manuscript from the database.
        """
        return self.find_all_documents(
            "manuscripts",
            {"id": manuscript_id},
            {"_id": 0,
             "fullname": 1,
                "wisse": 1,
                "von-soden": 1,
                "text-type": 1,
                "aland-cat": 1,
                "date": 1}
        )

    def get_manuscript_verses(self, manuscript_id: str, chapter: str, verse: str):
        """Get the list of the verses within a manuscript.
        """
        manuscript_content = self.find_document("manuscripts",
                                                {"id": manuscript_id},
                                                {"_id": 0,
                                                    "content": 1})
        return manuscript_content["content"][chapter][verse]

    def get_manuscripts_projected(self,
                                  manuscripts_list: list[str] = None,
                                  all_manuscripts: bool = False):
        """Given a list of manuscript, return their profiles.
        If all is enabled, all manuscripts are returned.
        Either one of the two must be enabled.
        """
        if not all_manuscripts:
            if not manuscripts_list:
                raise ValueError(
                    "Either all_manuscripts or manuscripts_list must be enabled")
        if not all_manuscripts:
            profiles = self.get_manuscripts_profiles(manuscripts_list)
        else:
            profiles = self.get_all_manuscripts_profiles()
        profiles = {profile["id"]: profile["profile"] for profile in profiles}
        return perform_projection_profiles(profiles)

    def get_content_projected(self,
                              chapter: str,
                              manuscripts_list: list[str] = None,
                              all_manuscripts: bool = False):
        """Given a list of manuscript, return their profiles.
        If all is enabled, all manuscripts are returned.
        Either one of the two must be enabled.
        """
        if not all_manuscripts:
            if not manuscripts_list:
                raise ValueError(
                    "Either all_manuscripts or manuscripts_list must be enabled")
        if not all_manuscripts:
            content = self.get_all_manuscripts_content(manuscripts_list)
        else:
            content = self.get_all_manuscripts_content()
        content = {text["id"]: text["content"][chapter] for text in content}
        return perform_projection_content(content)

    def get_profile_clustered(self,
                              manuscripts_list: list[str] = None,
                              all_manuscripts: bool = False):
        """Given a list of manuscript, return their profiles.
        If all is enabled, all manuscripts are returned.
        Either one of the two must be enabled.
        """
        if not all_manuscripts:
            if not manuscripts_list:
                raise ValueError(
                    "Either all_manuscripts or manuscripts_list must be enabled")
        if not all_manuscripts:
            profiles = self.get_manuscripts_profiles(manuscripts_list)
        else:
            profiles = self.get_all_manuscripts_profiles()
        profiles = {profile["id"]: profile["profile"] for profile in profiles}
        return cluster_profiles(profiles, clusterer_class=AgglomerativeClustering)

    def get_readings_clustered(self,
                               manuscripts_list: list[str] = None,
                               all_manuscripts: bool = False):
        """Given a list of manuscript, return their profiles.
        If all is enabled, all manuscripts are returned.
        Either one of the two must be enabled.
        """
        if not all_manuscripts:
            if not manuscripts_list:
                raise ValueError(
                    "Either all_manuscripts or manuscripts_list must be enabled")
        if not all_manuscripts:
            readings = self.get_all_manuscripts_readings(manuscripts_list)
        else:
            readings = self.get_all_manuscripts_readings()
        readings = {reading["id"]: reading["readings"] for reading in readings}
        return cluster_texts(readings,  clusterer_class=AgglomerativeClustering)

    def get_content_clustered(self,
                              chapter: str,
                              manuscripts_list: list[str] = None,
                              all_manuscripts: bool = False):
        """Given a list of manuscript, return their profiles.
        If all is enabled, all manuscripts are returned.
        Either one of the two must be enabled.
        """
        if not all_manuscripts:
            if not manuscripts_list:
                raise ValueError(
                    "Either all_manuscripts or manuscripts_list must be enabled")
        if not all_manuscripts:
            content = self.get_all_manuscripts_content(manuscripts_list)
        else:
            content = self.get_all_manuscripts_content()
        content = {text["id"]: text["content"][chapter] for text in content}
        return cluster_texts(content,
                              clusterer_class=AgglomerativeClustering,
                              linkage="complete")

    def get_content_distances(self,
                              chapter: str,
                              manuscripts_list: list[str] = None,
                              all_manuscripts: bool = False):
        """Given a list of manuscript, return the distance between them.
        """
        if not all_manuscripts:
            if not manuscripts_list:
                raise ValueError(
                    "Either all_manuscripts or manuscripts_list must be enabled")
        if not all_manuscripts:
            content = self.get_manuscripts_content(manuscripts_list)
        else:
            content = self.get_all_manuscripts_content()
        content = {text["id"]: text["content"][chapter] for text in content}
        return compute_distance_matrix_text(content)

    def get_reading_distances(self,
                              manuscripts_list: list[str] = None,
                              all_manuscripts: bool = False):
        """Given a list of manuscript, return the distance between them using their reading.
        """
        pass

    def get_profile_distance(self,
                             chapter: str,
                             manuscripts_list: list[str] = None,
                             all_manuscripts: bool = False):
        """Get the distance between the profiles.
        """
        if not all_manuscripts:
            if not manuscripts_list:
                raise ValueError(
                    "Either all_manuscripts or manuscripts_list must be enabled")
        if not all_manuscripts:
            profiles = self.get_manuscripts_profiles(manuscripts_list)
        else:
            profiles = self.get_all_manuscripts_profiles()
        profiles = {profile["id"]: profile["profile"] for profile in profiles}
        return compute_distance_matrix_profiles(profiles)

    def get_verse_distance_content(self,
                                   manuscript_1: str,
                                   manuscript_2: str,
                                   chapter: str):
        """Get the distance between the verses.
        """
        manuscript_1_content = self.get_manuscript_content(manuscript_1)[
            "content"][chapter]
        manuscript_2_content = self.get_manuscript_content(manuscript_2)[
            "content"][chapter]
        return compute_distance_matrix_verse_text(
            {manuscript_1: manuscript_1_content,
             manuscript_2: manuscript_2_content})

    def get_verse_distance_profiles(self,
                                    manuscript_1: str,
                                    manuscript_2: str):
        """Get the distance between the verses.
        """
        manuscript_1_profile = self.get_manuscript_profile(manuscript_1)
        manuscript_2_profile = self.get_manuscript_profile(manuscript_2)
        return compute_distance_matrix_profiles({manuscript_1: manuscript_1_profile,
                                                 manuscript_2: manuscript_2_profile})

    def measure_cluster_quality(self,
                                clusters: list[str],
                                ground_truth: list[str]):
        """Measure distance between clusterings.
        """
        return round(adjusted_rand_score(clusters, ground_truth), 2)