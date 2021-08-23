import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox
from libs.jsonlibs import *
from datetime import datetime


class EventosBotoes():
    def eventoTreeViewDoubleClick(self, event):
        for indice in self.varTreeView.selection():
            self.frameEditarProduto(self.varTreeView.item(indice, 'values'))

    def hoverBotaoVendas(self, event):
        self.botaoVendasImagemD = tk.PhotoImage(file='images\sellD.png')
        self.botaoVendas.configure(image=self.botaoVendasImagemD)

    def leaveBotaoVendas(self, event):
        self.botaoVendasImagemL = tk.PhotoImage(file='images\sellL.png')
        self.botaoVendas.configure(image=self.botaoVendasImagemL)

    def hoverBotaoEstoque(self, event):
        self.botaoEstoqueImagemD = tk.PhotoImage(file='images\estoqueD.png')
        self.botaoEstoque.configure(image=self.botaoEstoqueImagemD)

    def leaveBotaoEstoque(self, event):
        self.botaoEstoqueImagemL = tk.PhotoImage(file='images\estoqueL.png')
        self.botaoEstoque.configure(image=self.botaoEstoqueImagemL)

    def hoverBotaoCaixa(self, event):
        self.botaoCaixaImagemD = tk.PhotoImage(file='images\caixaD.png')
        self.botaoCaixa.configure(image=self.botaoCaixaImagemD)

    def leaveBotaoCaixa(self, event):
        self.botaoCaixaImagemL = tk.PhotoImage(file='images\CaixaL.png')
        self.botaoCaixa.configure(image=self.botaoCaixaImagemL)

    def hoverBotaoRelatorio(self, event):
        self.botaoRelatorioImagemD = tk.PhotoImage(file='images\elatorioD.png')
        self.botaoRelatorio.configure(image=self.botaoRelatorioImagemD)

    def leaveBotaoRelatorio(self, event):
        self.botaoRelatorioImagemL = tk.PhotoImage(file='images\elatorioL.png')
        self.botaoRelatorio.configure(image=self.botaoRelatorioImagemL)


class EntryPlaceHolder(tk.Entry):
    def __init__(self, master=None, placeholder='', bg='white', highlightbackground=None, highlightthickness=0, fg=None):
        super().__init__(master, bg=bg, highlightbackground=highlightbackground,
                         highlightthickness=highlightthickness, fg=fg)

        self.placeHolder = placeholder
        self.inserirPlaceHolder()
        self.bind('<Button-1>', self.limparEntry)

    def inserirPlaceHolder(self):
        self.insert(0, self.placeHolder)

    def limparEntry(self, event):
        self.delete(0, tk.END)
        self.unbind('<Button-1>')


class BancoDeDados():
    def modificarDescricaoBancoDeDados(self, novaDescricao, descricaoAntiga):
        self.cursor.execute(
            f'UPDATE Produtos SET descricao="{novaDescricao}" WHERE descricao="{descricaoAntiga}"')
        self.bancoDeDados.commit()

    def procurarNoBancoDeDados(self, chave1, chave2, valor1):
        self.cursor.execute(
            f'SELECT {str(chave2)} FROM Produtos WHERE {str(chave1)} = "{str(valor1)}"')

        if chave2 == 'descricao':
            valor = str(*self.cursor.fetchone())
        elif chave2 == 'estoque' or chave2 == 'estoqueMinimo':
            valor = int(*self.cursor.fetchone())
        else:
            valor = float(*self.cursor.fetchone())

        return valor

    def modificarPrecoDeCustoBancoDeDados(self, novoPrecoDeCusto, descricaoAntiga):
        self.cursor.execute(
            f'UPDATE Produtos SET precoDeCusto="{novoPrecoDeCusto}" WHERE descricao="{descricaoAntiga}"')
        self.bancoDeDados.commit()

    def modificarPrecoDeVendaBancoDeDados(self, novoPrecoDeVenda, descricaoAntiga):
        self.cursor.execute(
            f'UPDATE Produtos SET precoDeVenda="{novoPrecoDeVenda}" WHERE descricao="{descricaoAntiga}"')
        self.bancoDeDados.commit()

    def modificarEstoqueBancoDeDados(self, novoEstoque, descricaoAntiga):
        self.cursor.execute(
            f'UPDATE Produtos SET estoque="{novoEstoque}" WHERE descricao="{descricaoAntiga}"')
        self.bancoDeDados.commit()

    def modificarEstoqueMinimoBancoDeDados(self, novoEstoqueMinimo, descricaoAntiga):
        self.cursor.execute(
            f'UPDATE Produtos SET estoque="{novoEstoqueMinimo}" WHERE descricao="{descricaoAntiga}"')
        self.bancoDeDados.commit()

    def conectarBancoDeDados(self):
        self.bancoDeDados = sqlite3.connect('Produtos.db')
        self.cursor = self.bancoDeDados.cursor()

    def desconectarBancoDeDados(self):
        self.bancoDeDados.close()

    def montaTabelasEstoque(self):
        self.conectarBancoDeDados()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Produtos (
                codigo INTEGER PRIMARY KEY,
                descricao CHAR(40) NOT NULL,
                precoDeCusto FLOAT,
                precoDeVenda FLOAT,
                menorPreco FLOAT,
                ultimoPreco FLOAT,
                estoque INTEGER,
                estoqueMinimo INTEGER
            );
        """)
        self.bancoDeDados.commit()

    def montaTabelasVendas(self):
        self.conectarBancoDeDados()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas (
                codigo INTEGER PRIMARY KEY,
                descricao CHAR(40) NOT NULL,
                precoDeCusto FLOAT,
                precoDeVenda FLOAT,
                menorPreco FLOAT,
                ultimoPreco FLOAT,
                estoque INTEGER,
                estoqueMinimo INTEGER
            );
        """)
        self.bancoDeDados.commit()


