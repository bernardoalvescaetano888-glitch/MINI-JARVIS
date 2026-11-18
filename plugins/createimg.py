# -*- coding: utf-8 -*-
# Plugin: /createimg — gera imagens a partir de texto
# Uso:  /createimg um gato astronauta pintando o rio Muriaé
# Precisa de internet. Gratuito, sem chave.
info = {"nome": "Criar Imagem", "desc": "Gera imagem a partir de texto",
        "comando": "/createimg"}

def executar(args):
    import os
    import time as t
    import urllib.parse
    from urllib.request import urlopen, Request

    prompt = args.strip()
    if not prompt:
        print("Uso: /createimg <descrição da imagem>")
        print("Ex:  /createimg um gato astronauta")
        return

    url = ("https://image.pollinations.ai/prompt/"
           + urllib.parse.quote(prompt)
           + "?width=768&height=768&nologo=true")

    print("🎨 Gerando imagem… (pode levar ~30 segundos)")
    dados = urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}),
                    timeout=120).read()

    pasta = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "imagens")
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, f"img_{int(t.time())}.png")
    with open(caminho, "wb") as f:
        f.write(dados)

    print(f"✔ Imagem salva em: {caminho}")
    try:
        os.startfile(caminho)
        print("🖼 Aberta no visualizador!")
    except Exception:
        pass
