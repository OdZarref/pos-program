from libs.jsonlibs import *
from libs.etc import *


class Estoque():
    def cadastrarProduto(self):
        produtos = abrirJson('produtos.json')
        nome = str(input('Nome do Produto:\n')).strip().lower()
        
        if verificarCadastroProduto(produtos, nome):
            print('Produto já cadastrado. Se deseja editar, escolha a opção "Editar Produto".')
        else:
            quantidade = receberInteiro('Quantidade:\n')
            precoDeCompra = receberFracionario('Preço de Compra:\n')
            precoDeVenda = receberFracionario('Preço de Venda:\n')
            produto = {"nome": nome, "quantidade": quantidade, "precoDeCompra": precoDeCompra, "precoDeVenda": precoDeVenda}
            
            try:
                produtos[f'{int(list(produtos)[-1]) + 1}'] = produto
            except IndexError:
                produtos['1'] = produto

            editarJson('produtos.json', produtos)
            print('Produto Cadastrado Com Sucesso!')


    def calcularValorEstoque(self):
        produtos = abrirJson('produtos.json')
        totalEstoque = 0
        potencialDeVenda = 0

        for indice in produtos:
            totalEstoque += (produtos[indice]['precoDeCompra'] * produtos[indice]['quantidade'])
            potencialDeVenda += (produtos[indice]['precoDeVenda'] * produtos[indice]['quantidade'])

        print(f'Valor em Estoque: R$ {totalEstoque:.2f}\nPotencial de Venda: R$ {potencialDeVenda:.2f}')

    def editarProduto(self):
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


class Caixa():
    def __init__(self):
        self.caixa = abrirJson('caixa.json')

    def vender(self):
        def salvarVenda(self):
            def calcularLucroEEntrada(self):
                lucroEEntrada = dict()
                totalEntrada = 0
                totalLucro = 0
                
                for produto in produtosAVender:
                    precoDeCompra = produtosEstoque[f'{produto["idProdutoAVender"]}']['precoDeCompra']
                    precoDeVenda = produtosEstoque[f'{produto["idProdutoAVender"]}']['precoDeVenda']
                    quantidade = produto['quantidadeAVender']
                    totalEntrada += (precoDeVenda * quantidade)
                    totalLucro += (precoDeVenda * quantidade) - (precoDeCompra * quantidade)
                
                lucroEEntrada['lucro'] = totalLucro
                lucroEEntrada['entrada'] = totalEntrada

                return lucroEEntrada


            from datetime import datetime

            vendas = abrirJson('vendas.json')

            dataVenda = dict()
            dataVenda['ano'] = datetime.now().year
            dataVenda['mes'] = datetime.now().month
            dataVenda['dia'] = datetime.now().day
            dataVenda['hora'] = datetime.now().hour
            dataVenda['minuto'] = datetime.now().minute
            dataVenda['segundo'] = datetime.now().second
            EntradaELucro = calcularLucroEEntrada(self)
            venda = list()
            venda.append(EntradaELucro)
            venda.append(produtosAVender)
            venda.append(dataVenda)

            vendas.append(venda)

            editarJson('vendas.json', vendas)

        def modificarEstoque(self):
            for produto in produtosAVender:
                produtosEstoque[produto['idProdutoAVender']]['quantidade'] = produtosEstoque[produto['idProdutoAVender']]['quantidade'] - produto['quantidadeAVender']
                editarJson('produtos.json', produtosEstoque)

        def historicoVenda(self, valor):
            self.caixa['historico'].append({"acao": "venda", "quantidade": valor})
            self.caixa['valor'] += valor
            editarJson('caixa.json', self.caixa)
    
        produtosEstoque = abrirJson('produtos.json')
        produtosAVender = list()

        while True:
            produtoAVender = dict()
            mostrarProdutos(produtosEstoque)
        
            while True:
                produtoAVender['nomeProdutoAVender'] = str(input('Qual produto adicionará? [ 0 ] Sair\n')).strip().lower()
                try:
                    idProdutoAVender = verificarCadastroProduto(produtosEstoque, produtoAVender['nomeProdutoAVender'])[-1]
                    limparConsole()
                    break
                except TypeError:
                    if produtoAVender['nomeProdutoAVender'] == '0': break
                    else:
                        limparConsole()
                        print('Produto inválido, tente novamente.')

            if produtoAVender['nomeProdutoAVender'] == '0': break

            produtoAVender['idProdutoAVender'] = idProdutoAVender
            produtoAVender['quantidadeAVender'] = receberInteiro('Quantidade: ')
            produtosAVender.append(produtoAVender)
            
            escolhaVenda = str(input('Deseja adicionar mais produtos? [ S / N ]\n')).strip().lower()
            limparConsole()

            if 's' not in escolhaVenda: break

        total = float()

        for produto in produtosAVender:
            nomeProduto = produtosEstoque[produto["idProdutoAVender"]]['nome']
            precoProduto = produtosEstoque[produto['idProdutoAVender']]['precoDeVenda']
            print(f'Produto: {nomeProduto} {("-" * (40 - len(nomeProduto)))} | Preço: {precoProduto} {"-" * 36} | Quantidade: {produto["quantidadeAVender"]} {"-" * 38}')
            total += precoProduto * produto['quantidadeAVender']
        
        print(f'Total: {total}')

        escolha = receberInteiro('O que deseja fazer? [ 1 ] Finalizar Venda | [ 0 ] Cancelar Venda\n')

        if escolha == 1:
            modificarEstoque(self)
            salvarVenda(self)
            historicoVenda(self, total)
            print('Venda Finalizada')

    def abrirFecharCaixa(self, status=True):
        if status:
            valorCaixa = float(input('Qual o valor do caixa?\n'))
            self.caixa['valor'] = valorCaixa

        self.caixa['status'] = status
        editarJson('caixa.json', self.caixa)

    def verificarCaixaAbertoFechado(self):
        if self.caixa['status']: return True
    
    def consultarCaixa(self):
        print(f'Valor em Caixa: {self.caixa["valor"]:.2f}')

    def inserirRetirarValor(self):
        def receberValorAtualCaixa(self):
            return self.caixa['valor']

        escolha = receberInteiro('O que deseja fazer? [ 1 ] Inserir [ 2 ] Retirar [ 0 ] Sair')
        valorCaixa = receberValorAtualCaixa(self)

        if escolha == 1:
            quantidadeAInserir = receberFracionario('Quantidade a inserir:\n')
            self.caixa['historico'].append({'acao': 'insercao', 'quantidade': quantidadeAInserir})
            self.caixa['valor'] = valorCaixa + quantidadeAInserir
        elif escolha == 2:
            quantidadeARetirar = receberInteiro('Quantidade a retirar:\n')
            motivo = str(input('Qual o motivo da retirada? '))
            self.caixa['historico'].append({'acao': 'retirada', 'quantidade': quantidadeARetirar, 'motivo': motivo})
            self.caixa['valor'] = valorCaixa - quantidadeARetirar

        editarJson('caixa.json', self.caixa)

    def modificarCaixa(self, valorCaixa):
        self.caixa['valor'] = valorCaixa
        editarJson('caixa.json', self.caixa)


