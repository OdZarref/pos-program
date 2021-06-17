from os.path import isfile
from libs.jsonlibs import *
from libs.etc import *

def primeiraInicialização():
    open('produtos.json', 'w').write('{}')

def cadastrarProduto():
    produtos = abrirJson('produtos.json')
    nome = str(input('Nome do Produto: ')).strip().lower()
    
    if nome in produtos:
        print('Produto já cadastrado. Se deseja editar, escolha a opção "Editar Produto".')
    else:
        quantidade = receberInteiro('Quantidade: ')
        precoDeCompra = receberFracionario('Preço de Compra: ')
        precoDeVenda = receberFracionario('Preço de Venda: ')
        produto = {"quantidade": quantidade, "precoDeCompra": precoDeCompra, "precoDeVenda": precoDeVenda}
        produtos[nome] = produto

        editarJson('produtos.json', produtos)
        print('Produto Cadastrado Com Sucesso!')

def vender():
    pass

def editarProduto():
    produtos = abrirJson('produtos.json')

if __name__ == '__main__':
    if not isfile('produtos.json'):
        primeiraInicialização()

    while True:
        escolha = int(input('O que quer fazer? [0]Sair [1]Venda [2]Cadastrar Produto [3]Editar Produto\n'))

        if escolha == 0:
            break
        elif escolha == 1:
            vender()
        elif escolha == 2:
            cadastrarProduto()
        elif escolha == 3:
            editarProduto()
        else:
            print('OPÇÃO INVÁLIDA.')

        print('-=' * 40)