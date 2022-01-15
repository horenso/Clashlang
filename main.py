#!/usr/bin/env python3
from sys import stdin

from tokenizer import Tokenizer
from parser import Parser


def main():
    with open('test.cl', 'r') as file:
        content = file.read()
        parser = Parser(content)
        print(parser.parse())


if __name__ == '__main__':
    main()
