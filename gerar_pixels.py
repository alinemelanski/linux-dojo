# gerar_pixels.py — desenha a arte em pixel do site usando Python
#
# Rode UMA vez (ou sempre que mudar algo aqui):
#     pip install pillow
#     python3 gerar_pixels.py
#
# A IDEIA DO PIXEL ART:
# Desenhamos uma imagem MINÚSCULA (o fundo tem só 192x108 pixels!)
# e depois o CSS amplia sem "borrar" (image-rendering: pixelated).
# Cada pixelzinho vira um quadrado grande na tela — esse é o visual retrô.

import os
import random

from PIL import Image, ImageColor, ImageDraw  # Pillow: a biblioteca de imagens do Python

PASTA_IMG = os.path.join("static", "img")
os.makedirs(PASTA_IMG, exist_ok=True)  # cria static/img se não existir

# random.seed fixa a "sorte": o aleatório sai IGUAL toda vez que você rodar.
# Assim as montanhas não mudam de formato a cada execução.
random.seed(42)

LARGURA, ALTURA = 192, 108  # proporção 16:9, igual a uma tela


def perfil_montanha(picos, ruido):
    """Calcula a altura (y do topo) da montanha em cada coluna x.

    picos = lista de (x_do_pico, y_do_pico, inclinacao).
    Cada pico é um triângulo: quanto mais longe do pico, mais baixo
    (y maior — lembre: no computador o y CRESCE para baixo!).
    Em cada coluna ficamos com o pico mais alto (o menor y) — min().
    O ruído (random) deixa a encosta irregular, com cara de rocha.
    """
    alturas = []
    for x in range(LARGURA):
        topo = min(py + abs(x - px) * inc for px, py, inc in picos)
        alturas.append(int(topo) + random.randint(0, ruido))
    return alturas


def desenhar_fundo():
    img = Image.new("RGB", (LARGURA, ALTURA))
    d = ImageDraw.Draw(img)

    # 1) CÉU em faixas (degradê "em degraus" = cara de pixel art)
    faixas = ["#3b6fd8", "#4a80e0", "#5b92e8", "#6ea4ee", "#84b6f2", "#9cc8f5", "#b8daf8"]
    altura_faixa = 9
    for i, cor in enumerate(faixas):
        d.rectangle([0, i * altura_faixa, LARGURA, (i + 1) * altura_faixa], fill=cor)
    d.rectangle([0, len(faixas) * altura_faixa, LARGURA, ALTURA], fill=faixas[-1])

    # 2) SOL: um círculo pequeno e um "brilho" em volta
    d.ellipse([146, 14, 166, 34], fill="#fff3b0")
    d.ellipse([150, 18, 162, 30], fill="#ffe066")

    # 3) NUVENS: retângulos empilhados (nuvem de pixel é "escadinha")
    def nuvem(x, y):
        d.rectangle([x + 4, y,     x + 14, y + 2], fill="white")
        d.rectangle([x,     y + 3, x + 22, y + 6], fill="white")
        d.rectangle([x + 2, y + 7, x + 18, y + 8], fill="#dfeefe")  # sombrinha

    nuvem(18, 12)
    nuvem(88, 22)
    nuvem(120, 6)

    # 4) MONTANHAS DO FUNDO (mais claras = mais longe; é a "perspectiva atmosférica")
    longe = perfil_montanha([(30, 40, 0.9), (95, 30, 0.8), (170, 38, 0.9)], ruido=1)
    for x, topo in enumerate(longe):
        d.line([x, topo, x, ALTURA], fill="#8a9ad6")
        if topo < 46:  # só neva nos picos altos (sem esse if, a neve "subia" pro céu!)
            d.line([x, topo, x, min(topo + 6, 46)], fill="#e8eeff")

    # 5) MONTANHAS DA FRENTE, com sombra de um lado e neve no pico
    picos_perto = [(60, 44, 1.1), (135, 52, 1.0)]
    perto = perfil_montanha(picos_perto, ruido=1)
    for x, topo in enumerate(perto):
        # Encosta direita de cada pico fica mais escura: parece luz vindo da esquerda
        px_mais_perto = min(picos_perto, key=lambda p: abs(x - p[0]))[0]
        cor = "#3f5f8f" if x <= px_mais_perto else "#324c75"
        d.line([x, topo, x, ALTURA], fill=cor)
        if topo < 60:  # neve: do topo até a linha y=60 (ou 5 pixels, o que vier antes)
            d.line([x, topo, x, min(topo + 5, 60)], fill="#f4f8ff")

    # 6) CHÃO verde em duas faixas
    d.rectangle([0, 90, LARGURA, ALTURA], fill="#3e8e41")
    d.rectangle([0, 98, LARGURA, ALTURA], fill="#2f6f33")

    # 7) PINHEIROS: triângulos de pixel (cada linha um pouco mais larga)
    def pinheiro(x, chao, tamanho):
        for linha in range(tamanho):
            meia = linha // 2
            d.line([x - meia, chao - tamanho + linha, x + meia, chao - tamanho + linha],
                   fill="#1f4d2b")
        d.line([x, chao, x, chao + 2], fill="#5a3a1e")  # tronquinho

    for x in range(4, LARGURA, 13):
        pinheiro(x + random.randint(-3, 3), chao=96, tamanho=random.randint(8, 13))

    caminho = os.path.join(PASTA_IMG, "fundo.png")
    img.save(caminho)
    print("criado:", caminho)


