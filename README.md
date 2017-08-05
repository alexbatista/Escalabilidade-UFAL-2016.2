# Escalabilidade-UFAL-2016.2


## Arquitetura utilizada
![Arquitetura](escalabilidade.png)

A figura acima apresenta o esquema geral utilizado para o testador de carga.
- O usuário faz uma requisição POST a um recurso via API REST com um JSON no formato:
```
{
'host': 'http://www.myurl.com',
'totalRequests': 'qtdTotaldeRequisicoes',
'distributionType':'distribution',
'email':'email@email.com',
'testName':'MyTest'
}
```
onde:
   - **host** indica a URL do sistema/site a ser testado
   - **totalRequests** indica a quantidade de requisições a serem feitas
   - **distributionType** indica a maneira com a qual as requisições serão feitas. As opções são: *Normal*; *Gausiana*,*xxxxxx*
   - **email** indica o email para o qual o relatório será enviado após a conclusão dos testes
   - **testName** indica o nome do teste dado pelo Usuário


- O API GateWay dispara  uma função Lambda responsável por ativar o testador que está na instância do EC2.

- Dependendo da quantidade de requisições a serem realizadas e a distribuição escolhida, a quantidade de instâncias do EC2 pode ser escalada automaticamente através do *Load Balancer* e *Auto Scaling*.

- Neste projeto, na instância do EC2, foi utilizado um servidor simples em NODE.js que executava o testador *serverTester.py*. No entanto, qualquer servidor pode ser utilizado, bastando apenas executar o script passando os parâmetros corretamente.

- O script *serverTester.py* utiliza um esquema de threads para realizar as requições, maximizando assim, a quantidade de requisições simultâneas.

- Após a execução do testador *serverTester.py* os resultados ficam armazenados localmente para análise via RStudio e também são salvos no S3 para posterior envio por email para o usuário.


## Dependências do Projeto

### API GATEWAY

O Api Gateway foi utilizado para criar um recurso **requisicao**, capaz de disparar uma função Lambda passando os parâmetros no formato JSON.
O recurso possui apenas um método **POST** e os
campos do JSON utilizados na requisição, são os seguintes:

```
{
'host': 'http://www.myurl.com',
'totalRequests': 'qtdTotaldeRequisicoes',
'distributionType':'distribution',
'email':'email@email.com',
'testName':'MyTest'
}
```

### Lambda
O código da função lambda utilizada está disponível no arquivo *CodigoLambda.zip* que deverá ser enviado para o Lambda utilizando Python3.6.
Importante notar que a biblioteca *Requests* é uma dependência do código, já inclusa no arquivo compactado.

### EC2 (Servidor rodando script Python)
A instância do EC2 que será utilizada para execução do script *serverTester.py* deverá possui as seguintes biliotecas instaladas (além do python):
 - qrequests;
 - boto3;
 - numpy;
 - resource.

#### RStudio
Opcionalmente, pode ser instalado o RStudio para tratamento e análise dos dados na própria instância do EC2.


## Melhorias a serem realizadas
- Implementar o envio de email para o usuário ao fim de cada teste.

- Atualmente o mesmo EC2 está sendo utilizado para executar o Servidor R e processar as requisições, assim, separar as instâncias do EC2 e suas responsabilidades é primordial.

- Implementar uma aplicação ou sistema, para interface com o usuário, visto que a requisição do recurso REST, atualmente, só pode ser feita via ferramentas como o **POSTMAN**.
