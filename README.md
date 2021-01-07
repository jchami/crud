# CRUD
* API feita para implantação na plataforma Heroku
## Utilização
* A rota ```/login``` é a única rota acessível sem a autenticação adequada
### Exemplos
* Autenticação:
    ```
    curl --location --request POST 'URL/login' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "email": "foo@bar.com",
        "password": "123"
    }'
    ```

* Criação de solicitação:
    ```
    curl --location --request POST 'URL/post' \
    --header 'Authorization: Bearer **TOKEN DISPONIBILIZADO NA RESPOSTA DO LOGIN**' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "company_name": "Foobar Inc.",
    }'
    ```


## API
### /login
Autenticar um usuário
* Method: ```POST```
* Request Params:
    - ```email```: E-mail do usuário
    - ```password```: Senha do usuário
* Response: 
    - ```token```: Token de acesso a ser incluído no cabeçalho
    - ```userEmail```: E-mail do usuário logado
    - ```tokenExpiresIn```: Tempo em segundos para expiração do token

### /activationrequest
Visualizar uma solicitação de ativação
* Method: ```GET```
* Query Params:
    - ```request_id```: ID da solicitação a ser visualizada
* Response: 
    - ```id```: ID da solicitação visualizada
    - ```user```: ID do usuário criador da solicitação
    - ```company_name```: Nome da empresa parceira
    - ```status```: Status da solicitação de ativação

### /activationrequest
Criar nova solicitação de ativação
* Method: ```POST```
* Request Params:
    - ```company_name```: Nome da empresa parceira
* Response: 
    - ```id```: ID da solicitação criada
    - ```user```: ID do usuário logado (criador da solicitação)
    - ```company_name```: Nome da empresa parceira
    - ```status```: Status da solicitação de ativação recém criada (default=null)

### /activationrequest
Atualizar status de solicitação de ativação
* Method: ```PUT```
* Request Params:
    - ```request_id```: ID da solicitação a ser atualizada
    - ```approved```: Novo status de solicitação de ativação
* Response:
    - ```id```: ID da solicitação atualizada
    - ```user```: ID do usuário criador da solicitação
    - ```company_name```: Nome da empresa parceira
    - ```status```: Status da solicitação de ativação atualizada

### /activationrequest
Cancelar/remover solicitação de ativação existente
* Method: ```DELETE```
* Request Params:
    - ```request_id```: ID da solicitação a ser removida
* Response: 
    - ```id```: ID da solicitação removida
    - ```user```: ID do usuário criador da solicitação
    - ```company_name```: Nome da empresa parceira
