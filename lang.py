from tokenizer import Tokenizer


def main():
    for t in Tokenizer(input('Expression: ')).parse():
        print(t)


if __name__ == '__main__':
    main()


# Grammar:
# expr   -> factor
# factor -> (factor)
# factor -> term * term
# factor -> term
# term   -> num + num
# term   -> num

# 3 + 1232 * ((21 + 21) * 2)

#      (+)  expr -> factor -> term
#     /  \
#    3   (*)
#         |
#        (*)
#    /  \   \
#   21  21
#
