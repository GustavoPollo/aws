import imp
import json
import logging
import sys
import boto3
from botocore.exceptions import ClientError
import os
import requests
import codecs

#=======================================================
# Captura os valores passados pelo usuário.
acess_key_user = input("Chave de acesso:")
secret_acess_key_user = input("Chave Secreta de acesso:")

#=======================================================
# Usa as chaves do usuário para conectar-se ao S3 AWS.
acess_key = str(acess_key_user)
secret_access_key = str(secret_acess_key_user)
s3 = boto3.client(
    aws_access_key_id = acess_key,
    aws_secret_access_key= secret_access_key,
    region_name = 'us-east-1',
    service_name = 's3'
)

#=======================================================
# Função que pega um arquivo no computador, e faz o 
# upload no AWS.
def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

#=======================================================
# Função que usa o CEP passado pelo usuário, e o manda
# para API viacep que devolve um dicionário com as info.
def capt_cep():
    cep_request = requests.get('http://viacep.com.br/ws/{}/json/'.format(cep))
    cep_result = cep_request.json()
    return cep_result

#=======================================================
# Função que baixa um arquivo da AWS em uma pasta especifica.
def download_file():
    s3.download_file('s3-teste-bucket', nome_arquivo, dir_cep)

#=======================================================
# Função que transforma o dicionário feito pelo viacep
# e o transforma em um arquivo json.
def write_json():
    capt_cep_result = capt_cep()
    with open(str(diretorio_cep)+"\\cep.json", 'wb') as outfile:
        json.dump(capt_cep_result, codecs.getwriter("utf-8")(outfile))

#=======================================================
# Pergunta se o usuário deseja baixar um arquivo com
# informações de determinado CEP.
# Se sim, pergunta o CEP e o diretório para salva-lo,
# manda o CEP para a API viacep que retorna informações
# sobre este CEP, estas informações são convertidas para
# um arquivo json que é salvo no diretório escolhido.
download_cep = input("Você deseja baixar informações de um CEP?\n (1)Sim (2)Não\n")
if download_cep == "1":
    cep = input("CEP:")
    diretorio_cep = input("Diretório para salvar o arquivo:")
    capt_cep()
    write_json()
elif download_cep == "2":
    pass
else:
    print("Valor inválido.")
    sys.exit()

#=======================================================
# Pergunta se o usuário deseja dar upload em algum arquivo
# caso sim, pede o diretório e printa todos os arquivos
# do diretório escolhido. Então pede para selecionar um
# arquivo para dar upload e um nome para o arquivo no AWS.
upload_list = input("Você deseja mandar algum arquivo para AWS?\n (1)Sim (2)Não\n")
if upload_list == "1":
    diretorio_list = input("Diretório onde está o arquivo para upload:")
    dir = sorted(os.listdir(diretorio_list))
    print("******************************")
    for files in dir:
        print(files)
    nome_arquivo_upload = input("Nome do arquivo para upload:")
    nome_arquivo_aws = input("Nome do arquivo na AWS:")
    diretorio_arquivo = str(diretorio_list)+"\\"+str(nome_arquivo_upload)
    upload_file(diretorio_arquivo, 's3-teste-bucket', nome_arquivo_aws)
elif upload_list == "2":
    pass
else:
    print("Valor inválido.")

#=======================================================
# Pergunta se o usuário deseja fazer download de algum arquivo
# da AWS caso sim, pede o diretório, o arquivo na AWS e
# o nome que sará dado ao arquivo baixado. Então faz
# download do arquivo no diretório e com o nome escolhido.
download_aws = input("Você deseja fazer download de algum arquivo do AWS?\n (1)Sim (2)Não\n")
if download_aws == "1":
    diretorio = input("selecione o diretório destino:")
    nome_arquivo = input("Nome do arquivo AWS:")
    nome_arquivo_destino = input("Nome do arquivo destino:")
    dir_cep = (diretorio+"\\"+nome_arquivo_destino)
    download_file()
elif download_aws == "2":
    pass
else:
    print("Valor inválido.")
