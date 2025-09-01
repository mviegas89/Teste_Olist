Relatório de Tarefas

Script em Python que integra com a API pública [JSONPlaceholder](https://jsonplaceholder.typicode.com/), gera um relatório de tarefas por usuário e salva localmente em `.json`, além de enviar os dados via POST para a API mock.

Funcionalidades
- Busca usuários e tarefas (`/users`, `/todos`).
- Calcula tarefas concluídas e pendentes por usuário.
- Gera relatório em `relatorio_tarefas.json`.
- Envia relatório via POST para `/posts`.

Tecnologias
- Python 3.8+
- requests, json, logging, pathlib

Execução
```bash
pip install requests
python script.py
