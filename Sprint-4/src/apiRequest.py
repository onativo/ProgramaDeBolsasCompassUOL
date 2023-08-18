import json
import requests
import boto3    

def lambda_handler(event, context):
        #configurações do bancode dados
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
        #define a tabela que vamos usar
    table = dynamodb.Table('viacepDataset')

        #inicia a variavel cep com string vazia
    cep = ''
    
        #inicia a variável msg com string vazia
    msg = ''
    
        #essa condição pega o CEP passado no MethodTest na caixa de texto: {consultacep} ou na url da api: .../consultacep?cep=12345678
            #e retorna o CEP
    if event.get('queryStringParameters') and event['queryStringParameters'].get('cep'):
        cep = event['queryStringParameters']['cep']
        '''#verifica se o cep passado é diferente de 8 numeros (((ainda não consegui implantar)))
        if len(cep) != 8:
            msg = 'Digite um CEP válido com 8 digitos e sem o hífen, no formato 12345678.'
            result = {
                'statusCode': 200,
                'body': msg
            }'''
        
        #o cep é usado como chave de identificação da tabela. Esse chamado checa se o cep já está na tabela e armazena em 'response'
    response = table.get_item(
    Key={
        'cep': cep
        }
    )

        #se o item procurado está na variável response ele retorna o cep com os dados do banco de dados
    if 'Item' in response:
        response = table.get_item(
            Key={
                'cep': cep
                }
            )
        
            #armazena o resultado na variável items
        items = response['Item']
        msg = (f'Este CEP já está cadastrado no banco de dados. \nAqui estão seus dados: {items}')
        
            #exibe na tela o statusCode e o body da requisição onde estão os dados para aquele referido cep
        result = {
            'statusCode': 200,
            'body': msg
        }
    else:
            #essa parte é para fazer request na API do ViaCEP e retornar a response, converte o resultado para json
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        data = response.json()
        #dados = json.dumps(data, ensure_ascii=False).encode('utf8')
    
            #aqui ele adiciona o resultado da consulta realizada logo acima na variavel 'response'
        response = table.put_item(
            Item = {
            "cep": cep,
            "logradouro": data['logradouro'],
            "bairro": data['bairro'],
            "cidade": data['localidade'],
            "estado": data['uf'],
            "ddd": data['ddd']
            }
        )
    
            #busca o item recém adicionado ao banco de dados
        response = table.get_item(
            Key={
                'cep': cep
            }
        )
        items = response['Item']
        
            #altera a mensagem e retorna os dados recém adicionados
        msg = (f'Não tínhamos estes dados no banco.\nConsultamos nossa API e adicionamos este CEP em nosso banco de dados.\nO resultado está aqui: {items}')
    
            #exibe na tela o statusCode e o body da requisição
        result = {
            'statusCode': 200,
            'body': msg
        }
    
    return result