class FuncoesGerais():
    def salvarVenda(self, produtos):
        data = datetime.now()
        lucroTotal = 0
        vendas = abrirJson('vendas.json')
        venda = dict()
        venda['data'] = {'segundo': data.second, 'minuto': data.minute,
                         'hora': data.hour, 'dia': data.day, 'mes': data.month, 'ano': data.year}
        venda['produtos'] = list()

        for produto in produtos:
            nome = produto[0]
            precoDeCusto = self.procurarNoBancoDeDados(
                'descricao', 'precoDeCusto', nome)
            precoDeVenda = float(produto[2])
            quantidade = int(produto[1])
            lucro = (precoDeVenda - precoDeCusto) * quantidade
            lucro = float(f'{lucro:.2f}')
            lucroTotal += lucro
            venda['produtos'].append(
                {'nome': nome, 'quantidade': quantidade, 'lucro': lucro})

        venda['lucro'] = float(f'{lucroTotal:.2f}')
        vendas.append(venda)
        editarJson('vendas.json', vendas)

    def atualizarBancoDeDados(self, produtos):
        for produto in produtos:
            quantidadeEstoque = self.procurarNoBancoDeDados(
                'descricao', 'estoque', produto[0])
            novaQuantidade = quantidadeEstoque - produto[1]
            self.cursor.execute(
                f'UPDATE Produtos SET estoque={novaQuantidade} WHERE descricao="{produto[0]}"')
            self.bancoDeDados.commit()

    def adicionarProdutoCarrinho(self):
        def buscarPrecoProduto(self, descricaoProduto):
            self.cursor.execute(
                f'SELECT precoDeVenda from Produtos WHERE descricao="{descricaoProduto}"')
            return self.cursor.fetchone()

        def atualizarTreeViewEEntryTotal(self):
            self.varTreeView.insert('', tk.END, values=(
                descricaoProduto, quantidade, preco))

            if self.varTreeView.get_children():
                total = 0
                for item in self.varTreeView.get_children():
                    contador = 0
                    for valor in self.varTreeView.item(item)['values']:
                        contador += 1
                        if contador == 2:
                            quantidadeTreeView = valor
                        if contador == 3:
                            precoTreeView = valor

                    total += (quantidadeTreeView * float(precoTreeView))

                totalCarrinho = self.labelTotal.cget('text')
                if totalCarrinho != 'Total: ':
                    totalCarrinho = float(totalCarrinho.replace('Total: ', ''))
                else:
                    totalCarrinho = 0
                totalCarrinho = total
                self.labelTotal.configure(text='Total: ' + str(totalCarrinho))

        descricaoProduto = self.entryDescricao.get().strip().lower()
        quantidade = self.entryQuantidade.get()
        preco = buscarPrecoProduto(self, descricaoProduto)

        if self.validarEntryInt(quantidade):
            self.entryQuantidade.configure(highlightbackground=self.color1)
        else:
            self.entryQuantidade.configure(
                highlightbackground='#ff0000')  # , highlightthickness=2

        if self.validarExistenciaDeProduto(descricaoProduto):
            self.entryDescricao.configure(highlightbackground=self.color1)
        else:
            self.entryDescricao.configure(highlightbackground='#ff0000')

        if self.validarEntryInt(quantidade) and self.validarExistenciaDeProduto(descricaoProduto):
            atualizarTreeViewEEntryTotal(self)

        self.root.focus()

    def limparCarrinho(self):
        for item in self.varTreeView.get_children():
            self.varTreeView.delete(item)

    def concluirVenda(self):
        produtos = list()

        if self.varTreeView.get_children():
            for item in self.varTreeView.get_children():
                produto = list()
                for valor in self.varTreeView.item(item)['values']:
                    produto.append(valor)
                produtos.append(produto)

            self.atualizarBancoDeDados(produtos)
            self.salvarVenda(produtos)
            self.limparCarrinho()
            messagebox.showinfo('Info', 'VENDA CONCLUÍDA')

    def criarJson(self):
        from os.path import isfile

        if not isfile('vendas.json'):
            open('vendas.json', 'w').write('[]')

    def destruirFilhos(self, pais):
        for pai in pais:
            for filho in pai.winfo_children():
                filho.destroy()

    def adicionarProduto(self):
        descricao = self.cadastroEntryDescricao.get()
        self.root.focus()
        print(self.validarExistenciaDeProduto(descricao))
        if self.validarExistenciaDeProduto(descricao):
            messagebox.showwarning('Info', 'Este produto já está cadastrado.')
        else:
            quantidade = self.cadastroEntryQuantidade.get()
            precoDeCusto = self.cadastroEntryPrecoDeCusto.get()
            precoDeVenda = self.cadastroEntryPrecoDeVenda.get()
            menorPreco = precoDeCusto
            ultimoPreco = precoDeCusto
            estoqueMinimo = self.cadastroEntryEstoqueMinimo.get()
            self.cursor.execute(""" INSERT INTO Produtos (descricao, precoDeCusto, precoDeVenda, menorPreco, ultimoPreco, Estoque, EstoqueMinimo)
            VALUES (?, ?, ?, ?, ?, ?, ?) """, (descricao, precoDeCusto, precoDeVenda, menorPreco, ultimoPreco, quantidade, estoqueMinimo))
            self.bancoDeDados.commit()
            messagebox.showinfo('Info', 'Produto cadastrado com sucesso.')

    def editarProduto(self, event):
        novaDescricao = self.entryEditarDescricao.get().strip().lower()
        novoPrecoDeCusto = self.entryEditarPrecoDeCusto.get().strip().lower().replace(',', '.')
        novoPrecoDeVenda = self.entryEditarPrecoDeVenda.get().strip().lower().replace(',', '.')
        novoEstoque = self.entryEditarEstoque.get().strip().lower()
        novoEstoqueMinimo = self.entryEditarEstoqueMinimo.get().strip().lower()

        for c in self.varTreeView.get_children():
            descricaoAntiga = self.varTreeView.item(c)['values'][0]

        if novaDescricao and novaDescricao != 'nova descrição':
            self.modificarDescricaoBancoDeDados(novaDescricao, descricaoAntiga)

        if novoPrecoDeCusto and novoPrecoDeCusto != 'novo preço de custo':
            novoPrecoDeCusto = float(novoPrecoDeCusto.replace(',', '.'))
            self.modificarPrecoDeCustoBancoDeDados(
                novoPrecoDeCusto, descricaoAntiga)

        if novoPrecoDeVenda and novoPrecoDeVenda != 'novo preço de venda':
            novoPrecoDeVenda = float(novoPrecoDeVenda.replace(',', '.'))
            self.modificarPrecoDeVendaBancoDeDados(
                novoPrecoDeVenda, descricaoAntiga)

        if novoEstoque and novoEstoque != 'novo estoque':
            novoEstoque = int(novoEstoque)
            self.modificarEstoqueBancoDeDados(novoEstoque, descricaoAntiga)

        if novoEstoqueMinimo and novoEstoqueMinimo != 'novo estoque mínimo':
            novoEstoqueMinimo = int(novoEstoqueMinimo)
            self.modificarEstoqueMinimoBancoDeDados(
                novoEstoqueMinimo, descricaoAntiga)

    def selectLista(self):
        self.varTreeView.delete(*self.varTreeView.get_children())
        self.conectarBancoDeDados()
        lista = self.cursor.execute(""" SELECT descricao, precoDeCusto, precoDeVenda, menorPreco, ultimoPreco, estoque, estoqueMinimo FROM Produtos
        ORDER BY descricao ASC; """)

        for c in lista:
            self.varTreeView.insert("", tk.END, values=c)

    def validarExistenciaDeProduto(self, descricaoProduto):
        try:
            self.cursor.execute(
                f'SELECT descricao from Produtos WHERE descricao="{descricaoProduto}"')
            descricaoDataBase = str(*self.cursor.fetchone())
            if descricaoDataBase == descricaoProduto:
                return True
        except TypeError:
            pass

    def validarEntryInt(self, numero):
        try:
            if type(int(numero)) == int:
                return True
        except:
            pass


