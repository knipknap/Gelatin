import generator
from parser   import Parser
from compiler import SyntaxCompiler

def compile_string(syntax):
    return Parser().parse_string(syntax, SyntaxCompiler())

def compile(syntax_file):
    return Parser().parse(syntax_file, SyntaxCompiler())

def generate_to_file(converter, input_file, output_file, format = 'xml'):
    builder = generator.new(format)
    if builder is None:
        raise TypeError('invalid output format ' + repr(format))
    converter.parse(input_file, builder)
    builder.serialize_to_file(output_file)

def generate_string_to_file(converter, input, output_file, format = 'xml'):
    builder = generator.new(format)
    if builder is None:
        raise TypeError('invalid output format ' + repr(format))
    converter.parse_string(input, builder)
    builder.serialize_to_file(output_file)
