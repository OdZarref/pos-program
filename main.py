from os.path import isfile
from libs.jsonlibs import *
from libs.etc import *

def verificarCadastroProduto(produtos, nome):
    for chave in produtos:
        if produtos[chave]['nome'] == nome:
            return [True, chave]

def primeiraInicialização():
    open('produtos.json', 'w').write('{}')

def cadastrarProduto():
    produtos = abrirJson('produtos.json')
    nome = str(input('Nome do Produto:\n')).strip().lower()
    
    if verificarCadastroProduto(produtos, nome):
        print('Produto já cadastrado. Se deseja editar, escolha a opção "Editar Produto".')
    else:
        quantidade = receberInteiro('Quantidade:\n')
        precoDeCompra = receberFracionario('Preço de Compra:\n')
        precoDeVenda = receberFracionario('Preço de Venda:\n')
        produto = {"nome": nome, "quantidade": quantidade, "precoDeCompra": precoDeCompra, "precoDeVenda": precoDeVenda}
        produtos[f'{int(list(produtos)[-1]) + 1}'] = produto

        editarJson('produtos.json', produtos)
        print('Produto Cadastrado Com Sucesso!')

def vender():
    pass

def editarProduto():
    def mostrarProdutos(produtosDicionario):
        contador = 0
        for indice in produtosDicionario:
            contador += 1
            nome = produtosDicionario[indice]['nome']
            print(nome.capitalize() + ('-' * (40 - len(nome))) + ' | ', end='')

            if contador % 3 == 0:
                print('\n')

        print('\n')
    
    def mostrarProdutoOpcoes(produto):
        print(f'[ 1 ] Nome: {produto["nome"]}| [ 2 ] Quantidade: {produto["quantidade"]} | [ 3 ] Preço de Compra: {produto["precoDeCompra"]} | [ 4 ] Preço de Venda: {produto["precoDeVenda"]} | [ 0 ] Sair \n')

    produtos = abrirJson('produtos.json')

    while True:
        mostrarProdutos(produtos)
        produtoParaEditar = str(input('Qual produto deseja editar?\n'))
        idProduto = verificarCadastroProduto(produtos, produtoParaEditar)[-1]

        if idProduto:
            mostrarProdutoOpcoes(produtos[idProduto])
            escolhaEditar = receberInteiro('O que deseja editar?\n')

            if escolhaEditar == 0:
                break
            elif escolhaEditar == 1:
                novoNome = str(input('Novo nome:\n'))
                produtos[idProduto]['nome'] = novoNome
                editarJson('produtos.json', produtos)
                break
            elif escolhaEditar == 2:
                pass
            elif escolhaEditar == 3:
                pass
            elif escolhaEditar == 4:
                pass
        else:
            print('Este produto não está no sistema.') 
            input('pressione enter')

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