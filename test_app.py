# test_app.py — testes automáticos
# Rode com:  python3 -m pytest -v
# (instale antes: pip install pytest)
#
# O Flask tem um "cliente de teste": ele finge ser um navegador,
# sem precisar abrir o servidor de verdade.

from app import app
from desafios import normalizar


def cliente():
    app.config["TESTING"] = True
    return app.test_client()


def test_pagina_inicial_tem_pastas_novas():
    r = cliente().get("/")
    assert r.status_code == 200           # 200 = OK
    assert b"/python" in r.data           # b"..." = texto em bytes
    assert b"/seguranca" in r.data


def test_filtro_por_trilha():
    r = cliente().get("/desafios?trilha=seguranca")
    assert b"chmod" in r.data             # pergunta de segurança aparece
    assert b"len(" not in r.data          # pergunta de Python não aparece


def test_normalizar_ignora_maiusculas_e_espacos():
    assert normalizar("   LS    -L  ") == "ls -l"


def test_acertar_soma_pontos_so_uma_vez():
    c = cliente()
    c.post("/desafios/1", data={"resposta": "print"})
    c.post("/desafios/1", data={"resposta": "print"})   # repetiu!
    r = c.get("/desafios")
    assert "⭐ 10 pontos".encode() in r.data            # não virou 20


def test_errar_nao_soma_pontos():
    c = cliente()
    c.post("/desafios/2", data={"resposta": "4"})
    r = c.get("/desafios")
    assert "⭐ 0 pontos".encode() in r.data


def test_desafio_inexistente_da_404():
    assert cliente().get("/desafios/999").status_code == 404


def test_xss_e_bloqueado():
    # Tentamos "atacar" o próprio site: mandar um <script> na trilha.
    r = cliente().get("/desafios?trilha=<script>alert(1)</script>")
    assert b"<script>alert(1)</script>" not in r.data   # não foi parar no HTML
