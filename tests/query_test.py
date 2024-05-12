import unittest

import scripts.query_profs as qp
from scripts.course import Course, Campus, Session


class TestProfQuery(unittest.TestCase):
    def setUp(self):
        self.tb_v2_query = qp.ProfQuery("../ubc-pair-grade-data/tableau-dashboard-v2/UBCV/**/*.csv")
        # self.query_all = qp.ProfQuery("../ubc-pair-grade-data/**/**/**/*.csv")
        self.expected = [Course(Campus.Vancouver, 2023, Session.Summer, "LING", "201", None, "921",
                                "Linguistic Theory and Analysis II"),
                         Course(Campus.Vancouver, 2022, Session.Winter, "LING", "447", "B", "002",
                                "Topics in Linguistics"),
                         Course(Campus.Vancouver, 2022, Session.Winter, "LING", "201", None, "002",
                                "Linguistic Theory and Analysis II"),

                         Course(Campus.Vancouver, 2021, Session.Winter, "LING", "532", None, "002",
                                "Field Methods in Linguistics II"),
                         Course(Campus.Vancouver, 2021, Session.Winter, "LING", "531", None, "001",
                                "Field Methods in Linguistics I"), ]

    def test_ctor(self):
        # non-empty
        self.assertGreater(len(self.tb_v2_query.data), 2)

    def test_query_exact(self):
        self.query_test_helper("Michael Ryan Bochnak")

    def test_query_ssc(self):
        self.query_test_helper(self.tb_v2_query.close_profs("BOCHNAK, MICHAEL RYAN", count=1)[0])

    def query_test_helper(self, q: str):
        actual = self.tb_v2_query.query(q)

        self.assertEqual(len(self.expected), len(actual))

        for expected_course, actual_course in zip(self.expected, actual):
            self.assertEqual(expected_course, actual_course)


if __name__ == '__main__':
    unittest.main()