# ---------- ÍCONE DE PASTA 16x16, desenhado com TEXTO ----------
# Cada letra é um "pixel". Isto é pixel art escrita à mão!
#   . = transparente   C = contorno   F = frente   A = aba/fundo   B = brilho
PASTA_DESENHO = [
    "................",
    "................",
    ".CCCCC..........",
    "CAAAAAC.........",
    "CAAAAAACCCCCCCC.",
    "CAAAAAAAAAAAAAAC",
    "CCCCCCCCCCCCCCCC",
    "CBBBBBBBBBBBBBBC",
    "CBFFFFFFFFFFFFFC",
    "CFFFFFFFFFFFFFFC",
    "CFFFFFFFFFFFFFFC",
    "CFFFFFFFFFFFFFFC",
    "CFFFFFFFFFFFFFFC",
    "CFFFFFFFFFFFFFFC",
    "CCCCCCCCCCCCCCCC",
    "................",
]

# Paleta de cada cor de pasta: (frente, aba, brilho)
CORES_PASTA = {
    "amarela":  ("#f7c948", "#d9a520", "#fff1a8"),
    "azul":     ("#5aa0f0", "#3a76c4", "#bfe0ff"),
    "verde":    ("#6cc66c", "#3f9a45", "#c8f5c0"),
    "vermelha": ("#f06a5a", "#c4433a", "#ffc7bf"),
    "roxa":     ("#a77de8", "#7a52c0", "#e2d2ff"),
    "laranja":  ("#f59a3c", "#cc7220", "#ffd9ad"),
}


def desenhar_pasta(nome, frente, aba, brilho):
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))  # RGBA: o "A" é transparência
    cores = {"C": "#1b1b2f", "F": frente, "A": aba, "B": brilho}

    # enumerate dá o número da linha (y) e da coluna (x) junto com o caractere
    for y, linha in enumerate(PASTA_DESENHO):
        for x, char in enumerate(linha):
            if char in cores:
                # ImageColor.getrgb("#f7c948") -> (247, 201, 72): a cor em números
                img.putpixel((x, y), ImageColor.getrgb(cores[char]))

    caminho = os.path.join(PASTA_IMG, f"pasta-{nome}.png")
    img.save(caminho)
    print("criado:", caminho)


if __name__ == "__main__":
    desenhar_fundo()
    for nome, (frente, aba, brilho) in CORES_PASTA.items():
        desenhar_pasta(nome, frente, aba, brilho)
