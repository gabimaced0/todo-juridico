ToDo Jurídico - Serverless API
==============================

API Serverless para gerenciamento de tarefas jurídicas, desenvolvida com **Python, AWS Lambda, DynamoDB e Terraform**. O projeto segue princípios de **Clean Architecture** para garantir desacoplamento, testabilidade e fácil manutenção.

Tecnologias Utilizadas
-------------------------

-   **Linguagem:** Python 3.12

-   **Compute:** AWS Lambda

-   **API:** AWS API Gateway (HTTP API)

-   **Banco de Dados:** Amazon DynamoDB (NoSQL)

-   **IaC:** Terraform

-   **Testes:** Unittest + Moto (Mock AWS)

* * * * *

Como Executar (Deploy)
-------------------------

### Pré-requisitos

-   AWS CLI configurado com credenciais válidas.

-   Terraform instalado.

-   Python 3.12 instalado.

### 1\. Provisionar Infraestrutura

Entre na pasta de infraestrutura e execute o Terraform:

Bash

```
cd infra
terraform init
terraform apply --auto-approve

```

Ao final, o terminal exibirá a **URL da API**.

> **Exemplo:** `https://xyz123.execute-api.sa-east-1.amazonaws.com/tasks`

* * * * *

Documentação da API
----------------------

### 1\. Criar Tarefa

`POST /tasks`

**Corpo da Requisição (JSON):**

JSON

```
{
  "titulo": "Análise de Processo 123",
  "descricao": "Verificar prazos e documentos anexos.",
  "criado_por": "Dr. Silva"
}

```

### 2\. Listar Todas as Tarefas

`GET /tasks`

### 3\. Buscar Tarefa por ID

`GET /tasks/{id}`

### 4\. Atualizar Tarefa (Parcial)

`PUT /tasks/{id}`

**Corpo da Requisição (JSON):**

JSON

```
{
  "status": "Em Progresso",
  "data_conclusao": "10/02/2026"
}

```

### 5\. Deletar Tarefa

`DELETE /tasks/{id}` *(Resposta: 204 No Content)*

* * * * *

Testes
---------

O projeto utiliza **Moto** para simular o ambiente AWS sem gerar custos ou necessidade de conexão.

### Instalar dependências de teste

Bash

```
pip install boto3 moto requests

```

### Rodar Testes Unitários

Bash

```
python -m unittest discover tests

```

* * * * *

Estrutura do Projeto
-----------------------

Plaintext

```
todojuridico/
├── src/
│   ├── dto/           # Data Transfer Objects (Validação)
│   ├── enums/         # Status e Tipos fixos
│   ├── exceptions/    # Exceções customizadas
│   ├── model/         # Entidades de Domínio
│   ├── service/       # Regras de Negócio e Persistência
│   ├── utils/         # Validadores auxiliares
│   └── lambda_handler.py  # Ponto de entrada (Entrypoint)
├── infra/             # Arquivos Terraform (.tf)
├── tests/             # Testes unitários e mocks
└── README.md

```

* * * * *

Decisões de Design
---------------------

1.  **Serverless First:** Uso de Lambda + DynamoDB para garantir escalabilidade automática e custo zero em períodos de inatividade.

2.  **API Gateway:** Opção pela HTTP API por apresentar menor latência e custo reduzido em relação à REST API padrão.

3.  **Camadas de Responsabilidade:**

    -   **Handler:** Orquestra a entrada/saída HTTP.

    -   **Service:** Onde mora o "coração" do negócio.

    -   **DTO:** Barreira de segurança para integridade de dados.