class CriarFrames():
    def frameEditarProduto(self, dadosProduto):
        def frameUtilEditarProdutoEsquerdo(self):
            self.varFrameUtilEsquerdo = tk.Frame(
                self.varFrameLateralDireito, bg=self.color2)
            self.varFrameUtilEsquerdo.place(
                relx=0.01, rely=0.04, relwidth=0.85, relheight=0.98)

            self.varTreeView = ttk.Treeview(self.varFrameUtilEsquerdo, height=3, column=(
                'coluna1', 'coluna2', 'coluna3', 'coluna4', 'coluna5', 'coluna6', 'coluna7'))
            self.varTreeView.heading('#0', text='')
            self.varTreeView.heading('#1', text='Descrição')
            self.varTreeView.heading('#2', text='Preço de Custo')
            self.varTreeView.heading('#3', text='Preço de Venda')
            self.varTreeView.heading('#4', text='Menor Preço')
            self.varTreeView.heading('#5', text='Último Preço')
            self.varTreeView.heading('#6', text='Estoque Atual')
            self.varTreeView.heading('#7', text='Estoque Mínimo')
            self.varTreeView.column('#0', width=0, stretch=tk.NO)
            self.varTreeView.column('#1', width=75, anchor=tk.CENTER)
            self.varTreeView.column('#2', width=50, anchor=tk.CENTER)
            self.varTreeView.column('#3', width=50, anchor=tk.CENTER)
            self.varTreeView.column('#4', width=50, anchor=tk.CENTER)
            self.varTreeView.column('#5', width=50, anchor=tk.CENTER)
            self.varTreeView.column('#6', width=50, anchor=tk.CENTER)
            self.varTreeView.column('#7', width=50, anchor=tk.CENTER)
            self.varTreeView.place(relx=0.01, rely=0.0,
                                   relwidth=0.95, relheight=0.08)
            self.varTreeView.insert("", tk.END, values=dadosProduto)

            self.entryEditarDescricao = EntryPlaceHolder(
                self.varFrameUtilEsquerdo, placeholder='Nova Descrição', bg=self.color2, highlightbackground=self.color1, highlightthickness=1, fg='White')
            self.entryEditarDescricao.bind('<Return>', self.editarProduto)
            self.entryEditarPrecoDeCusto = EntryPlaceHolder(
                self.varFrameUtilEsquerdo, placeholder='Novo Preço de Custo', bg=self.color2, highlightbackground=self.color1, highlightthickness=1, fg='White')
            self.entryEditarPrecoDeCusto.bind('<Return>', self.editarProduto)
            self.entryEditarPrecoDeVenda = EntryPlaceHolder(
                self.varFrameUtilEsquerdo, placeholder='Novo Preço de Venda', bg=self.color2, highlightbackground=self.color1, highlightthickness=1, fg='White')
            self.entryEditarPrecoDeVenda.bind('<Return>', self.editarProduto)
            self.entryEditarEstoque = EntryPlaceHolder(
                self.varFrameUtilEsquerdo, placeholder='Novo Estoque', bg=self.color2, highlightbackground=self.color1, highlightthickness=1, fg='White')
            self.entryEditarEstoque.bind('<Return>', self.editarProduto)
            self.entryEditarEstoqueMinimo = EntryPlaceHolder(
                self.varFrameUtilEsquerdo, placeholder='Novo Estoque Mínimo', bg=self.color2, highlightbackground=self.color1, highlightthickness=1, fg='White')
            self.entryEditarEstoqueMinimo.bind('<Return>', self.editarProduto)

            self.entryEditarDescricao.place(
                relx=0.01, rely=0.1, relwidth=0.14, relheight=0.04)
            self.entryEditarPrecoDeCusto.place(
                relx=0.01, rely=0.3, relwidth=0.14, relheight=0.04)
            self.entryEditarPrecoDeVenda.place(
                relx=0.01, rely=0.5, relwidth=0.14, relheight=0.04)
            self.entryEditarEstoque.place(
                relx=0.01, rely=0.7, relwidth=0.14, relheight=0.04)
            self.entryEditarEstoqueMinimo.place(
                relx=0.01, rely=0.9, relwidth=0.14, relheight=0.04)

        def frameUtilEditarProdutoDireito(self):
            self.varFrameUtilDireito = tk.Frame(
                self.varFrameLateralDireito, background=self.color1)
            self.varFrameUtilDireito.place(
                relx=0.87, rely=0.01, relwidth=0.12, relheight=0.98)

            self.botaoAdicionar = tk.Button(
                self.varFrameUtilDireito, text='Editar', bg=self.color3, command=self.editarProduto)
            self.botaoAdicionar.place(
                relx=0.2, rely=0.01, relwidth=0.6, relheight=0.04)

        self.destruirFilhos([self.varFrameLateralDireito])
        frameUtilEditarProdutoEsquerdo(self)
        frameUtilEditarProdutoDireito(self)

    def frameVendas(self):
        def frameVendasLateralEsquerdo(self):
            self.varFrameUtilEsquerdo = tk.Frame(
                self.varFrameLateralDireito, background=self.color2)
            self.varFrameUtilEsquerdo.place(
                relx=0.01, rely=0.01, relwidth=0.80, relheight=0.98)

            self.entryDescricao = EntryPlaceHolder(self.varFrameUtilEsquerdo, placeholder='Descrição',
                                                   bg=self.color2, highlightbackground=self.color1, highlightthickness=1, fg='White')
            self.entryDescricao.place(
                relx=0.1, rely=0.1, relwidth=0.55, relheight=0.04)

            self.entryQuantidade = EntryPlaceHolder(self.varFrameUtilEsquerdo, placeholder='Quantidade',
                                                    bg=self.color2, highlightbackground=self.color1, highlightthickness=1, fg='White')
            self.entryQuantidade.place(
                relx=0.66, rely=0.1, relwidth=0.13, relheight=0.04)

            self.adicionarProduto = tk.Button(
                self.varFrameUtilEsquerdo, text='Adicionar', bg=self.color3, command=self.adicionarProdutoCarrinho)
            self.adicionarProduto.place(
                relx=0.8, rely=0.1, relwidth=0.1, relheight=0.04)

        def frameVendaLateralDireito(self):
            self.varFrameUtilDireito = tk.Frame(
                self.varFrameLateralDireito, background=self.color1)
            self.varFrameUtilDireito.place(
                relx=0.82, rely=0.01, relwidth=0.17, relheight=0.98)

            self.varTreeView = ttk.Treeview(
                self.varFrameUtilDireito, height=3, column=('coluna1', 'coluna2', 'coluna3'))
            self.varTreeView.heading('#0', text='')
            self.varTreeView.heading('#1', text='Descrição')
            self.varTreeView.heading('#2', text='Quant...')
            self.varTreeView.heading('#3', text='Preço')
            self.varTreeView.column('#0', width=0, stretch=tk.NO)
            self.varTreeView.column(
                '#1', width=70, anchor=tk.CENTER, minwidth=70)
            self.varTreeView.column(
                '#2', width=25, anchor=tk.CENTER, minwidth=25)
            self.varTreeView.column(
                '#3', width=25, anchor=tk.CENTER, minwidth=25)
            self.varTreeView.place(relx=0.02, rely=0.01,
                                   relwidth=0.96, relheight=0.85)

            self.labelTotal = tk.Label(
                self.varFrameUtilDireito, bg=self.color1, text='Total: ', font=('Arial', 15), fg='White')
            self.labelTotal.place(
                relx=0.01, rely=0.88, relwidth=0.95, relheight=0.04)

            self.botaoFecharCompra = tk.Button(self.varFrameUtilDireito, text='Concluir', bg=self.color3,
                                               highlightbackground=self.color1, highlightthickness=1, fg='black', command=self.concluirVenda)
            self.botaoFecharCompra.place(
                relx=0.52, rely=0.94, relwidth=0.46, relheight=0.04)

            self.botaoLimparCarrinho = tk.Button(self.varFrameUtilDireito, text='Limpar', bg=self.color3,
                                                 highlightbackground=self.color1, highlightthickness=1, fg='black', command=self.limparCarrinho)
            self.botaoLimparCarrinho.place(
                relx=0.02, rely=0.94, relwidth=0.46, relheight=0.04)

        self.destruirFilhos([self.varFrameLateralDireito])
        frameVendasLateralEsquerdo(self)
        frameVendaLateralDireito(self)

    def frameEstoque(self):
        def frameEstoqueEsquerdo(self):
            self.varFrameUtilEsquerdo = tk.Frame(self.varFrameLateralDireito)
            self.varFrameUtilEsquerdo.place(
                relx=0.01, rely=0.01, relwidth=0.85, relheight=0.98)

            self.varTreeView = ttk.Treeview(self.varFrameUtilEsquerdo, height=3, column=(
                'coluna1', 'coluna2', 'coluna3', 'coluna4', 'coluna5', 'coluna6', 'coluna7'))
            self.varTreeView.heading('#0', text='')
            self.varTreeView.heading('#1', text='Descrição')
            self.varTreeView.heading('#2', text='Preço de Custo')
            self.varTreeView.heading('#3', text='Preço de Venda')
            self.varTreeView.heading('#4', text='Menor Preço')
            self.varTreeView.heading('#5', text='Último Preço')
            self.varTreeView.heading('#6', text='Estoque Atual')
            self.varTreeView.heading('#7', text='Estoque Mínimo')
            self.varTreeView.column('#0', width=0, stretch=tk.NO)
            self.varTreeView.column('#1', width=75, anchor=tk.CENTER)
            self.varTreeView.column('#2', width=50, anchor=tk.CENTER)
            self.varTreeView.column('#3', width=50, anchor=tk.CENTER)
            self.varTreeView.column('#4', width=50, anchor=tk.CENTER)
            self.varTreeView.column('#5', width=50, anchor=tk.CENTER)
            self.varTreeView.column('#6', width=50, anchor=tk.CENTER)
            self.varTreeView.column('#7', width=50, anchor=tk.CENTER)
            self.varTreeView.place(relx=0.01, rely=0.01,
                                   relwidth=0.95, relheight=0.98)
            self.varTreeView.bind('<Double-1>', self.eventoTreeViewDoubleClick)

            self.listaEstoqueScroll = tk.Scrollbar(
                self.varFrameUtilEsquerdo, orient='vertical')
            self.varTreeView.configure(yscroll=self.listaEstoqueScroll.set)
            self.listaEstoqueScroll.place(
                relx=0.96, rely=0.01, relwidth=0.03, relheight=98)

            self.selectLista()

        def frameEstoqueDireito(self):
            def calculatTotalEstoqueEPotencialDeVenda(self, escolha):
                if self.varTreeView.get_children():
                    totalEmEstoque = float()
                    potencialDeVenda = float()
                    for indice in self.varTreeView.get_children():
                        contador = 0
                        for valorItem in self.varTreeView.item(indice)['values']:
                            if contador == 1:
                                precoDeCusto = float(valorItem)
                            elif contador == 2:
                                precoDeVenda = float(valorItem)
                            elif contador == 5:
                                quantidade = int(valorItem)
                            contador += 1

                        totalEmEstoque += (precoDeCusto * quantidade)
                        potencialDeVenda += (precoDeVenda * quantidade)

                    if escolha:
                        return f'{totalEmEstoque:.2f}'
                    else:
                        return f'{potencialDeVenda:.2f}'

            self.varFrameUtilDireito = tk.Frame(
                self.varFrameLateralDireito, background=self.color1)
            self.varFrameUtilDireito.place(
                relx=0.87, rely=0.01, relwidth=0.12, relheight=0.98)

            self.botaoAdicionar = tk.Button(
                self.varFrameUtilDireito, text='Adicionar', bg=self.color3, command=self.frameAdicionarProduto)
            self.botaoAdicionar.place(
                relx=0.2, rely=0.01, relwidth=0.6, relheight=0.04)

            labelTotalEmEstoque = tk.Label(
                self.varFrameUtilDireito, text='Total Estoque: ' + calculatTotalEstoqueEPotencialDeVenda(self, 1))
            labelTotalEmEstoque.place(relx=0.08, rely=0.9, relheight=0.04)

            labelPotencialVendas = tk.Label(
                self.varFrameUtilDireito, text='Potencial Vendas: ' + calculatTotalEstoqueEPotencialDeVenda(self, 0))
            labelPotencialVendas.place(relx=0.02, rely=0.95, relheight=0.04)

        self.destruirFilhos([self.varFrameLateralDireito])
        frameEstoqueEsquerdo(self)
        frameEstoqueDireito(self)

    def frameAdicionarProduto(self):
        self.destruirFilhos([self.varFrameLateralDireito])

        self.cadastroLabelDescricao = tk.Label(
            self.varFrameLateralDireito, text='Descrição', bg=self.color2, font=1, fg='white')
        self.cadastroLabelDescricao.place(relx=0.38, rely=0.31)
        self.cadastroEntryDescricao = tk.Entry(
            self.varFrameLateralDireito, font=1)
        self.cadastroEntryDescricao.place(
            relx=0.2, rely=0.34, relwidth=0.4, relheight=0.03)

        self.cadastroLabelQuantidade = tk.Label(
            self.varFrameLateralDireito, text='Quantidade', bg=self.color2, font=1, fg='white')
        self.cadastroLabelQuantidade.place(relx=0.68, rely=0.31)
        self.cadastroEntryQuantidade = tk.Entry(
            self.varFrameLateralDireito, font=1)
        self.cadastroEntryQuantidade.place(
            relx=0.65, rely=0.34, relwidth=0.15, relheight=0.03)

        self.cadastroLabelPrecoDeCusto = tk.Label(
            self.varFrameLateralDireito, text='Preço de Custo', bg=self.color2, font=1, fg='white')
        self.cadastroLabelPrecoDeCusto.place(relx=0.25, rely=0.4)
        self.cadastroEntryPrecoDeCusto = tk.Entry(
            self.varFrameLateralDireito, font=1)
        self.cadastroEntryPrecoDeCusto.place(
            relx=0.23, rely=0.43, relwidth=0.15, relheight=0.03)

        self.cadastroLabelPrecoDeVenda = tk.Label(
            self.varFrameLateralDireito, text='Preço de Venda', bg=self.color2, font=1, fg='white')
        self.cadastroLabelPrecoDeVenda.place(relx=0.45, rely=0.4)
        self.cadastroEntryPrecoDeVenda = tk.Entry(
            self.varFrameLateralDireito, font=1)
        self.cadastroEntryPrecoDeVenda.place(
            relx=0.43, rely=0.43, relwidth=0.15, relheight=0.03)

        self.cadastroLabelEstoqueMinimo = tk.Label(
            self.varFrameLateralDireito, text='Estoque Mínimo', bg=self.color2, font=1, fg='white')
        self.cadastroLabelEstoqueMinimo.place(relx=0.65, rely=0.4)
        self.cadastroEntryEstoqueMinimo = tk.Entry(
            self.varFrameLateralDireito, font=1)
        self.cadastroEntryEstoqueMinimo.place(
            relx=0.63, rely=0.43, relwidth=0.15, relheight=0.03)

        self.cadastroLabelAdicionar = tk.Button(
            self.varFrameLateralDireito, text='Adicionar', font=1, fg=self.color1, command=self.adicionarProduto)
        self.cadastroLabelAdicionar.place(relx=0.47, rely=0.5)

    def frameCaixa(self):
        self.destruirFilhos([self.varFrameLateralDireito])

    def frameRelatorio(self):
        def calcularLucroDia():
            vendas = abrirJson('vendas.json')
            dataHoje = datetime.now()
            lucroDia = 0

            for venda in vendas:
                diaVenda = venda['data']['dia']
                mesVenda = venda['data']['mes']
                anoVenda = venda['data']['ano']

                if diaVenda == dataHoje.day and mesVenda == dataHoje.month and anoVenda == dataHoje.year:
                    lucroDia += venda['lucro']

            return lucroDia

        self.destruirFilhos([self.varFrameLateralDireito])
        lucroDia = calcularLucroDia()

        labelLucroDia = tk.Label(self.varFrameLateralDireito)
        labelLucroDia.configure(text=f'Lucro do Dia: {str(lucroDia)}', font=(
            'arial', 10), bg=self.color1, fg='white')
        labelLucroDia.place(relx=0.5, rely=0.03)


