import json


def converter_json_para_txt(conteudo_json):
    dados = json.loads(conteudo_json)
    return dados["nome"]


def lista_para_csv(lista):
    resultado = ""
    for item in lista:
        resultado += item + ","
    return resultado
