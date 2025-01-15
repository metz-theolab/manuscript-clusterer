"""Tests that performing clustering behaves as expected.
"""
import unittest
from sklearn.cluster import KMeans, DBSCAN
import numpy as np
from manuscript_clusterer.engine.cluster import cluster_profiles, compute_distance_matrix_text, cluster_texts


class TestClustering(unittest.TestCase):
    """Tests that performing clustering behaves as expected.
    """

    def test_cluster_profiles(self):
        """Tests that clustering the profiles behaves as expected.
        """
        profiles = {
            "20001": {
                "1:1": 0,
                "1:2": 0,
                "1:3": 0,
                "1:4": 1,
                "1:5": 0,
                "1:6": 1,
                "1:7": 0,
                "1:8": 1,
                "1:9": 0,
                "1:10": 0
            },
            "20002": {
                "1:1": 0,
                "1:2": 0,
                "1:3": 0,
                "1:4": 1,
                "1:5": 0,
                "1:6": 0,
                "1:7": 0,
                "1:8": 1,
                "1:9": 0,
                "1:10": 0
            },
            "20003": {
                "1:1": 0,
                "1:2": 0,
                "1:3": 0,
                "1:4": 0,
                "1:5": 0,
                "1:6": 1,
                "1:7": 0,
                "1:8": 1,
                "1:9": 0,
                "1:10": 0
            }
        }
        self.assertEqual(cluster_profiles(
            profiles,
            clusterer_class=KMeans,
            n_clusters=2,
            random_state=0
        ),
            {'20001': 0,
             '20002': 0,
             '20003': 1})

    def test_compute_distance(self):
        """
        Tests that computing the distance matrix behaves as expected.
        """
        clustered_content = {
            "ms1": {"1:1": "text1", "1:2": "text2"},
            "ms2": {"1:1": "text1", "1:2": "text2"},
            "ms3": {"1:1": "another_text", "1:2": "text2"}
        }
        manuscript_keys, distance_matrix = compute_distance_matrix_text(
            clustered_content)
        self.assertEqual(manuscript_keys, ["ms1", "ms2", "ms3"])
        expected_matrix = np.array([
            [0, 0, 0.69],
            [0, 0, 0.69],
            [0.69, 0.69, 0]
        ])
        self.assertTrue(np.allclose(distance_matrix,
                        expected_matrix, rtol=1e-2))

    def test_cluster_readings(self):
        """Tests that clustering the variants behaves as expected.
        """
        readings = {
            "20001": {
                "1:1": "παρεδοσαν",
                "1:2": "και ουκ ην αυτοις τεκνον καθοτι ην η ελεισαβετ στειρα και αμφοτεροι προβεβηκοτες εν ταις ημεραις αυτων ησαν ",
                "1:3": "η",
                "1:4": "εναντιον",
                "1:5": "κυριου"
            },
            "20002": {
                "1:1": "καθως παρεδωσαν ημειν οι απ αρχης αυτοπται και υπηρεται γενομενοι του λογου ",
                "1:2": "και ουκ ην αυτοις τεκνον καθοτι η ελισαβετ ην στειρα και αμφοτεροι προβεβηκοτες εν ταις ημεραις αυτων ησαν ",
                "1:3": "η",
                "1:4": "εναντιον",
                "1:5": "κυριου"
            },
            "20003": {
                "1:1": "παρεδοσαν",
                "1:2": "και ουκ ην αυτοις τεκνον καθοτι ην ελισαβετ στειρα και αμφοτεροι προβεβηκοτες εν ταις ημεραις αυτων ησαν ",
                "1:3": "η",
                "1:4": "εναντι",
                "1:5": "κυριου"
            },
            "20004": {
                "1:1": "και υπηρεται γενομενου του λογου ",
                "1:2": "και ουκ ην αυτοις τεκνον καθοτει η ελεισαβετ ην στειρα και αμφοτεροι προβεβηκοτες εν ταις ημεραις αυτων ησαν ",
                "1:3": "η",
                "1:4": "εναντιον",
                "1:5": "κυριου"
            }
        }
        self.assertEqual(cluster_texts(
            readings,
            clusterer_class=DBSCAN
        ),
            {'20001': '-1',
             '20002': '-1',
             '20003': '-1',
             '20004': '-1'})

    def test_cluster_content(self):
        """Tests that clustering the content behaves as expected.
        """
        texts = {
            "20001": {
                "1": "επειδηπερ πολλοι επεχειρησαν αναταξασθαι διηγησιν περι των πεπληροφορημενων εν ημιν πραγματων",
                "2": "καθως παρεδοσαν ημιν οι απ αρχης αυτοπται και υπηρεται γενομενοι του λογου",
                "3": "εδοξε καμοι παρηκολουθηκοτι ανωθεν πασιν ακρειβως καθεξης σοι γραψαι κρατιστε θεοφιλε",
                "4": "ινα επιγνως περι ων κατηχηθης λογων την ασφαλιαν",
                "5": "εγενετο εν ταις ημεραις ηρωδου βασιλεως της ιουδαιας ιερευς τις ονοματι ζαχαριας εξ εφημεριας αβια και γυνη αυτω εκ των θυγατερων ααρων και το ονομα αυτης ελισαβετ"
            },
            "20002": {
                "1": "επειδηπερ πολλοι επεχειρησαν αναταξασθαι διηγησιν περι των πεπληροφορημενων εν ημιν πραγματων",
                "2": "καθως παρεδωσαν ημειν οι απ αρχης αυτοπται και υπηρεται γενομενοι του λογου",
                "3": "εδοξεν καμοι παρηκολουθηκοτι ανωθεν πασιν ακριβως καθεξης σοι γραψαι κρατιστε θεοφιλε",
                "4": "ινα επιγνως περι ων κατηχηθης λογων την ασφαλειαν",
                "5": "εγενετο εν ταις ημεραις ηρωδου του βασιλεως της ιουδαιας ιερευς τις ονοματι ζαχαριας εξ εφημεριας αβια και η γυνη αυτου εκ των θυγατερων ααρων και ονομα αυτης ελισαβετ"
            }
        }
        self.assertEqual(cluster_texts(
            texts,
            clusterer_class=DBSCAN
        ),
            {'20001': '-1',
             '20002': '-1'})


if __name__ == "__main__":
    unittest.main()
