import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app.logic import extract_lessons_tokens
from tests.cases import token_test_cases

class TestTokens(unittest.TestCase):
    def test_tokens(self):
        for inputs, expected in token_test_cases:
            with self.subTest(inputs=inputs, outputs=expected):
                self.assertEqual(extract_lessons_tokens(inputs), expected)

if __name__ == '__main__':
    unittest.main(verbosity=0)
    
