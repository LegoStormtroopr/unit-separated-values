import unittest
import usv
from pathlib import Path

sample_data = """# Fisher's Iris data set


This group contains the first 3 rows of the Fisher data set
Dataset orderSepal lengthSepal widthPetal lengthPetal widthSpecies
15.13.51.40.2I. setosa
24.93.01.40.2I. setosa
1505.93.05.11.8I. virginica


This group contains the last 3 rows of the Fisher data set
Dataset orderSepal lengthSepal widthPetal lengthPetal widthSpecies
1486.53.05.22.0I. virginica
1496.23.45.42.3I. virginica
1505.93.05.11.8I. virginica
"""

examples = Path("../examples")

class TestUSV(unittest.TestCase):

    def test_a_parsererror(self):
        err = usv.BetterParseError(None, 5, "This text is broken")

    def test_roundtrip(self):
        before = usv.USVReader(sample_data)
        before.insert(1, usv.Annotation("More text"))
        after = usv.USVReader(str(before))
        self.assertEqual(before, after)

    def test_fromfile_roundtrip(self):
        before = usv.USVReader.from_file(examples / "iris-data-set.usv.md")
        after = usv.USVReader(str(before))
        self.assertEqual(before, after)

    def test_nonstrict(self):
        before = usv.USVReader(sample_data, strict=False)
        # before.insert(1, usv.Annotation("More text"))
        # after = usv.USVReader(str(before))
        # self.assertEqual(before, after)


if __name__ == '__main__':
    unittest.main()
