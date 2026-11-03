"""
Automated tests for word_analyzer.py
Run with:  python test_word_analyzer.py
"""

import os
import tempfile
import unittest

import word_analyzer as wa


class TestCase1NormalInput(unittest.TestCase):
    """Test Case 1: Text: Python is easy. Python is fun."""

    def test_counts(self):
        result = wa.analyse("Python is easy. Python is fun.")
        self.assertEqual(result["words"], 6)
        self.assertEqual(result["chars_with_spaces"], 30)
        self.assertEqual(result["sentences"], 2)


class TestCase2Boundary(unittest.TestCase):
    """Test Case 2: Text: Hello"""

    def test_counts(self):
        result = wa.analyse("Hello")
        self.assertEqual(result["words"], 1)
        self.assertEqual(result["chars_with_spaces"], 5)
        self.assertEqual(result["sentences"], 1)
        self.assertEqual(len(result["unique_words"]), 1)


class TestCase3InvalidInput(unittest.TestCase):
    """Test Case 3: (a) empty text  (b) file that does not exist"""

    def test_empty_text(self):
        self.assertTrue(wa.is_empty(""))
        self.assertTrue(wa.is_empty("   \n  "))
        self.assertTrue(wa.is_empty(None))
        self.assertEqual(wa.MSG_NO_TEXT, "No text to analyse.")

    def test_missing_file(self):
        if os.path.exists("notes.txt"):
            self.skipTest("notes.txt exists in this folder")
        text, error = wa.read_text_from_file("notes.txt")
        self.assertIsNone(text)
        self.assertEqual(error, "File 'notes.txt' not found.")


class TestCase4DifferentScenario(unittest.TestCase):
    """Test Case 4: Text: The cat saw the dog. The dog ran.  Menu option 2"""

    def test_frequency(self):
        result = wa.analyse("The cat saw the dog. The dog ran.")
        top = [pair for pair in result["frequency"] if pair[1] > 1]
        self.assertEqual(top, [("the", 3), ("dog", 2)])
        self.assertEqual(result["unique_words"], ["cat", "dog", "ran", "saw", "the"])
        self.assertEqual(len(result["unique_words"]), 5)


class TestExtraChecks(unittest.TestCase):
    """Extra tests for edge cases."""

    def test_case_insensitive(self):
        self.assertEqual(wa.word_frequency(wa.get_words("Cat CAT cat")), {"cat": 3})

    def test_punctuation_removed(self):
        self.assertEqual(wa.get_words("Hello, world!!!"), ["hello", "world"])

    def test_hyphen_splits_words(self):
        self.assertEqual(wa.get_words("well-known"), ["well", "known"])

    def test_sentence_types(self):
        self.assertEqual(wa.count_sentences("Hi! How are you? Fine."), 3)
        self.assertEqual(wa.count_sentences("Wait?! Really..."), 2)
        self.assertEqual(wa.count_sentences("Pi is 3.14 today."), 1)

    def test_only_punctuation_has_no_words(self):
        self.assertEqual(wa.analyse("!!! ... ???")["words"], 0)

    def test_extra_spaces_and_new_lines(self):
        self.assertEqual(wa.analyse("one   two\nthree")["words"], 3)

    def test_sort_order(self):
        freq = {"b": 1, "a": 1, "c": 2}
        self.assertEqual(wa.sort_by_frequency(freq), [("c", 2), ("a", 1), ("b", 1)])

    def test_read_existing_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "demo.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write("Python is easy. Python is fun.")
            text, error = wa.read_text_from_file(path)
            self.assertIsNone(error)
            self.assertEqual(wa.analyse(text)["words"], 6)

    def test_folder_instead_of_file(self):
        with tempfile.TemporaryDirectory() as folder:
            text, error = wa.read_text_from_file(folder)
            self.assertIsNone(text)
            self.assertIsNotNone(error)


if __name__ == "__main__":
    unittest.main(verbosity=2)
