import unittest


class TestSymbol(unittest.TestCase):
    def test_symbol(self):
        self.assertTrue('HELLO')
       
class TestChart(unittest.TestCase):
    def test_chart(self):
        self.assertTrue('1')
        self.assertTrue('2')

class TestTime(unittest.TestCase):
    def test_time(self):
        self.assertTrue('1')
        self.assertTrue('2')
        self.assertTrue('3')
        self.assertTrue('4')

class TestStart(unittest.TestCase):
    def test_start(self):
        self.assertTrue('2020-03-30')

class TestEnd(unittest.TestCase):
    def test_end(self):
        self.assertTrue('2020-03-30')


if __name__ == '__main__':
    unittest.main()