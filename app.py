# app.py — o "cérebro" do site
# Flask é um micro-framework web em Python: recebe o pedido do navegador
# (ex.: "quero a página /") e devolve uma resposta (HTML).

import os  # para ler variáveis de ambiente (usado na secret_key)

from flask import Flask, render_template, request, session, abort

# Importamos do nosso próprio arquivo desafios.py
from desafios import DESAFIOS, TRILHAS, buscar_desafio, resposta_correta

app = Flask(__name__)

# SEGURANÇA: a secret_key assina o "cookie de sessão" (onde guardamos os pontos).
# Sem ela, alguém poderia editar o cookie e se dar 1000 pontos.
# Nunca escreva a chave real no código (ela iria para o GitHub!).
# Por isso lemos de uma variável de ambiente; o valor depois do "or"
# é só para desenvolvimento na sua máquina.
app.secret_key = os.environ.get("SECRET_KEY") or "chave-so-para-desenvolvimento"

# As "pastas" da área de trabalho.
# "cor" escolhe qual ícone usar (static/img/pasta-<cor>.png, gerado pelo gerar_pixels.py)
# "link" é opcional: se existir, clicar na pasta abre aquela página.
PASTAS = [
    {"nome": "home",      "cor": "amarela",  "descricao": "Bem-vindo! Comece por aqui."},
    {"nome": "bin",       "cor": "laranja",  "descricao": "Comandos essenciais do Linux."},
    {"nome": "python",    "cor": "verde",    "descricao": "Aprenda Python do zero.",
     "link": "/desafios?trilha=python"},
    {"nome": "seguranca", "cor": "vermelha", "descricao": "Cibersegurança na prática.",
     "link": "/desafios?trilha=seguranca"},
    {"nome": "java",      "cor": "roxa",     "descricao": "Aprenda a programar em Java no Linux."},
    {"nome": "desafios",  "cor": "azul",     "descricao": "Todos os desafios.",
     "link": "/desafios"},
    {"nome": "ranking",   "cor": "amarela",  "descricao": "Em breve: veja quem está no topo."},
]


@app.route("/")
def desktop():
    # a barra de tarefas mostra os pontos em todas as telas, então mandamos aqui também
    return render_template("index.html", pastas=PASTAS, pontos=session.get("pontos", 0))


@app.route("/desafios")
def lista_desafios():
    # request.args lê o que vem depois do "?" na URL.
    # Ex.: /desafios?trilha=python  ->  trilha = "python"
    trilha = request.args.get("trilha")

    # SEGURANÇA: só aceitamos trilhas que existem. Se alguém digitar
    # ?trilha=qualquercoisa, simplesmente mostramos todos.
    if trilha not in TRILHAS:
        trilha = None

    # "list comprehension": um for compacto que filtra a lista
    if trilha:
        lista = [d for d in DESAFIOS if d["trilha"] == trilha]
    else:
        lista = DESAFIOS

    # session é um dicionário guardado no navegador (assinado pela secret_key)
    resolvidos = session.get("resolvidos", [])

    return render_template("desafios.html", desafios=lista, trilhas=TRILHAS,
                           trilha=trilha, resolvidos=resolvidos,
                           pontos=session.get("pontos", 0))


# <int:desafio_id> captura o número da URL e já converte para int.
# methods: GET = abrir a página; POST = enviar o formulário com a resposta.
@app.route("/desafios/<int:desafio_id>", methods=["GET", "POST"])
def desafio(desafio_id):
    d = buscar_desafio(desafio_id)
    if d is None:
        abort(404)  # página "não encontrada"

    resultado = None  # None = ainda não respondeu; True/False = acertou/errou

    if request.method == "POST":
        # .get("resposta", "") evita erro se o campo não vier
        resposta = request.form.get("resposta", "")
        resultado = resposta_correta(d, resposta)

        resolvidos = session.get("resolvidos", [])
        # Só soma pontos na PRIMEIRA vez que acerta (senão era só repetir!)
        if resultado and d["id"] not in resolvidos:
            resolvidos.append(d["id"])
            session["resolvidos"] = resolvidos
            session["pontos"] = session.get("pontos", 0) + d["pontos"]

    return render_template("desafio.html", d=d, trilhas=TRILHAS,
                           resultado=resultado, pontos=session.get("pontos", 0))


if __name__ == "__main__":
    app.run(debug=True)
