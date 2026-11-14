# Oficina API — API REST em Flask

API REST para uma oficina mecânica, com CRUD de clientes, veículos, peças, serviços e ordens de serviço.

Avaliação B1 da disciplina **Programação Avançada III** (ADS, UniSALESIANO Araçatuba), entregue em abril de 2026. O enunciado pedia uma API com pelo menos 5 tabelas e CRUD para cada uma.

## Rotas

Cada recurso tem as mesmas cinco rotas:

| Método | Rota | Ação |
| --- | --- | --- |
| GET | `/<recurso>` | lista todos |
| GET | `/<recurso>/<id>` | busca um |
| POST | `/<recurso>` | cria |
| PUT | `/<recurso>/<id>` | atualiza |
| DELETE | `/<recurso>/<id>` | exclui |

Recursos: `clientes`, `veiculos`, `pecas`, `servicos`, `ordemservicos`. A rota `/` responde `Oficina API`.

## Stack

- Python e Flask, com um Blueprint por recurso
- Flask-SQLAlchemy e Flask-Migrate
- MySQL com PyMySQL
- python-dotenv para a configuração

## Modelo de dados

- `Cliente`
- `Veiculo`, ligado a um cliente
- `Peca`
- `Servico`
- `OrdemServico`, ligada a um veículo, um serviço e uma peça

## Como rodar

1. Crie um banco MySQL chamado `oficina`.
2. Copie `.env.example` para `.env` e preencha usuário e senha do banco.
3. Instale e rode:

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python app.py
```

4. A API sobe em `http://127.0.0.1:5000/`. Teste com Postman ou curl:

```bash
curl http://127.0.0.1:5000/clientes
```

## Estrutura

```
app.py          cria a aplicação e registra os blueprints
config.py       lê o .env e monta a conexão
db.py           inicialização do SQLAlchemy
models.py       modelos das 5 tabelas
routes/         um arquivo de rotas por recurso
```

## Observações

- Projeto acadêmico, sem autenticação nas rotas.
- A mesma oficina tem uma versão web em [oficina-cc-django](https://github.com/Fabioluiiz22010/oficina-cc-django).

## Autor

Fabio Luiz Florêncio da Silva · [github.com/Fabioluiiz22010](https://github.com/Fabioluiiz22010) · [LinkedIn](https://www.linkedin.com/in/fabio-l-florencio/)
