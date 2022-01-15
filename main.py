#!/usr/bin/env python3
from sys import stdin

from tokenizer import Tokenizer
from parser import Parser


def main():
    i = ''
    while True:
        try:
            i = input('Expression: ')
        except KeyboardInterrupt:
            print('goodbye :)')
            return
        parser = Parser(i)
        tree = parser.parse()
        if tree is None:
            print('Invalid!')
        else:
            print(str(tree))
            print('=')
            print(tree.eval())
    # with open('test.cl', 'r') as file:
    #     content = file.read()
    #     parser = Parser(content)
    #     tree = parser.parse()
    #     if tree is None:
    #         print('Tree is None!')
    #     else:
    #         print(tree)


if __name__ == '__main__':
    main()
