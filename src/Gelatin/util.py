import generator
from parser   import Parser
from compiler import SyntaxCompiler

def compile_string(syntax):
    """
    Builds a converter from the given syntax and returns it.

    @type  syntax: str
    @param syntax: A Gelatin syntax.
    @rtype:  compiler.Context
    @return: The compiled converter.
    """
    return Parser().parse_string(syntax, SyntaxCompiler())

def compile(syntax_file):
    """
    Like compile_string(), but reads the syntax from the file with the
    given name.

    @type  syntax_file: str
    @param syntax_file: Name of a file containing Gelatin syntax.
    @rtype:  compiler.Context
    @return: The compiled converter.
    """
    return Parser().parse(syntax_file, SyntaxCompiler())

def generate(converter, input_file, format = 'xml'):
    """
    Given a converter (as returned by compile()), this function reads
    the given input file and converts it to the requested output format.

    Supported output formats are 'xml', 'yaml', 'json', or 'none'.

    @type  converter: compiler.Context
    @param converter: The compiled converter.
    @type  input_file: str
    @param input_file: Name of a file to convert.
    @type  format: str
    @param format: The output format.
    @rtype:  str
    @return: The resulting output.
    """
    return generate_string(converter, open(input_file).read(), format = 'xml')

def generate_to_file(converter, input_file, output_file, format = 'xml'):
    """
    Like generate(), but writes the output to the given output file
    instead.

    @type  converter: compiler.Context
    @param converter: The compiled converter.
    @type  input_file: str
    @param input_file: Name of a file to convert.
    @type  output_file: str
    @param output_file: The output filename.
    @type  format: str
    @param format: The output format.
    @rtype:  str
    @return: The resulting output.
    """
    input  = open(input_file).read()
    result = generate_string(converter, input, format = 'xml')
    open(output_file, 'w').write(result)

def generate_string(converter, input, format = 'xml'):
    """
    Like generate(), but reads the input from a string instead of
    from a file.

    @type  converter: compiler.Context
    @param converter: The compiled converter.
    @type  input: str
    @param input: The string to convert.
    @type  format: str
    @param format: The output format.
    @rtype:  str
    @return: The resulting output.
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

    @type  converter: compiler.Context
    @param converter: The compiled converter.
    @type  input: str
    @param input: The string to convert.
    @type  output_file: str
    @param output_file: The output filename.
    @type  format: str
    @param format: The output format.
    @rtype:  str
    @return: The resulting output.
    """
    result = generate_string(converter, input, output_file, format)
    open(output_file, 'w').write(result)
