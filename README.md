# Escalabilidade-UFAL-2016.2


## Código Lambda
- Executar com Python 3.6
- A biblioteca Requests é um dependência (código já comprimido)


## API GATEWAY
- método POST 
- Formato (JSON) da requisição a ser enviada: 
{
'host': event['host'],
'totalRequests': event['totalRequests'],
'distributionType':event['distributionType'],
'email':event['email'],
'testName':event['testName']
}


