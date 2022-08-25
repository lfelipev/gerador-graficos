# beotag-wafermaps
Aplicação dockerizada de tratamento de Wafermaps com integração com banco de dados MySQL

## Instruções para download e execução local.

Para executar a infraestrutura siga as instruções:
  1. Baixe e instale a ferramenta [Docker Compose](https://docs.docker.com/compose/install/).
    - Fique atento aos pré-requisitos da instalação.
  2. Inicie a ferramenta instalada.
  3. Clone o repositório em um diretório da sua preferência:
 
```bash 
git clone https://github.com/EASY-UFAL/beotag-wafermaps.git
```
  
  4. No terminal, acesse na pasta do repositório.
  5. Em seguida execute os serviços
  ```bash
  docker compose up
  ```
  
  ## Compilação e teste do código
  
  1. Ao compilar o código ou fazer mudanças no repositório da aplicação execute.
  ```bash
  docker compose build
  ```
  2. Em seguida
  ```bash
  docker compose up
  ```
  3. Para testar a aplicação individualmente, em outro terminal execute.
  ```bash
  docker-compose exec python_app bash
  ```
  4. E finalmente execute a aplicação, por exemplo.
   ```bash
  python ProcessWafer.py
  ```
  
  ## Recomenda-se utilizar uma branch separada para testes
  
  1. Para criar uma nova branch execute.
  ```bash
  git checkout -b feature/wafermap-reading
  ```
  2. Ao finalizar a programação na branch, criar um Pull Request e aguardar a avaliação/aprovação.

  ## Dicas para o pull request
  
  1. Remova todos os arquivos temporários;
  2. Remova todas as bibliotecas, variáveis e funções não utilizadas;
  3. Remova todos os comentários desnecessários
