#!/usr/bin/env python3
from sys import stdin
from runtime import Runtime

from tokenizer import Tokenizer
from parser import Parser


def main():
    runtime = Runtime()
    # i = ''
    # while True:
    #     try:
    #         i = input('Stmt: ')
    #     except KeyboardInterrupt:
    #         print('     Goodbye :)')
    #         return
    #     # print('Tokens:', list(Tokenizer(i).generator()))
    #     parser = Parser(Tokenizer(i).generator())
    #     tree = parser.parse()
    #     if tree is None:
    #         print('Error')
    #     else:
    #         print('Tree:', str(tree))
    #         print('Result:', tree.eval(runtime))
    with open('test.cl', 'r') as file:
        for statement in file.readlines():
            parser = Parser(Tokenizer(statement).generator())
            tree = parser.parse()
            if tree is not None:
                print(tree.eval(runtime))


if __name__ == '__main__':
    main()
