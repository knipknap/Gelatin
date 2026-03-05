# Copyright (C) 2010 Samuel Abels.
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
"""Command-line interface for Gelatin."""
from __future__ import annotations

import datetime
import os
import sys
from argparse import ArgumentParser

from Gelatin import __version__, generator
from Gelatin.generator import Builder
from Gelatin.util import compile


def _build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="gel",
        description="Transform text files to XML, JSON, or YAML using Gelatin syntax.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "-s",
        "--syntax",
        required=True,
        metavar="FILE",
        help="The file containing the syntax for parsing the input.",
    )
    parser.add_argument(
        "-f",
        "--format",
        default="xml",
        metavar="FORMAT",
        help="The output format. Valid values: xml json yaml none. Default: xml.",
    )
    parser.add_argument(
        "--debug",
        type=int,
        default=0,
        metavar="NUM",
        help="Print debug info.",
    )
    parser.add_argument(
        "input_files",
        nargs="+",
        metavar="FILE",
        help="Input files to process.",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    """Entry point for the ``gel`` command."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if not os.path.exists(args.syntax):
        parser.error(f"no such file or directory: {args.syntax}")
    if not os.path.isfile(args.syntax):
        parser.error(f"not a valid input file: {args.syntax}")

    serializer = generator.new(args.format)
    if serializer is None:
        parser.error(f"invalid output format: {args.format}")

    def dbg(*msg: str) -> None:
        if args.debug:
            now = str(datetime.datetime.now())
            sys.stderr.write(now + " " + " ".join(msg) + "\n")

    start = datetime.datetime.now()
    dbg("Compiling", args.syntax + "...")
    converter = compile(args.syntax)
    for input_file in args.input_files:
        dbg("Parsing", input_file + "...")
        builder = Builder()
        converter.parse(input_file, builder, debug=args.debug)
        if args.format != "none":
            dbg("Generating output...")
            print(builder.serialize(serializer))
    dbg("Total: " + str(datetime.datetime.now() - start))


if __name__ == "__main__":
    main()
