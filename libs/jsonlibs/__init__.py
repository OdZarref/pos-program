import json

def abrirJson(nomeArquivo):
    arquivo = open('produtos.json')
    arquivoJsonAberto = json.load(arquivo)

    return arquivoJsonAberto

def editarJson(nomeArquivo, arquivoJson):
    with open('produtos.json', 'w') as arquivo:
        json.dump(arquivoJson, arquivo, indent=4)
        arquivo.close()