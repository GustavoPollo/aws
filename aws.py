import imp
import json
import logging
import boto3
from botocore.exceptions import ClientError
import os
import requests
import codecs

acess_key_user = input("Chave de acesso:")
secret_acess_key_user = input("Chave Secreta de acesso:")
diretorio = input("selecione o diretório destino")
nome_arquivo = input("Nome do arquivo:")
cep = input("CEP:")
dir_cep = (diretorio+"\\"+nome_arquivo)

acess_key  =  str(acess_key_user)
secret_access_key  =  str(secret_acess_key_user)

s3 = boto3.client(
    aws_access_key_id = acess_key,
    aws_secret_access_key= secret_access_key,
    region_name = 'us-east-1',
    service_name = 's3'
)

def capt_cep():
    cep_request = requests.get('http://viacep.com.br/ws/{}/json/'.format(cep))
    cep_result = cep_request.json()
    return cep_result

def upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        response = s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def download_file():
    s3.download_file('s3-teste-bucket', nome_arquivo, dir_cep)

def write_json():
    capt_cep_result = capt_cep()
    with open(".\\cep.json", 'wb') as outfile:
        json.dump(capt_cep_result, codecs.getwriter("utf-8")(outfile))

write_json()
upload_file('.\\cep.json', 's3-teste-bucket', nome_arquivo)
download_file()
