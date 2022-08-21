#!/usr/bin/env python3
from sys import stdin, argv
from runtime import Runtime

from lexer import Lexer
from parser import Parser


def main():

    runtime = Runtime()
    while True:
        statement = input('Statement: ')
        parser = Parser(Lexer(statement).generator())
        tree = parser.parse()
        if tree is not None:
            print(statement)
            print(str(tree))
            print('>>>', tree.eval(runtime))
            print()


if __name__ == '__main__':
    main()
