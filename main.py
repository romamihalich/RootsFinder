import sympy as sp
from polynomial import Polynomial
from functions import get_result, find_roots
from sys import exit

def read_coefs():
    coefs = input().split(',')
    return [sp.parsing.sympy_parser.parse_expr(coef) for coef in coefs]

def print_series(series):
    print("Последовательность Штурма:")
    for s in series:
        print(s)
    print()

def print_roots(roots):
    if len(roots["exact roots"]) > 0:
        print("Удалось найти точные корни:")
        print(", ".join([str(c) for c in roots["exact roots"]]))
        print()
    
    if len(roots["approximate roots"]) > 0:
        print("Приближенные значения корней:")
        print(", ".join([str(c) for c in roots["approximate roots"]]))
        print()

def main():
    #coefs = [1, 0, -5, 0, 0, -1, 0]
    print("Введите коэфициенты многочлена(через запятую): ")
    coefs = read_coefs()
    f = Polynomial(coefs)
    print(f, "\n")

    if f.deg == 0:
        print("Корней нет")
        exit()

    if f.deg == -1:
        print("Корень - любое число")
        exit()    

    result, series = get_result(f)

    roots = False
    if "zero" in result:
        roots = True
        print("Есть нулевой корень\n")

    if "pos" in result:
        roots = True
        (pos_rootcount, pos_interval) = result["pos"]
        print(f"Положительные корни({pos_rootcount}):", sp.pretty(pos_interval), sep="\n")
        print()

    if "neg" in result:
        roots = True
        (neg_rootcount, neg_interval) = result["neg"]
        print(f"Отрицательные корни({neg_rootcount}): ", sp.pretty(neg_interval), sep="\n")

    if roots == False:
        print("Корней нет")

    commands = {
        "q" : lambda: exit(),
        "r" : lambda: main(),
        "s" : lambda: print_series(series),
        "f" : lambda digits: print_roots(find_roots(result, series, digits))
    }
    print(
        "\nq - quit" 
        "\nr - restart" 
        "\ns - вывести последовательность Штурма"
        "\nf n - найти приближенные значения корней с точностью до n знаков после запятой\n"
    )
    while True:
        inp = input("enter command:")
        print()
        if inp in commands:
            commands[inp]()
        elif len(inp) > 0 and inp[0] in commands:
            digits = int(inp[1:])
            commands[inp[0]](digits)
        else:
            print("wrong command")


if __name__ == "__main__":
    main()