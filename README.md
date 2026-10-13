# 🐧 Linux Dojo

Site educativo com visual de **área de trabalho retrô em pixel art**, para aprender
**Linux, Python, Cibersegurança e Java** resolvendo desafios e ganhando pontos.

## ✨ Funcionalidades

- Área de trabalho com pastas clicáveis (`/python`, `/seguranca`, `/java`...)
- Desafios com resposta digitada como num terminal
- Pontuação por sessão (cada desafio só pontua uma vez)
- Arte em pixel (fundo e ícones) **gerada com Python** usando Pillow
- Testes automáticos, incluindo um teste de proteção contra XSS

## 🛠️ Tecnologias

- Python 3 + [Flask](https://flask.palletsprojects.com/)
- Jinja2 (templates com herança)
- Pillow (geração das imagens)
- pytest (testes)
- HTML + CSS

## 🚀 Como rodar

```bash
git clone https://github.com/alinemelanski/linux-dojo.git
cd linux-dojo
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 gerar_pixels.py         # gera o fundo e os ícones
python3 app.py
```

Abra http://127.0.0.1:5000 no navegador.

Para rodar os testes: `python3 -m pytest -v`

## 📁 Estrutura

```
linux-dojo/
├── app.py            # rotas do site (Flask)
├── desafios.py       # banco de perguntas e lógica de correção
├── gerar_pixels.py   # desenha o fundo e os ícones em pixel art
├── test_app.py       # testes automáticos
├── templates/        # páginas HTML (Jinja)
└── static/           # CSS e imagens
```

## 🗺️ Próximos passos

- [ ] Cadastro e login (com hash de senha)
- [ ] Ranking com banco de dados SQLite
- [ ] Trilha de Java
- [ ] Trilha de comandos Linux

---

Feito por **Aline Melanski** como projeto de aprendizado ·
[LinkedIn](https://linkedin.com/in/aline-melanski-840a65113)
