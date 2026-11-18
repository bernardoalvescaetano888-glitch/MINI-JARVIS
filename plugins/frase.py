# -*- coding: utf-8 -*-
# Plugin de exemplo: frases motivacionais 100% offline
info = {"nome": "Frase", "desc": "Frase motivacional aleatória", "comando": "/frase"}

FRASES = [
    "A gente só aprende a programar programando. Bora codar! 💻",
    "Cada erro hoje é um bug a menos amanhã. 🐛",
    "O segredo não é ser gênio, é não desistir na linha 42. 😄",
    "Grandes projetos começam com print('Olá, mundo!').",
    "Você não precisa ser o melhor, precisa ser constante. 🚀",
]

def executar(args):
    import random
    print("  ✨ " + random.choice(FRASES))
