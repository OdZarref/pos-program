import json

def abrirJson(nomeArquivo):
    arquivo = open(nomeArquivo)
    arquivoJsonAberto = json.load(arquivo)

    return arquivoJsonAberto

def editarJson(nomeArquivo, arquivoJson):
    with open(nomeArquivo, 'w') as arquivo:
        json.dump(arquivoJson, arquivo, indent=4)
        arquivo.close()