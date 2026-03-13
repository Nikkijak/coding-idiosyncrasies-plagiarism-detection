import os
import sys
import tempfile
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from lex_tokenizer import tokenize, toText
from winnowing import sha1_hash, kgrams, min_index, fingerprints, hash_list, process_text, compare_fingerprints


class BaseTempFileTest(unittest.TestCase):
    def make_file(self, content, suffix=".py"):
        temp = tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False, encoding="utf-8")
        temp.write(content)
        temp.close()
        self.addCleanup(lambda: os.path.exists(temp.name) and os.remove(temp.name))
        return temp.name


class TestTokenizer(BaseTempFileTest):
    def test_tokenize_structure(self):
        path = self.make_file("x=1\nprint(x)\n")
        tokens = tokenize(path)

        self.assertIsInstance(tokens, list)
        self.assertGreater(len(tokens), 0)
        self.assertTrue(all(len(t) == 3 for t in tokens))

    def test_normalized_text(self):
        path = self.make_file("x=1\nprint(x)\n")
        text = toText(tokenize(path))

        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)

    def test_variable_renaming_normalization(self):
        p1 = self.make_file("x=1\nprint(x)\n")
        p2 = self.make_file("value=1\nprint(value)\n")

        self.assertEqual(toText(tokenize(p1)), toText(tokenize(p2)))


class TestWinnowingHelpers(unittest.TestCase):
    def test_sha1_hash(self):
        self.assertIsInstance(sha1_hash("test"), int)

    def test_kgrams(self):
        grams = kgrams("ABCDEFGH", 3)
        self.assertEqual(len(grams), 6)
        self.assertEqual(grams[0][0], "ABC")
        self.assertEqual(grams[-1][0], "FGH")

    def test_min_index(self):
        self.assertEqual(min_index([9, 3, 5, 3]), 1)

    def test_hash_list(self):
        grams = [("ABC", 100, 0, 3), ("BCD", 200, 1, 4)]
        self.assertEqual(hash_list(grams), [100, 200])

    def test_fingerprints_small_input(self):
        arr = [8, 2, 5]
        self.assertEqual(fingerprints(arr, win_size=5), [2])


class TestPlagiarismPipeline(BaseTempFileTest):
    def test_process_text(self):
        path = self.make_file("x=1\ny=2\nprint(x+y)\n")
        fp = process_text(path)

        self.assertIsInstance(fp, list)
        self.assertGreater(len(fp), 0)

    def test_process_text_invalid_t(self):
        path = self.make_file("x=1\n")

        with self.assertRaises(ValueError):
            process_text(path, t=5)

    def test_identical_files_similarity(self):
        p1 = self.make_file("x=1\nprint(x)\n")
        p2 = self.make_file("x=1\nprint(x)\n")

        similarity, matches = compare_fingerprints(process_text(p1), process_text(p2))

        self.assertEqual(similarity, 100.0)
        self.assertGreater(len(matches), 0)

    def test_variable_renaming_high_similarity(self):
        p1 = self.make_file("x=1\nprint(x)\n")
        p2 = self.make_file("value=1\nprint(value)\n")

        similarity, _ = compare_fingerprints(process_text(p1), process_text(p2))

        self.assertGreaterEqual(similarity, 80.0)

    def test_different_files_lower_similarity(self):
        p1 = self.make_file("x=1\nprint(x)\n")
        p2 = self.make_file("total=0\nfor i in range(3):\n total+=i\nprint(total)\n")

        similarity, _ = compare_fingerprints(process_text(p1), process_text(p2))
        self.assertLess(similarity, 100.0)


if __name__ == "__main__":
    unittest.main()