#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""An enhanced version of the 'echo' cmd line utility."""

__author__ = "PokeyJess, with help from Daniel's walk-through"


import sys
import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        description="Perform transformation on input text.")
    parser.add_argument('text', help="text to be manipulated")
    parser.add_argument('-u', '--upper', action="store_true",
                        help="convert text to uppercase")
    parser.add_argument('-l', '--lower', action="store_true",
                        help="convert text to lowercase")
    parser.add_argument('-t', '--title', action="store_true",
                        help="convert text to titlecase")
    return parser


def main(args):
    parser = create_parser()
    args = parser.parse_args(args)
    msg = args.text
    if args.upper:
        msg = msg.upper()
    if args.lower:
        msg = msg.lower()
    if args.title:
        msg = msg.title()
    print(msg)


if __name__ == '__main__':
    main(sys.argv[1:])
