from parser import Parser


def main():
    with open('test/math.txt', 'r') as file:
        for expression in file.readlines():
            tree = Parser(expression).parse()
            if tree is None:
                print(f'Failed to parse: {expression}')
            else:
                # print('Passed', str(tree), tree.eval())
                print('Passed')


if __name__ == '__main__':
    main()
