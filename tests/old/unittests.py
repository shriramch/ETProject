import unittest
import argparse
from enumerator import setup, dfs, State


class TestEnumerator(unittest.TestCase):

    def DFS(self, max_depth):
        atn_state, parser = setup()
        init_state = State(atn_state, "")
        init_state.stack = []
        parser = argparse.ArgumentParser()
        parser.add_argument("solver1", help="the first SMT solver")
        parser.add_argument("solver2", help="the second SMT solver")
        parser.add_argument("depth", type=int, help="depth bound")
        parser.add_argument("--bugfolder", type=str, default="./bugs", help="bug folder")
        parser.add_argument("-t", "--timeout", type=int, help="timeout in secs", default=1)
        parser.add_argument("-m", "--max-iterations", type=int,
                            help="limit number of iterations", default=-1)

        args = parser.parse_args()
        formulas = dfs(parser, init_state, max_depth, args)
        return formulas

    def test_DFS(self):
        self.assertEqual(len(self.DFS(0)), 0)
        self.assertEqual(len(self.DFS(1)), 0)
        self.assertEqual(len(self.DFS(2)), 4)
        self.assertEqual(len(self.DFS(3)), 52)
        self.assertEqual(len(self.DFS(4)), 8116)



if __name__ == "__main__":
    unittest.main()

# python3.9 -m unittest test.py
