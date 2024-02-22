# tests.py

import unittest

from src import project


class ProjectTests(unittest.TestCase):
    
    def test_my_first_test(self):
        self.assertEqual(5, 5)
        
        
if __name__ == '__main__':
    unittest.main()
