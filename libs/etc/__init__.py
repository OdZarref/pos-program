def receberString():
    pass
def receberInteiro(texto):
    while True:
        try:
            inteiro = int(input(texto))
            return inteiro
        except ValueError:
            print('DIGITE UM VALOR NUMÉRICO!')
def receberFracionario(texto):
    while True:
        try:
            fracionario = float(input(texto).replace(',', '.'))
            return fracionario
        except ValueError:
            print('VALOR INVÁLIDO!')

def limparConsole():
    from os import system

    system('cls')