class Relatorio():
    def calcularRelatorio(self, opcao, dataEspecifica=None):         
        from datetime import datetime

        dataHoje = datetime.now()
        vendas = abrirJson('vendas.json')
        lucro = 0
        entrada = 0

        for venda in vendas:
            if opcao == 'dia':
                if venda[2]['ano'] == dataHoje.year and venda[2]['mes'] == dataHoje.month and venda[2]['dia'] == dataHoje.day:
                    lucro += venda[0]['lucro']
                    entrada += venda[0]['entrada']
            elif opcao == 'semana':
                if venda[2]['ano'] == dataHoje.year and venda[2]['mes'] == dataHoje.month and venda[2]['dia'] > dataHoje.day - 7:
                    lucro += venda[0]['lucro']
                    entrada += venda[0]['entrada']
            elif opcao == 'mes':
                if venda[2]['ano'] == dataHoje.year and venda[2]['mes'] == dataHoje.month:
                    lucro += venda[0]['lucro']
                    entrada += venda[0]['entrada']
            elif opcao == 'ano':
                if venda[2]['ano'] == dataHoje.year:
                    lucro += venda[0]['lucro']
                    entrada += venda[0]['entrada']
            elif opcao == 'especifico':
                if venda[2]['ano'] == dataEspecifica['ano'] and venda[2]['mes'] == dataEspecifica['mes'] and venda[2]['dia'] == dataEspecifica['dia']:
                    lucro += venda[0]['lucro']
                    entrada += venda[0]['entrada']

        print(f'Lucro: {lucro}\nEntrada no Caixa: {entrada}')


if __name__ == '__main__':
    primeiraInicialização()

    while True:
        escolha = receberInteiro('O que quer fazer? [1]Venda e Caixa [2]Estoque [3]Relatório [0]Sair\n')
        limparConsole()

        if escolha == 0: break
        elif escolha == 1:
            caixa = Caixa()
            escolha = receberInteiro('[0] Sair [1]Venda [2]Editar Caixa\n')
            limparConsole()

            if escolha == 1:
                if not caixa.verificarCaixaAbertoFechado():
                    print('O caixa está fechado. É necessário abri-lo.')
                    caixa.abrirFecharCaixa()
                caixa.vender()
            elif escolha == 2:
                escolha = receberInteiro('[1]Consultar Caixa [2]Inserir ou Retirar Valor do Caixa [3]Editar Valor do Caixa [0]Sair\n')
                limparConsole()

                if escolha == 1: caixa.consultarCaixa()
                elif escolha == 2: caixa.inserirRetirarValor()
                elif escolha == 3:
                    novoValorCaixa = float(input('Novo Valor Caixa:\n'))
                    caixa.modificarCaixa(novoValorCaixa)
                    
        elif escolha == 2:
            estoque = Estoque()
            escolha = receberInteiro('[0]Sair [1]CadasTrar Produto [2]Editar Produto [3]Conferir Valor em Estoque\n')
            if escolha == 1: estoque.cadastrarProduto()
            elif escolha == 2: estoque.editarProduto()
            elif escolha == 3: estoque.calcularValorEstoque()
            
        elif escolha == 3:
            escolha = receberInteiro('[0]Sair [1]Relatório do Dia [2]Relatório da Semana [3]Relatório do Mês [4]Relatório do Ano\n')
            relatorio = Relatorio()

            if escolha == 1: relatorio.calcularRelatorio('dia')
            elif escolha == 2: relatorio.calcularRelatorio('semana')
            elif escolha == 3: relatorio.calcularRelatorio('mes')
            elif escolha == 4: relatorio.calcularRelatorio('ano')
            elif escolha == 5:
                dados = str(input('Data: dd/mm/aaaa')).split()
                dataEspecifica = dict()
                dataEspecifica['dia'] = int(dados[0])
                dataEspecifica['mes'] = int(dados[1])
                dataEspecifica['ano'] = int(dados[-1])
                print(dataEspecifica)
                relatorio.calcularRelatorio('especifico', dataEspecifica)

        else: print('OPÇÃO INVÁLIDA.')

        print('-=' * 40)