class Aplicacao(CriarFrames, FuncoesGerais, EventosBotoes, BancoDeDados):
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.montaTabelasEstoque()
        self.config()
        self.frames()
        self.criarJson()
        self.root.mainloop()

    def config(self):
        self.imagemLogo = tk.PhotoImage(file='images\logo.png')
        self.color1 = '#34343F'
        self.color2 = '#2d2d30'
        self.color3 = '#9AF995'
        self.color4 = '#1c1c1c'
        self.root.title('Selli')
        self.root.iconphoto(False, self.imagemLogo)
        self.root.iconbitmap('images\logo.ico')
        self.root.state('zoomed')
        self.root.resizable(True, True)
        self.treeViewStyle = ttk.Style(self.root)
        self.treeViewStyle.theme_use('classic')

    def frames(self):
        def frameLateralEsquerdo(self):
            def botoesLateraisEsquerdo(self):
                self.botaoVendasImagem = tk.PhotoImage(file='images\sellL.png')
                self.botaoVendas = tk.Button(self.varFrameLateralEsquerdo, image=self.botaoVendasImagem,
                                             command=self.frameVendas, bg=self.color4, highlightthickness=0, bd=0)
                self.botaoVendas.place(relx=0.24, rely=0.05)
                self.botaoVendas.bind("<Enter>", self.hoverBotaoVendas)
                self.botaoVendas.bind("<Leave>", self.leaveBotaoVendas)

                self.botaoEstoqueImagem = tk.PhotoImage(
                    file='images\estoqueL.png')
                self.botaoEstoque = tk.Button(self.varFrameLateralEsquerdo, image=self.botaoEstoqueImagem,
                                              command=self.frameEstoque, bg=self.color4, highlightthickness=0, bd=0)
                self.botaoEstoque.place(relx=0.24, rely=0.15)
                self.botaoEstoque.bind("<Enter>", self.hoverBotaoEstoque)
                self.botaoEstoque.bind("<Leave>", self.leaveBotaoEstoque)

                self.botaoCaixaImagem = tk.PhotoImage(file='images\caixaL.png')
                self.botaoCaixa = tk.Button(self.varFrameLateralEsquerdo, image=self.botaoCaixaImagem,
                                            command=self.frameCaixa, bg=self.color4, highlightthickness=0, bd=0)
                self.botaoCaixa.place(relx=0.24, rely=0.25)
                self.botaoCaixa.bind("<Enter>", self.hoverBotaoCaixa)
                self.botaoCaixa.bind("<Leave>", self.leaveBotaoCaixa)

                self.botaoRelatorioImagem = tk.PhotoImage(
                    file='images\elatorioL.png')
                self.botaoRelatorio = tk.Button(self.varFrameLateralEsquerdo, image=self.botaoRelatorioImagem,
                                                command=self.frameRelatorio, bg=self.color4, highlightthickness=0, bd=0)
                self.botaoRelatorio.place(relx=0.24, rely=0.35)
                self.botaoRelatorio.bind("<Enter>", self.hoverBotaoRelatorio)
                self.botaoRelatorio.bind("<Leave>", self.leaveBotaoRelatorio)

            self.varFrameLateralEsquerdo = tk.Frame(
                self.root, bg=self.color4, highlightbackground=self.color1, highlightthickness=4)
            self.varFrameLateralEsquerdo.place(
                relx=0.0, rely=0.0, relwidth=0.1, relheight=1)

            botoesLateraisEsquerdo(self)

        def frameLateralDireito(self):
            self.varFrameLateralDireito = tk.Frame(
                self.root, bg=self.color2, highlightbackground=self.color1, highlightthickness=4)
            self.varFrameLateralDireito.place(
                relx=0.1, rely=0.0, relwidth=0.9, relheight=1)

            self.logo = tk.Label(self.varFrameLateralDireito, image=self.imagemLogo,
                                 bg=self.color2, highlightthickness=0, bd=0)
            self.logo.place(relx=0.45, rely=0.1)

        frameLateralEsquerdo(self)
        frameLateralDireito(self)


if __name__ == '__main__':
    Aplicacao()
