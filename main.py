import requests
import json
import logging
from pathlib import Path

# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

USERS_URL = "https://jsonplaceholder.typicode.com/users"
TODOS_URL = "https://jsonplaceholder.typicode.com/todos"
POST_URL = "https://jsonplaceholder.typicode.com/posts"
OUTPUT_FILE = Path("Teste_Olist/relatorio_tarefas.json")


def fetch_data(url):
    """Faz a requisição GET e retorna os dados em JSON."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Erro ao acessar {url}: {e}")
        return []


def process_data(users, todos):
    """Processa os dados para gerar o relatório."""
    report = []

    for user in users:
        user_id = user["id"]
        name = user["name"]

        user_tasks = [task for task in todos if task["userId"] == user_id]
        completed = sum(task["completed"] for task in user_tasks)
        pending = len(user_tasks) - completed

        report.append({
            "user_id": user_id,
            "title": f"{name} tasks",
            "body": f"completed_tasks: {completed}, pending_tasks: {pending}"
        })

    return report


def save_local(report):
    """Salva o relatório em um arquivo .json local."""
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
        logging.info(f"Relatório salvo em {OUTPUT_FILE.absolute()}")
    except Exception as e:
        logging.error(f"Erro ao salvar arquivo local: {e}")


def send_report(report):
    """Envia o relatório via POST para a API mock."""
    try:
        response = requests.post(POST_URL, json=report, timeout=10)
        response.raise_for_status()
        logging.info("Relatório enviado com sucesso!")
        logging.info(f"Resposta da API: {response.json()}")
    except requests.RequestException as e:
        logging.error(f"Erro ao enviar relatório: {e}")


def main():
    logging.info("Iniciando integração de dados...")
    users = fetch_data(USERS_URL)
    todos = fetch_data(TODOS_URL)

    if not users or not todos:
        logging.error("Não foi possível obter dados necessários. Abortando.")
        return

    report = process_data(users, todos)

    save_local(report)
    send_report(report)
    logging.info("Processo concluído!")


if __name__ == "__main__":
    main()
