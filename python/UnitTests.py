import unittest
import MarkdownLog

class testMarkdown(unittest.TestCase):
    testMd = """# 2025-04-08
    ## My new exercise.
    This is my note.

    | Value | Reps |
    | ----- | ---- |
    | 10    | 12   |
    | 12    | 8    |
    |       |      |
    """

    def testDays(self):
      with open("/__pycache__/test.md", "w") as textFile:
        textFile.write(testMd)
      MarkdownLog("/__pycache__/test.md")
     


if __name__ == '__main__':
    unittest.main()