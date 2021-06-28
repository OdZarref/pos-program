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

def primeiraInicialização():
    from os.path import isfile

    if not isfile('produtos.json'): open('produtos.json', 'w').write('{}')
    if not isfile('vendas.json'): open('vendas.json', 'w').write('[]')
    if not isfile('caixa.json'): open('caixa.json', 'w').write('{"status": false, "historico": [], "valor": 0}')

def mostrarProdutos(produtosDicionario):
    contador = 0
    for indice in produtosDicionario:
        contador += 1
        nome = produtosDicionario[indice]['nome']
        print(nome.capitalize() + ' ' + ('-' * (40 - len(nome))) + ' | ', end='')

        if contador % 3 == 0:
            print('\n')

    print('\n')

def verificarCadastroProduto(produtos, nome):
    for chave in produtos:
        if produtos[chave]['nome'] == nome:
            return [True, chave]