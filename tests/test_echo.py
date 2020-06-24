#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Implements a test fixture for the echo.py module

Students are expected to edit this module, to add more tests to run
against the 'echo.py' program.
"""

__author__ = "PokeyJess, with help from Daniel's walk-through"
# especially that test_help! Phew!

import sys
import importlib
import inspect
import argparse
import unittest
import subprocess
from io import StringIO

# devs: change this to 'soln.echo' to run this suite against the solution
PKG_NAME = 'echo'


class Capturing(list):
    """Context Mgr helper for capturing stdout from a function call"""

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


def run_capture(pyfile, args=()):
    """
    Runs a python program in a separate process,
    returns stdout and stderr outputs as 2-tuple
    """
    cmd = ["python", pyfile]
    cmd.extend(args)
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = p.communicate()
    stdout = stdout.decode().splitlines()
    stderr = stderr.decode().splitlines()
    assert stdout or stderr, "The program is not printing any output"
    return stdout, stderr


class TestEcho(unittest.TestCase):
    """Main test fixture for 'echo' module"""
    @classmethod
    def setUpClass(cls):
        """Performs module import and suite setup at test-runtime"""
        # check for python3
        cls.assertGreaterEqual(cls, sys.version_info[0], 3)
        # This will import the module to be tested
        cls.module = importlib.import_module(PKG_NAME)
        # Make a dictionary of each function in the student's test module
        cls.funcs = {
            k: v for k, v in inspect.getmembers(
                cls.module, inspect.isfunction
            )
        }
        # check the module for required functions
        assert "main" in cls.funcs, "Missing required function main()"
        assert "create_parser" in cls.funcs, "Missing required function create_parser()"

    def setUp(self):
        pass

    def test_parser(self):
        result = self.module.create_parser()
        self.assertIsInstance(
            result, argparse.ArgumentParser,
            "create_parser() function is not returning a parser object")

    def test_help(self):
        process = subprocess.Popen(
            ["python", "./echo.py", "-h"],
            stdout=subprocess.PIPE
        )
        stdout, _ = process.communicate()
        with open('USAGE') as f:
            usage = f.read()
        self.assertEqual(stdout.decode(), usage)

    def test_echo(self):
        stdout, stderr = run_capture(self.module.__file__)

    def test_simple_echo(self):
        args = ['Was soll die ganze Aufregung?']
        stdout, stderr = run_capture(self.module.__file__, args)
        self.assertEqual(
            stdout[0], args[0],
            "The program is not performing simple echo"
        )

    def test_lower_short(self):
        args = ["-l", "HELLO WORLD"]
        with Capturing() as output:
            self.module.main(args)
        assert output, "The program did not print anything."
        self.assertEqual(output[0], "hello world")

    def test_lower_long(self):
        args = ["--lower", "HELLO WORLD"]
        with Capturing() as output:
            self.module.main(args)
        assert output, "The program did not print anything."
        self.assertEqual(output[0], "hello world")

    def test_upper_short(self):
        args = ["-u", "hello world"]
        with Capturing() as output:
            self.module.main(args)
        assert output, "The program did not print anything."
        self.assertEqual(output[0], "HELLO WORLD")

    def test_upper_long(self):
        args = ["--upper", "hello world"]
        with Capturing() as output:
            self.module.main(args)
        assert output, "The program did not print anything."
        self.assertEqual(output[0], "HELLO WORLD")

    def test_title_short(self):
        args = ["-t", "hello world"]
        with Capturing() as output:
            self.module.main(args)
        assert output, "The program did not print anything."
        self.assertEqual(output[0], "Hello World")

    def test_title_long(self):
        args = ["--title", "hello world"]
        with Capturing() as output:
            self.module.main(args)
        assert output, "The program did not print anything."
        self.assertEqual(output[0], "Hello World")

    def test_no_options(self):
        args = ["hello world"]
        with Capturing() as output:
            self.module.main(args)
        assert output, "The program did not print anything."
        self.assertEqual(output[0], "hello world")

    def test_all_options(self):
        args = ["-tul", "hEllo wORld"]
        with Capturing() as output:
            self.module.main(args)
        assert output, "The program did not print anything."
        self.assertEqual(output[0], "Hello World")


if __name__ == '__main__':
    unittest.main()
