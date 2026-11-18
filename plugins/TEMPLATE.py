# -*- coding: utf-8 -*-
# ══════════════════════════════════════════════
#  TEMPLATE DE PLUGIN — copie este arquivo,
#  troque o conteúdo e pronto: vira um comando!
# ══════════════════════════════════════════════

# info: como o Jarvis mostra seu plugin no painel
info = {
    "nome": "Meu Plugin",        # nome bonito
    "desc": "O que ele faz",     # descrição curta
    "comando": "/meu",           # comando para ativar na conversa
}

def executar(args):
    """args = o que vier depois do comando. Ex: /meu 10 → args='10'"""
    print("  Olá! Este é um plugin de exemplo. Você digitou:", args or "(nada)")
