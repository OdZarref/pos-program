import json

def abrirJson(nomeArquivo):
    arquivo = open(nomeArquivo)
    arquivoJsonAberto = json.load(arquivo)

    return arquivoJsonAberto

def editarJson(nomeArquivo, novoJson):
    with open(nomeArquivo, 'w') as arquivo:
        json.dump(novoJson, arquivo, indent=4)
        arquivo.close()