from parser import Parser


def main():
    with open('test/math.txt', 'r') as file:
        for expression in file.readlines():
            parser = Parser(expression)
            if parser.parse():
                print('Passed')
            else:
                print(f'Failed to parse: {expression}')


if __name__ == '__main__':
    main()
