import unittest
from src.estimate import estimate_score_with_iteration, read_data_from_csv


class TestModel(unittest.TestCase):

    def test_estimate_score(self):
        # 使用模拟的测试数据
        data = [(1580, True), (1600, False), (1550, True)]
        estimated_score, confidence_interval = estimate_score_with_iteration(
            data, initial_score=1580)
        self.assertGreater(estimated_score, 0)
        self.assertTrue(
            confidence_interval[0] < estimated_score < confidence_interval[1])

    def test_read_data(self):
        data = read_data_from_csv('./data/questions_data.csv')
        self.assertGreater(len(data), 0)


if __name__ == '__main__':
    unittest.main()
