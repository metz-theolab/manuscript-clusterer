"""Test the engine for the classification of manuscripts.
"""

import unittest
from manuscript_clusterer.engine.get_profiles import evaluate_manuscript_profile


class TestComputeProfile(unittest.TestCase):
    """Tests that computing the silhouette behaves as expected.
    """

    def setUp(self):
        self.manuscript_1 = {'1': {'1': 'επειδηπερ πολλοι επεχειρησαν αναταξασθαι διηγησιν περι των πεπληροφορημενων εν ημειν πραγματων ',
                                   '2': 'καθα παρεδοσαν ημειν οι απ αρχης αυτοπται και υπηρεται γενομενοι του λογου ',
                                   '3': 'εδοξε καμοι παρηκολουθηκοτι ανωθεν πασιν ακριβως καθεξης σοι γραψαι κρατιστε θεοφιλε ',
                                   '4': 'ινα επιγνως περι ων κατηχηθης λογων την ασφαλειαν ',
                                   '5': 'εγενετο εν ταις ημεραις ηρωδου του βασιλεως της ιουδαιας ιερευς τις ονοματι ζαχαριας εξ εφημεριας αβια και γυνη αυτω εκ των θυγατερων ααρων και το ονομα αυτης ελεισαβεθ ',
                                   '6': 'ησαν δε δικαιοι αμφοτεροι ενωπιον του θυ πορευομενοι εν πασαις ταις εντολαις και δικαιωμασιν του κυ αμεπτοι ',
                                   '7': 'και ουκ ην αυτοις τεκνον καθοτι ην η ελισαβεθ στειρα και αμφοτεροι ησαν προβεβηκοτες εν ταις ημεραις αυτων ',
                                   '8': 'εγενετο δε εν τω ιερατευειν αυτον εν τη ταξει της εφημεριας αυτου εναντι του θυ ',
                                   '9': 'κατα το εθος της ιερατειας ελαχε του θυμιασαι εισελθων εις τον ναον του θυ '}}
        self.readings_id = ["1:1", "1:2", "1:3", "1:4", "1:5"]

    def test_compute_profile(self):
        """Tests that computing the profiles behaves as expected.
        """
        profile = evaluate_manuscript_profile(self.manuscript_1,
                                              chapters=[1])
        # Limit the scope to the first 5 readings
        profile = {key: profile[key] for key in self.readings_id}
        expected_profile = {"1:1": 0,
                            "1:2": 1,
                            "1:3": 0,
                            "1:4": 0,
                            "1:5": 1}
        self.assertEqual(profile,
                         expected_profile)


if __name__ == "__main__":
    unittest.main()
