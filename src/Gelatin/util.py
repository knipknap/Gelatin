import generator
from parser   import Parser
from compiler import SyntaxCompiler

_parser   = None
_compiler = None

def get_parser():
    global _parser
    if not _parser:
        _parser = Parser()
    return _parser

def get_compiler():
    global _compiler
    if not _compiler:
        _compiler = SyntaxCompiler()
    return _compiler

def compile_string(syntax):
    return get_parser().parse_string(syntax, get_compiler())

def compile(syntax_file):
    return get_parser().parse(syntax_file, get_compiler())

def generate_to_file(converter, input_file, output_file, format = 'xml'):
    builder = generator.new(format)
    if builder is None:
        raise TypeError('invalid output format ' + repr(format))
    converter.parse(input_file, builder)
    builder.serialize_to_file(output_file)
