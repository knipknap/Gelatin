import sys, unittest, re, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from Gelatin.util import compile, generate

demo_dir = os.path.join('..', 'demo')

def convert(filename, format):
    syntax_file = os.path.join(demo_dir, filename, 'syntax.gel')
    input_file = os.path.join(demo_dir, filename, 'input1.txt')
    syntax = compile(syntax_file)
    return generate(syntax, input_file, format)

class DemoTest(unittest.TestCase):
    def setUp(self):
        self.demos = os.listdir(demo_dir)

    def testDemos(self):
        for filename in self.demos:
            for format in ('xml', 'yaml', 'json'):
                output = convert(filename, format)
                output_file = os.path.join(demo_dir, filename, 'output1.' + format)
                with open(output_file) as fp:
                    self.assertEqual(output, fp.read())

def suite():
    return unittest.TestLoader().loadTestsFromTestCase(DemoTest)
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity = 2).run(suite())
