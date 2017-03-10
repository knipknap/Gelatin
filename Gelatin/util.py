# Copyright (c) 2010-2017 Samuel Abels
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import generator
from parser   import Parser
from compiler import SyntaxCompiler

def compile_string(syntax):
    """
    Builds a converter from the given syntax and returns it.

    :type  syntax: str
    :param syntax: A Gelatin syntax.
    :rtype:  compiler.Context
    :return: The compiled converter.
    """
    return Parser().parse_string(syntax, SyntaxCompiler())

def compile(syntax_file):
    """
    Like compile_string(), but reads the syntax from the file with the
    given name.

    :type  syntax_file: str
    :param syntax_file: Name of a file containing Gelatin syntax.
    :rtype:  compiler.Context
    :return: The compiled converter.
    """
    return Parser().parse(syntax_file, SyntaxCompiler())

def generate(converter, input_file, format = 'xml'):
    """
    Given a converter (as returned by compile()), this function reads
    the given input file and converts it to the requested output format.

    Supported output formats are 'xml', 'yaml', 'json', or 'none'.

    :type  converter: compiler.Context
    :param converter: The compiled converter.
    :type  input_file: str
    :param input_file: Name of a file to convert.
    :type  format: str
    :param format: The output format.
    :rtype:  str
    :return: The resulting output.
    """
    with open(input_file) as thefile:
        return generate_string(converter, thefile.read(), format = format)

def generate_to_file(converter, input_file, output_file, format = 'xml'):
    """
    Like generate(), but writes the output to the given output file
    instead.

    :type  converter: compiler.Context
    :param converter: The compiled converter.
    :type  input_file: str
    :param input_file: Name of a file to convert.
    :type  output_file: str
    :param output_file: The output filename.
    :type  format: str
    :param format: The output format.
    :rtype:  str
    :return: The resulting output.
    """
    with open(output_file, 'w') as thefile:
        result = generate(converter, input_file, format = format)
        thefile.write(result)

def generate_string(converter, input, format = 'xml'):
    """
    Like generate(), but reads the input from a string instead of
    from a file.

    :type  converter: compiler.Context
    :param converter: The compiled converter.
    :type  input: str
    :param input: The string to convert.
    :type  format: str
    :param format: The output format.
    :rtype:  str
    :return: The resulting output.
    """
    builder = generator.new(format)
    if builder is None:
        raise TypeError('invalid output format ' + repr(format))
    converter.parse_string(input, builder)
    return builder.serialize()

def generate_string_to_file(converter, input, output_file, format = 'xml'):
    """
    Like generate(), but reads the input from a string instead of
    from a file, and writes the output to the given output file.

    :type  converter: compiler.Context
    :param converter: The compiled converter.
    :type  input: str
    :param input: The string to convert.
    :type  output_file: str
    :param output_file: The output filename.
    :type  format: str
    :param format: The output format.
    :rtype:  str
    :return: The resulting output.
    """
    with open(output_file, 'w') as thefile:
        result = generate_string(converter, input_file, format = format)
        thefile.write(result)
