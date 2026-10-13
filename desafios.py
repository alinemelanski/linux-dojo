# desafios.py — o "banco de perguntas" do Linux Dojo
#
# POR QUE UM ARQUIVO SEPARADO?
# Separar dados de lógica é uma boa prática chamada "separação de responsabilidades".
# O app.py cuida das rotas (o que acontece em cada página);
# este arquivo só guarda o conteúdo. Mais tarde, trocaremos esta lista
# por um banco de dados (SQLite) sem precisar mexer nas rotas.
#
# ESTRUTURA DE CADA DESAFIO (um dicionário):
#   id        -> número único, usado na URL (/desafios/1)
#   trilha    -> categoria: "python" ou "seguranca"
#   nivel     -> "fácil", "médio" ou "difícil"
#   pontos    -> quanto vale (servirá para o ranking)
#   pergunta  -> o enunciado
#   respostas -> LISTA de respostas aceitas (há várias formas certas de responder!)
#   explicacao-> mostrada depois de acertar: aqui é onde a pessoa APRENDE

DESAFIOS = [
    # ---------------- TRILHA PYTHON ----------------
    {
        "id": 1,
        "trilha": "python",
        "nivel": "fácil",
        "pontos": 10,
        "pergunta": "Qual função do Python mostra um texto na tela?",
        "respostas": ["print", "print()"],
        "explicacao": "print() envia o texto para a saída padrão (o terminal). "
                      "Exemplo: print('Olá, mundo!')",
    },
    {
        "id": 2,
        "trilha": "python",
        "nivel": "fácil",
        "pontos": 10,
        "pergunta": "Qual o resultado de: len('linux') ?",
        "respostas": ["5"],
        "explicacao": "len() conta quantos itens existem. Uma string é uma sequência "
                      "de caracteres: l-i-n-u-x = 5.",
    },
    {
        "id": 3,
        "trilha": "python",
        "nivel": "médio",
        "pontos": 20,
        "pergunta": "Qual palavra-chave cria uma função em Python?",
        "respostas": ["def"],
        "explicacao": "def vem de 'define'. Exemplo:\n"
                      "def saudacao(nome):\n    return 'Oi, ' + nome",
    },
    {
        "id": 4,
        "trilha": "python",
        "nivel": "médio",
        "pontos": 20,
        "pergunta": "Qual comando instala uma biblioteca do Python pelo terminal? "
                    "(ex.: para instalar o flask)",
        "respostas": ["pip install flask", "pip3 install flask"],
        "explicacao": "pip é o gerenciador de pacotes do Python. Dica: use sempre "
                      "dentro de um venv para não misturar projetos.",
    },

    # ---------------- TRILHA CIBERSEGURANÇA ----------------
    {
        "id": 5,
        "trilha": "seguranca",
        "nivel": "fácil",
        "pontos": 10,
        "pergunta": "No Linux, qual comando mostra as permissões dos arquivos de uma pasta?",
        "respostas": ["ls -l", "ls -la", "ls -al"],
        "explicacao": "ls -l mostra algo como -rwxr-xr--. São 3 grupos: dono, grupo "
                      "e outros. r = ler, w = escrever, x = executar.",
    },
    {
        "id": 6,
        "trilha": "seguranca",
        "nivel": "médio",
        "pontos": 20,
        "pergunta": "Qual número usar no chmod para que SÓ o dono possa ler e escrever "
                    "um arquivo (ninguém mais acessa)?",
        "respostas": ["600", "chmod 600"],
        "explicacao": "Cada permissão vale um número: r=4, w=2, x=1. Dono: 4+2 = 6. "
                      "Grupo: 0. Outros: 0. Resultado: 600. Ideal para arquivos com "
                      "senhas, como chaves SSH.",
    },
    {
        "id": 7,
        "trilha": "seguranca",
        "nivel": "médio",
        "pontos": 20,
        "pergunta": "Qual a sigla do ataque em que alguém injeta código JavaScript "
                    "malicioso numa página através de um campo de texto?",
        "respostas": ["xss", "cross-site scripting", "cross site scripting"],
        "explicacao": "XSS = Cross-Site Scripting. A defesa é nunca exibir o texto do "
                      "usuário 'cru'. O Flask (Jinja) já 'escapa' tudo que você coloca "
                      "em {{ }}, transformando < em &lt;. Por isso este site é protegido!",
    },
    {
        "id": 8,
        "trilha": "seguranca",
        "nivel": "difícil",
        "pontos": 30,
        "pergunta": "Senhas devem ser guardadas no banco como texto puro, criptografadas "
                    "ou como hash?",
        "respostas": ["hash", "como hash", "hash com salt"],
        "explicacao": "Hash é uma via de mão única: não dá para 'desfazer'. No login, "
                      "você gera o hash da senha digitada e compara. Em Python: "
                      "werkzeug.security.generate_password_hash (vem com o Flask). "
                      "Vamos usar isso quando fizermos o cadastro!",
    },
]

# As trilhas, com nome bonito e ícone para mostrar na tela
TRILHAS = {
    "python":    {"titulo": "Python",         "icone": "🐍"},
    "seguranca": {"titulo": "Cibersegurança", "icone": "🛡️"},
}


def buscar_desafio(desafio_id):
    """Procura um desafio pelo id. Devolve None se não existir."""
    # next() pega o primeiro item que satisfaz a condição;
    # o segundo argumento (None) é o valor padrão se nada for encontrado.
    return next((d for d in DESAFIOS if d["id"] == desafio_id), None)


def normalizar(texto):
    """Deixa a resposta num formato padrão antes de comparar.

    SEGURANÇA + USABILIDADE: nunca confie que o usuário digitou
    exatamente como você espera. Aqui:
      - strip()  -> tira espaços do começo e do fim
      - lower()  -> tudo minúsculo ("PRINT" vira "print")
      - split()/join -> troca espaços repetidos por um só ("ls   -l" vira "ls -l")
      - [:100]   -> corta textos gigantes (evita abuso)
    """
    return " ".join(texto.strip().lower().split())[:100]


def resposta_correta(desafio, resposta_usuario):
    """True se a resposta (já normalizada) estiver na lista de aceitas."""
    resposta = normalizar(resposta_usuario)
    aceitas = [normalizar(r) for r in desafio["respostas"]]
    return resposta in aceitas
