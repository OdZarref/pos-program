from os.path import isfile
from libs.jsonlibs import *
from libs.etc import *

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

def primeiraInicialização():
    if not isfile('produtos.json'): open('produtos.json', 'w').write('{}')
    if not isfile('vendas.json'): open('vendas.json', 'w').write('[]')
    if not isfile('caixa.json'): open('caixa.json', 'w').write('{"status": false, "historico": [], "valor": 0}')

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

class Caixa:
    def __init__(self):
        self.caixa = abrirJson('caixa.json')

    def vender(self):
        def salvarVenda(self):
            from datetime import datetime

            vendas = abrirJson('vendas.json')

            dataVenda = dict()
            dataVenda['ano'] = datetime.now().year
            dataVenda['mes'] = datetime.now().month
            dataVenda['dia'] = datetime.now().day
            dataVenda['hora'] = datetime.now().hour
            dataVenda['minuto'] = datetime.now().minute
            dataVenda['segundo'] = datetime.now().second
            venda = list()
            venda.append(produtosAVender)
            venda.append(dataVenda)

            vendas.append(venda)

            editarJson('vendas.json', vendas)

        def modificarEstoque(self):
            for produto in produtosAVender:
                produtosEstoque[produto['idProdutoAVender']]['quantidade'] = produtosEstoque[produto['idProdutoAVender']]['quantidade'] - produto['quantidadeAVender']
                editarJson('produtos.json', produtosEstoque)

            
        produtosEstoque = abrirJson('produtos.json')
        produtosAVender = list()

        while True:
            produtoAVender = dict()
            mostrarProdutos(produtosEstoque)
        
            while True:
                produtoAVender['nomeProdutoAVender'] = str(input('Qual produto adicionará?\n'))
                idProdutoAVender = verificarCadastroProduto(produtosEstoque, produtoAVender['nomeProdutoAVender'])[-1]
                if idProdutoAVender: break
                else: print('Produto Inválido!')

            produtoAVender['idProdutoAVender'] = idProdutoAVender
            produtoAVender['quantidadeAVender'] = receberInteiro('Quantidade: ')
            produtosAVender.append(produtoAVender)
            
            escolhaVenda = str(input('Deseja adicionar mais produtos? ')).strip().lower()

            if 's' not in escolhaVenda: break
        total = float()

        for produto in produtosAVender:
            nomeProduto = produtosEstoque[produto["idProdutoAVender"]]['nome']
            precoProduto = produtosEstoque[produto['idProdutoAVender']]['precoDeVenda']
            print(f'Produto: {nomeProduto} {("-" * (40 - len(nomeProduto)))} | Preço: {precoProduto} {"-" * 36} | Quantidade: {produto["quantidadeAVender"]} {"-" * 38}')
            total += precoProduto * produto['quantidadeAVender']
        
        print(f'Total: {total}')

        escolha = receberInteiro('O que deseja fazer? [ 1 ] Finalizar Venda | [ 0 ] Cancelar Venda')

        if escolha == 1:
            self.vender().modificarEstoque()
            self.vender().salvarVenda()
            print('Venda Finalizada')

    def abrirFecharCaixa(self, status=True):
        self.caixa['status'] = status
        editarJson('caixa.json', self.caixa)

    def verificarCaixaAbertoFechado(self):
        if self.caixa['status']: return True

    def inserirRetirarValor(self):
        escolha = receberInteiro('O que deseja fazer? [ 1 ] Inserir [ 2 ] Retirar [ 0 ]')

        if escolha == 1:
            quantidadeAInserir = receberInteiro('Quantidade a retirar:\n')
            self.caixa['historico'].append({"acao": "entrada", "quantidade": quantidadeAInserir})
        elif escolha == 2:
            quantidadeARetirar = receberInteiro('Quantidade a retirar:\n')
            self.caixa['historico'].append({"acao": "retirada", "quantidade": -quantidadeARetirar})

        editarJson('caixa.json', self.caixa)

    def inserirValorVenda(self, valor):
        self.caixa['historico'].append({"acao": "venda", "quantidade": valor})
        

def editarProduto():
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
                novaQuantidade = receberInteiro('Nova Quantidade: ')
                produtos[idProduto]['quantidade'] = novaQuantidade
                editarJson('produtos.json', produtos)
                break
            elif escolhaEditar == 3:
                novoPrecoDeCompra = receberFracionario('Novo Preço de Compra:\n')
                produtos[idProduto]['precoDeCompra'] = novoPrecoDeCompra
                editarJson('produtos.json', produtos)
                break
            elif escolhaEditar == 4:
                novoPrecoDeVenda = receberFracionario('Novo Preço de Venda:\n')
                produtos[idProduto]['precoDeVenda'] = novoPrecoDeVenda
                editarJson('produtos.json', produtos)
                break
        else:
            print('Este produto não está no sistema.') 
            input('pressione enter')

if __name__ == '__main__':
    primeiraInicialização()

    while True:
        escolha = int(input('O que quer fazer? [0]Sair [1]Venda [2]Cadastrar Produto [3]Editar Produto\n'))

        if escolha == 0:
            break
        elif escolha == 1:
            caixa = Caixa()

            if not caixa.verificarCaixaAbertoFechado():
                escolha = str(input('O caixa está fechado, deseja abri-lo? [ S / N ]')).strip().lower()

                if 's' in escolha: caixa.abrirFecharCaixa()
            elif caixa.verificarCaixaAbertoFechado():
                caixa.vender()
    
        elif escolha == 2:
            cadastrarProduto()
        elif escolha == 3:
            editarProduto()
        else:
            print('OPÇÃO INVÁLIDA.')

        print('-=' * 40)