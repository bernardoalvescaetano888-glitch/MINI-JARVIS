#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
 MINI-JARVIS  v1.0  â€”  Assistente de IA local, offline e expansÃ­vel
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
 â€¢ Instala o Ollama sozinho (com sua permissÃ£o avanÃ§ada)
 â€¢ Vitrine de IAs com % de chance de funcionar no seu PC
 â€¢ Cria/lÃª/organiza arquivos, roda comandos e usa Git
 â€¢ 100% offline (e hÃ­brido: com internet usa IA maior na nuvem)
 â€¢ Modo claro/escuro, painel lateral, plugins e chats salvos
 â€¢ Sem limite de tokens: tudo roda na sua mÃ¡quina, de graÃ§a
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
"""

import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
import webbrowser
from datetime import datetime

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  CAMINHOS E CONFIGURAÃ‡ÃƒO
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
PASTA_BASE   = os.path.dirname(os.path.abspath(__file__))
PASTA_CHATS  = os.path.join(PASTA_BASE, "chats")
PASTA_PLUGS  = os.path.join(PASTA_BASE, "plugins")
TEMP_DIR     = "D:\\JarvisTemp"   # temporário: some quando o app fecha
try:
    os.makedirs(TEMP_DIR, exist_ok=True)
except Exception:
    TEMP_DIR = PASTA_BASE
ARQ_CONFIG   = os.path.join(PASTA_BASE, "config.json")
ARQ_MEMORIA  = os.path.join(PASTA_BASE, "memoria.json")
ARQ_LEMBRETES = os.path.join(PASTA_BASE, "lembretes.json")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
os.system("")  # habilita cores ANSI no terminal do Windows

TEMAS = {
    "escuro": {"primario": "96", "destaque": "92", "texto": "97",
               "aviso": "93", "erro": "91", "dim": "90", "ok": "92"},
    "claro":  {"primario": "34", "destaque": "32", "texto": "30",
               "aviso": "33", "erro": "31", "dim": "90", "ok": "32"},
}

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  CATÃLOGO DE IAs (chance estimada num PC
#  de 4 GB de RAM com processador ARM64)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
CATALOGO = [
    ("Qwen 2.5 Turbo",        "qwen2.5:0.5b",     400,  100, "RECOMENDADO"),
    ("Qwen 3 Mini",           "qwen3:0.6b",       500,  100, "RECOMENDADO"),
    ("SmolLM2 RÃ¡pida",        "smollm2:360m",     300,  100, "LEVEZINHA"),
    ("Llama 3.2 (1B)",        "llama3.2:1b",      1300,  95, "Ã“TIMA ESCOLHA"),
    ("Qwen 2.5 (1.5B)",       "qwen2.5:1.5b",     1000,  90, "FUNCIONA BEM"),
    ("DeepSeek R1 (1.5B)",    "deepseek-r1:1.5b", 1100,  85, "RACIOCÃNIO"),
    ("Gemma 3 (1B) do Google","gemma3:1b",        900,   85, "MODERNA"),
    ("Qwen 2.5 (3B)",         "qwen2.5:3b",       1900,  60, "LENTA MAS OK"),
    ("Llama 3.2 (3B)",        "llama3.2:3b",      2000,  55, "NO LIMITE"),
    ("Phi-3.5 Mini",          "phi3.5:3.8b",      2200,  50, "NO LIMITE"),
    ("Gemma 3 (4B)",          "gemma3:4b",        3300,  30, "MUITO LENTA"),
    ("Mistral (7B)",          "mistral:7b",       4100,  10, "TRAVA O PC"),
    ("Llama 3.1 (8B)",        "llama3.1:8b",      4700,   5, "TRAVA O PC"),
]

SITES_PADRAO = [
    ("Google",    "https://www.google.com"),
    ("YouTube",   "https://www.youtube.com"),
    ("WikipÃ©dia", "https://pt.wikipedia.org"),
]

def cfg_padrao():
    return {"tema": "escuro", "modelo": None, "chave_nuvem": None,
            "modelo_nuvem": "meta-llama/llama-3.3-70b-instruct:free",
            "sites": [list(s) for s in SITES_PADRAO]}

def carregar_cfg():
    try:
        with open(ARQ_CONFIG, encoding="utf-8") as f:
            c = cfg_padrao(); c.update(json.load(f)); return c
    except Exception:
        return cfg_padrao()

def salvar_cfg(cfg):
    with open(ARQ_CONFIG, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)

CFG = carregar_cfg()

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  MEMÃ“RIA DE VERDADE (o que o Jarvis sabe de vocÃª)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def carregar_memoria():
    try:
        with open(ARQ_MEMORIA, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def salvar_memoria_lista(lista):
    with open(ARQ_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(lista[-60:], f, ensure_ascii=False, indent=1)

def lembrar(fato):
    fato = str(fato).strip()
    if fato and fato not in carregar_memoria():
        salvar_memoria_lista(carregar_memoria() + [fato])

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  LEMBRETES (agenda do Jarvis)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def carregar_lembretes():
    try:
        with open(ARQ_LEMBRETES, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def salvar_lembretes(lista):
    with open(ARQ_LEMBRETES, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=1)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  LISTA DE TAREFAS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
ARQ_TAREFAS = os.path.join(PASTA_BASE, "tarefas.json")

def carregar_tarefas():
    try:
        with open(ARQ_TAREFAS, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def salvar_tarefas(lista):
    with open(ARQ_TAREFAS, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=1)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  INTERFACE (cores, banner, perguntas)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def cor(nome):   return "\033[" + TEMAS[CFG["tema"]][nome] + "m"
def fim():       return "\033[0m"

def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def titulo(texto):
    return f"{cor('primario')}â—† {texto}{fim()}"

def ok(texto):    return f"{cor('ok')}{texto}{fim()}"
def erro(texto):  return f"{cor('erro')}{texto}{fim()}"
def aviso(texto): return f"{cor('aviso')}{texto}{fim()}"
def dim(texto):   return f"{cor('dim')}{texto}{fim()}"

def banner():
    limpar()
    t = CFG["tema"]
    print(f"""{cor('primario')}   â–ˆâ–ˆâ•—â–ˆâ–ˆâ–ˆâ•—   â–ˆâ–ˆâ–ˆâ•—â•šâ•â•—â–ˆâ–ˆâ•— â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•— â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•— â–ˆâ–ˆâ•—   â–ˆâ–ˆâ•—â–ˆâ–ˆâ•—â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—
   â–ˆâ–ˆâ•‘â–ˆâ–ˆâ–ˆâ–ˆâ•— â–ˆâ–ˆâ–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•—â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•—â–ˆâ–ˆâ•‘   â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â•â•â•â•â•
   â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â–ˆâ–ˆâ–ˆâ–ˆâ•”â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•‘â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•”â•â–ˆâ–ˆâ•‘   â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•—
   â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘â•šâ–ˆâ–ˆâ•”â•â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•”â•â•â–ˆâ–ˆâ•—â•šâ–ˆâ–ˆâ•— â–ˆâ–ˆâ•”â•â–ˆâ–ˆâ•‘â•šâ•â•â•â•â–ˆâ–ˆâ•‘
   â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘ â•šâ•â• â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘  â–ˆâ–ˆâ•‘â–ˆâ–ˆâ•‘  â–ˆâ–ˆâ•‘ â•šâ–ˆâ–ˆâ–ˆâ–ˆâ•”â• â–ˆâ–ˆâ•‘â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ•‘
   â•šâ•â•â•šâ•â•     â•šâ•â•â•šâ•â•â•šâ•â•â•šâ•â•  â•šâ•â•â•šâ•â•  â•šâ•â•  â•šâ•â•â•â•  â•šâ•â•â•šâ•â•â•â•â•â•â•{fim()}""")
    print(f"  {dim('Seu assistente de IA 100% seu â€” offline, sem limites e sem custo')}\n")

def perguntar(texto):
    try:
        return input(f"{cor('destaque')}â¯ {fim()}{texto}").strip()
    except (KeyboardInterrupt, EOFError):
        return "sair"

def pedir_permisso(texto):
    """Pergunta s/n com resposta padrÃ£o NÃƒO (seguranÃ§a)."""
    r = input(f"{cor('aviso')}? {fim()}{texto} {dim('[s/N]')}: ").strip().lower()
    return r in ("s", "si", "sim", "y", "yes")

def linha(n=58):
    print(dim("â”€" * n))

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  OLLAMA: DETECÃ‡ÃƒO, INSTALAÃ‡ÃƒO E SERVIDOR
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def achar_ollama():
    exe = shutil.which("ollama")
    if exe:
        return exe
    candidato = os.path.join(os.environ.get("LOCALAPPDATA", ""),
                             "Programs", "Ollama", "ollama.exe")
    if os.path.exists(candidato):
        return candidato
    return None

def servidor_no_ar():
    try:
        with urllib.request.urlopen("http://localhost:11434/api/version", timeout=2):
            return True
    except Exception:
        return False

def iniciar_servidor(exe):
    if servidor_no_ar():
        return True
    print(dim("âš™ Ligando o motor da IA..."))
    subprocess.Popen([exe, "serve"], stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL, creationflags=0x08000000)
    for _ in range(10):
        time.sleep(1)
        if servidor_no_ar():
            return True
    return False

def instalar_ollama():
    """InstalaÃ§Ã£o com PERMISSÃƒO AVANÃ‡ADA: mostra tudo antes."""
    print()
    linha()
    print(titulo("INSTALAÃ‡ÃƒO DO MOTOR (Ollama) â€” PERMISSÃƒO AVANÃ‡ADA"))
    linha()
    print("  O que serÃ¡ feito no seu PC:")
    print(f"   {dim('1.')} Baixar o instalador oficial {ok('Ollama (ARM64)')}")
    print(f"   {dim('2.')} Tamanho do download: {aviso('~700 MB a 1 GB')}")
    print(f"   {dim('3.')} Instalar em: {dim(os.path.join(os.environ.get('LOCALAPPDATA',''), 'Programs', 'Ollama'))}")
    print(f"   {dim('4.')} EspaÃ§o total depois, com IAs instaladas: {aviso('pode passar de 5 GB')}")
    print(f"   {dim('5.')} Depois disso o programa fica {ok('100% offline')}")
    linha()
    if not pedir_permisso("AUTORIZA a instalaÃ§Ã£o?"):
        print(erro("  InstalaÃ§Ã£o cancelada. Sem o motor, sÃ³ o modo nuvem funciona."))
        return False
    print(dim("â¬‡ Baixando e instalando o Ollama (isso pode demorar alguns minutos)..."))
    try:
        codigo = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "irm https://ollama.com/install.ps1 | iex"],
        ).returncode
    except Exception as e:
        print(erro(f"  Falha no download: {e}"))
        return False
    exe = achar_ollama()
    if exe:
        print(ok("  âœ” Ollama instalado com sucesso!"))
        return iniciar_servidor(exe)
    print(aviso("  Se o Windows pedir confirmaÃ§Ã£o, clique em SIM."))
    return False

def listar_modelos_instalados(exe):
    try:
        r = subprocess.run([exe, "list"], capture_output=True, text=True,
                           timeout=20, encoding="utf-8", errors="replace")
        nomes = []
        for l in r.stdout.splitlines()[1:]:
            p = l.split()
            if p:
                nomes.append(p[0])
        return nomes
    except Exception:
        return []

def espaco_livre_mb():
    return shutil.disk_usage(PASTA_BASE).free // (1024 * 1024)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  TELA DE SELEÃ‡ÃƒO DE IAs (a vitrine!)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def barra(chance):
    cheio = chance // 10
    cor_barra = cor("ok") if chance >= 70 else (cor("aviso") if chance >= 40 else cor("erro"))
    return f"{cor_barra}{'â–ˆ' * cheio}{'â–‘' * (10 - cheio)}{fim()}"

def tela_selecao(exe):
    instaladas = listar_modelos_instalados(exe) if exe else []
    while True:
        banner()
        linha()
        print(titulo("QUAL IA VOCÃŠ DESEJA INSTALAR?"))
        linha()
        for i, (apelido, modelo, mb, chance, tag) in enumerate(CATALOGO, 1):
            marca = ok("âœ” jÃ¡ instalada") if modelo in instaladas else dim(f"~{mb//1000 or 1} GB" if mb >= 1000 else f"~{mb} MB")
            selo = ""
            if chance >= 95 and "RECOMENDADO" in tag:
                selo = ok("  â† RECOMENDADA")
            elif chance <= 30:
                selo = erro("  â›” NÃƒO INSTALE")
            print(f"  {cor('destaque')}[{i:>2}]{fim()} {apelido:<24} {barra(chance)} "
                  f"{cor('aviso') if chance < 70 else cor('ok')}{chance:>3}%{fim()} {dim(tag):<18} {marca}{selo}")
        linha()
        print(dim("  NÃºmero = instalar  |  [a] atualizar lista  |  [0] usar IA jÃ¡ configurada  |  [s] sair"))
        r = perguntar("")
        if r == "s":
            return None
        if r == "0":
            return CFG.get("modelo")
        if r == "a":
            continue
        if r.isdigit() and 1 <= int(r) <= len(CATALOGO):
            apelido, modelo, mb, chance, tag = CATALOGO[int(r) - 1]
            livre = espaco_livre_mb()
            print(f"\n  {dim('EspaÃ§o livre no disco:')} {livre:,} MB {dim('| precisa de ~')} {mb} MB")
            if livre < mb:
                print(erro("  âš  Disco quase cheio â€” libere espaÃ§o antes!"))
                input(dim("  Enter para voltar...")); continue
            if chance < 60:
                print(aviso(f"  âš  Esta IA tem sÃ³ {chance}% de chance de rodar bem ({tag})."))
                if not pedir_permisso("Mesmo assim deseja instalar?"):
                    continue
            print(dim(f"\nâ¬‡ Baixando {apelido} ({mb:,} MB)... a barra abaixo Ã© do prÃ³prio Ollama:\n"))
            codigo = subprocess.run([exe, "pull", modelo]).returncode
            if codigo == 0 and modelo in listar_modelos_instalados(exe):
                CFG["modelo"] = modelo; salvar_cfg(CFG)
                print(ok(f"\n  âœ” {apelido} instalada e configurada como sua IA padrÃ£o!"))
                time.sleep(1.5)
                return modelo
            print(erro("\n  âœ˜ O download falhou. Verifique a internet e tente de novo."))
            time.sleep(1.5)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  INTERNET / MODO HÃBRIDO
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def tem_internet():
    try:
        socket.create_connection(("ollama.com", 443), timeout=2).close()
        return True
    except Exception:
        return False

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  FERRAMENTAS DO JARVIS (arquivos, comandos, git)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
COMANDOS_PROIBIDOS = ["format", "shutdown", "del ", "rd ", "rmdir", "remove-item",
                      "reg ", "taskkill", "diskpart", "cipher", "vssadmin",
                      "bcdedit", "net user", "attrib -h"]

def caminho_seguro(caminho):
    caminho = caminho.strip().strip('"')
    if not os.path.isabs(caminho):
        caminho = os.path.join(PASTA_BASE, caminho)
    return os.path.normpath(caminho)

def planejar_edicao(caminho, texto_antigo, texto_novo):
    """Prepara uma ediÃ§Ã£o: localiza o trecho e gera o conteÃºdo novo.
       Retorna (alvo, conteudo_novo, erro)."""
    alvo = caminho_seguro(caminho)
    try:
        with open(alvo, encoding="utf-8", errors="replace") as f:
            conteudo = f.read()
    except Exception as e:
        return alvo, None, f"Erro ao ler: {e}"
    n = conteudo.count(texto_antigo)
    if n != 1:
        return alvo, None, (f"O texto antigo aparece {n} vez(es) no arquivo â€” "
                             "precisa ser exatamente 1. Inclua mais linhas de contexto.")
    return alvo, conteudo.replace(texto_antigo, texto_novo), None

def aplicar_edicao(alvo, conteudo_novo):
    """Salva a ediÃ§Ã£o criando um backup .bak antes."""
    with open(alvo + ".bak", "w", encoding="utf-8") as f:
        with open(alvo, encoding="utf-8", errors="replace") as orig:
            f.write(orig.read())
    with open(alvo, "w", encoding="utf-8") as f:
        f.write(conteudo_novo)
    return f"Arquivo editado: {alvo} (backup salvo em {alvo}.bak)"

def t_criar_arquivo(caminho, conteudo):
    alvo = caminho_seguro(caminho)
    dentro = PASTA_BASE.lower() in alvo.lower()
    if not dentro and not pedir_permisso(f"Criar arquivo FORA da pasta do projeto: {alvo}?"):
        return "Cancelado pelo usuÃ¡rio."
    os.makedirs(os.path.dirname(alvo), exist_ok=True)
    with open(alvo, "w", encoding="utf-8") as f:
        f.write(conteudo)
    return f"Arquivo criado: {alvo} ({len(conteudo)} caracteres)."

def t_ler_arquivo(caminho):
    alvo = caminho_seguro(caminho)
    try:
        with open(alvo, encoding="utf-8", errors="replace") as f:
            return f.read(4000)
    except Exception as e:
        return f"Erro ao ler: {e}"

def t_abrir_site(url):
    """Abre um site no navegador."""
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    return f"Site aberto no navegador: {url}"

def t_ler_site(url):
    """LÃª o conteÃºdo de um site e devolve o texto para interpretaÃ§Ã£o."""
    import re
    if not url.startswith("http"):
        url = "https://" + url
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=20) as r:
            html = r.read(200000).decode("utf-8", errors="replace")
    except Exception as e:
        return f"Erro ao acessar o site: {e}"
    html = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", html)
    texto = re.sub(r"<[^>]+>", " ", html)
    texto = re.sub(r"\s+", " ", texto).strip()
    return f"ConteÃºdo de {url}:\n" + texto[:4000]

def t_tarefas(acao, texto, numero):
    """Lista de tarefas: listar, adicionar, concluir, apagar."""
    tarefas = carregar_tarefas()
    acao = str(acao).lower().strip()
    if acao == "listar":
        if not tarefas:
            return "Nenhuma tarefa na lista."
        linhas = []
        for i, t in enumerate(tarefas):
            marca = "âœ”" if t.get("feita") else "â¬œ"
            linhas.append(f"{i}. {marca} {t['texto']}")
        return "Tarefas:\n" + "\n".join(linhas)
    if acao == "adicionar":
        texto = str(texto).strip()
        if not texto:
            return "Tarefa vazia."
        tarefas.append({"texto": texto, "feita": False})
        salvar_tarefas(tarefas)
        return f"Tarefa adicionada: {texto} (veja na pÃ¡gina Agenda do app)"
    if acao == "concluir":
        try:
            tarefas[int(numero)]["feita"] = True
            salvar_tarefas(tarefas)
            return f"Tarefa {numero} concluÃ­da! âœ…"
        except Exception:
            return "NÃºmero invÃ¡lido. Use tarefas(listar) para ver os nÃºmeros."
    if acao == "apagar":
        try:
            tarefa = tarefas.pop(int(numero))
            salvar_tarefas(tarefas)
            return f"Tarefa apagada: {tarefa['texto']}"
        except Exception:
            return "NÃºmero invÃ¡lido."
    return "AÃ§Ãµes: listar, adicionar, concluir, apagar"

def t_info_pc():
    """InformaÃ§Ãµes do PC do usuÃ¡rio."""
    try:
        import psutil
        bateria = ""
        try:
            b = psutil.sensors_battery()
            if b:
                bateria = f", bateria {int(b.percent)}%" + \
                          (" (carregando)" if b.power_plugged else "")
        except Exception:
            pass
        return ("PC: RAM livre {:.1f} GB de {:.1f} GB ({}% usada), "
                "CPU {}%, {} nÃºcleos{}".format(
                    psutil.virtual_memory().available / 1e9,
                    psutil.virtual_memory().total / 1e9,
                    psutil.virtual_memory().percent,
                    int(psutil.cpu_percent(interval=0.5)),
                    psutil.cpu_count(), bateria))
    except Exception as e:
        return f"NÃ£o consegui ler: {e}"

def t_gerar_senha(tamanho):
    """Cria uma senha forte aleatÃ³ria."""
    import secrets
    import string
    try:
        n = max(8, min(64, int(tamanho)))
    except Exception:
        n = 16
    letras = string.ascii_letters + string.digits + "!@#$%&*?"
    senha = "".join(secrets.choice(letras) for _ in range(n))
    return f"Senha forte ({n} caracteres): {senha}\nGuarde num lugar seguro!"

def t_capturar_tela():
    """Tira uma captura de tela e salva na pasta imagens."""
    from datetime import datetime as _dt
    pasta = TEMP_DIR
    if not os.path.isdir(pasta):
        pasta = os.path.join(PASTA_BASE, "imagens")
        os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(
        pasta, "print_" + _dt.now().strftime("%Y%m%d_%Hh%M%S") + ".png")
    try:
        from PIL import ImageGrab
        ImageGrab.grab().save(caminho)
    except Exception as e:
        return f"NÃ£o consegui capturar: {e}"
    try:
        os.startfile(caminho)
    except Exception:
        pass
    return f"Captura de tela salva e aberta: {caminho}"

def t_calcular(expressao):
    """Faz contas matemÃ¡ticas com seguranÃ§a."""
    import re as _re
    expressao = str(expressao).replace("^", "**").replace(",", ".")
    if not _re.fullmatch(r"[0-9eE+\-*/(). %\t]*", expressao):
        return "SÃ³ sei fazer contas com nÃºmeros (+ - * / % e potÃªncia ^)."
    try:
        resultado = eval(expressao, {"__builtins__": {}}, {})
        return f"{expressao.strip()} = {resultado}"
    except Exception:
        return "NÃ£o consegui calcular. Exemplo: (15 + 7) * 2"

def t_pesquisar_web(consulta):
    """Abre a pesquisa do Google no navegador."""
    import urllib.parse
    consulta = str(consulta).strip()
    if not consulta:
        return "Nada para pesquisar."
    url = "https://www.google.com/search?q=" + urllib.parse.quote(consulta)
    webbrowser.open(url)
    return f"Pesquisa aberta no navegador: '{consulta}'"

def t_salvar_memoria(fato):
    """Memoriza uma informaÃ§Ã£o sobre o usuÃ¡rio, para sempre."""
    fato = str(fato).strip()
    if not fato:
        return "NÃ£o informou nada para memorizar."
    if fato in carregar_memoria():
        return f"Eu jÃ¡ sabia isso: {fato}"
    lembrar(fato)
    return f"Memorizado para sempre: {fato}"

def t_ver_memoria():
    """Devolve tudo o que o Jarvis sabe sobre o usuÃ¡rio."""
    mem = carregar_memoria()
    if not mem:
        return "Ainda nÃ£o sei nada sobre o usuÃ¡rio. Pergunte e memorize!"
    return "O que eu sei sobre o usuÃ¡rio:\n- " + "\n- ".join(mem)

def t_criar_lembrete(quando, texto):
    """Cria um lembrete que aparece na tela na hora marcada."""
    import re
    from datetime import timedelta
    s = str(quando).strip().lower()
    agora = datetime.now()
    dt = None
    try:                       # formato completo: 2026-11-17T20:00
        dt = datetime.fromisoformat(str(quando).strip())
    except ValueError:
        pass
    if dt is None:             # em X minutos / em X horas
        m = re.search(r"em\s+(\d+)\s*(min|hora)", s)
        if m:
            n = int(m.group(1))
            dt = agora + timedelta(minutes=n if "min" in m.group(2) else n * 60)
    if dt is None:             # (amanhÃ£|depois de amanhÃ£)? HH:MM ou HHh
        dias = 0
        if "depois de amanh" in s:
            dias = 2
        elif "amanh" in s:
            dias = 1
        m = re.search(r"(\d{1,2})[:h](\d{2})", s)
        if m:
            dt = (agora + timedelta(days=dias)).replace(
                hour=int(m.group(1)), minute=int(m.group(2)), second=0,
                microsecond=0)
            if dt <= agora and not dias:
                dt += timedelta(days=1)
    if dt is None:
        return ("NÃ£o entendi a hora. Use '2026-11-17T20:00', "
                "'amanhÃ£ 20:00' ou 'em 10 minutos'.")
    lembretes = carregar_lembretes()
    lembretes.append({"quando": dt.isoformat(timespec="seconds"),
                      "quando_ts": dt.timestamp(),
                      "texto": str(texto).strip() or "Lembrete"})
    salvar_lembretes(lembretes)
    return (f"Lembrete criado para {dt.strftime('%d/%m Ã s %H:%M')}: "
            f"{texto}. O alarme vai tocar sozinho.")

def t_abrir_arquivo(caminho):
    """Abre ou interpreta um arquivo em qualquer formato."""
    alvo = caminho_seguro(caminho)
    if not os.path.exists(alvo):
        return f"FALHA: arquivo nÃ£o encontrado: {alvo}"
    ext = os.path.splitext(alvo)[1].lower()
    if ext in (".html", ".htm"):
        webbrowser.open("file:///" + alvo.replace("\\", "/"))
        return f"Arquivo aberto no navegador: {alvo}"
    if ext in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".pdf", ".docx",
               ".xlsx", ".pptx", ".mp3", ".mp4", ".wav"):
        os.startfile(alvo)
        return f"Arquivo aberto no programa padrÃ£o: {alvo}"
    try:
        with open(alvo, encoding="utf-8", errors="replace") as f:
            return f"ConteÃºdo de {alvo} ({ext or 'sem extensÃ£o'}):\n" + f.read(4000)
    except Exception as e:
        return f"Erro ao ler: {e}"

def t_listar_pasta(caminho="."):
    alvo = caminho_seguro(caminho)
    try:
        itens = os.listdir(alvo)
        return "\n".join(("ðŸ“ " if os.path.isdir(os.path.join(alvo, i)) else "ðŸ“„ ") + i
                         for i in itens[:50]) or "(pasta vazia)"
    except Exception as e:
        return f"Erro: {e}"

def _prioridade_baixa(proc):
    try:
        import ctypes
        h = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, proc.pid)
        ctypes.windll.kernel32.SetPriorityClass(h, 0x00004000)  # BELOW_NORMAL
    except Exception:
        pass

def t_rodar_comando(comando):
    baixo = comando.lower()
    if any(p in baixo for p in COMANDOS_PROIBIDOS):
        return "BLOQUEADO: comando perigoso nÃ£o Ã© permitido."
    print(f"\n  {aviso('âš¡ O Jarvis quer executar:')} {cor('texto')}{comando}{fim()}")
    if not pedir_permisso("Permite executar?"):
        return "Cancelado pelo usuÃ¡rio."
    try:
        r = subprocess.run(comando, shell=True, capture_output=True, text=True,
                           timeout=120, encoding="utf-8", errors="replace",
                           cwd=PASTA_BASE)
        saida = (r.stdout or "") + (("\n[erro]\n" + r.stderr) if r.stderr else "")
        return (saida or "(sem saÃ­da)")[:4000]
    except Exception as e:
        return f"Erro: {e}"

def t_editar_arquivo(caminho, texto_antigo, texto_novo):
    alvo, conteudo_novo, erro = planejar_edicao(caminho, texto_antigo, texto_novo)
    if erro:
        return f"FALHA: {erro}"
    print(f"\n  {aviso('âœ O Jarvis quer editar:')} {cor('texto')}{alvo}{fim()}")
    print(f"  {dim('ANTES:')} {cor('erro')}{texto_antigo[:150]!r}{fim()}")
    print(f"  {dim('DEPOIS:')} {cor('ok')}{texto_novo[:150]!r}{fim()}")
    if not pedir_permisso("Confirma a ediÃ§Ã£o?"):
        return "Cancelado pelo usuÃ¡rio."
    return aplicar_edicao(alvo, conteudo_novo)

def t_git(acao, mensagem=""):
    git = shutil.which("git")
    if not git:
        return "Git nÃ£o estÃ¡ instalado neste PC."
    try:
        if acao == "status":
            args = [git, "status", "--short", "-b"]
        elif acao == "log":
            args = [git, "log", "--oneline", "-10"]
        elif acao == "init":
            args = [git, "init"]
        elif acao == "commit":
            args = [git, "commit", "-m", mensagem or "commit do Jarvis"]
            subprocess.run([git, "add", "-A"], cwd=PASTA_BASE,
                           capture_output=True, text=True)
        else:
            return f"AÃ§Ã£o git desconhecida: {acao}"
        r = subprocess.run(args, cwd=PASTA_BASE, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        return (r.stdout or r.stderr or "(sem saÃ­da)")[:2000]
    except Exception as e:
        return f"Erro: {e}"

FERRAMENTAS = [
    {"type": "function", "function": {"name": "criar_arquivo",
        "description": "Cria ou sobrescreve um arquivo de texto. Use SEMPRE que o usuÃ¡rio pedir para criar algo.",
        "parameters": {"type": "object", "properties": {
            "caminho": {"type": "string", "description": "caminho do arquivo, relativo Ã  pasta do projeto"},
            "conteudo": {"type": "string", "description": "conteÃºdo completo do arquivo"}},
            "required": ["caminho", "conteudo"]}}},
    {"type": "function", "function": {"name": "editar_arquivo",
        "description": "EDITA um trecho de um arquivo existente (tipo buscar e substituir). Use para mudanÃ§as pequenas e precisas, inclusive para editar o prÃ³prio cÃ³digo do programa se o usuÃ¡rio pedir.",
        "parameters": {"type": "object", "properties": {
            "caminho": {"type": "string"},
            "texto_antigo": {"type": "string", "description": "trecho EXATO que deve ser substituÃ­do (copie do arquivo, com contexto suficiente para ser Ãºnico)"},
            "texto_novo": {"type": "string", "description": "texto que substitui o trecho antigo"}},
            "required": ["caminho", "texto_antigo", "texto_novo"]}}},
    {"type": "function", "function": {"name": "abrir_site",
        "description": "Abre um site no navegador do usuÃ¡rio.",
        "parameters": {"type": "object", "properties": {
            "url": {"type": "string"}}, "required": ["url"]}}},
    {"type": "function", "function": {"name": "ler_site",
        "description": "LÃª o conteÃºdo de um site e retorna o texto, para vocÃª saber o que estÃ¡ acontecendo nele.",
        "parameters": {"type": "object", "properties": {
            "url": {"type": "string"}}, "required": ["url"]}}},
    {"type": "function", "function": {"name": "abrir_arquivo",
        "description": "Abre ou interpreta um arquivo em qualquer formato: .html/.htm abre no navegador, imagens/pdf abrem no programa padrÃ£o, e .py/.txt/.md/.json/.csv retornam o conteÃºdo para interpretaÃ§Ã£o.",
        "parameters": {"type": "object", "properties": {
            "caminho": {"type": "string"}}, "required": ["caminho"]}}},
    {"type": "function", "function": {"name": "ler_arquivo",
        "description": "LÃª o conteÃºdo de um arquivo.",
        "parameters": {"type": "object", "properties": {
            "caminho": {"type": "string"}}, "required": ["caminho"]}}},
    {"type": "function", "function": {"name": "listar_pasta",
        "description": "Lista os arquivos de uma pasta.",
        "parameters": {"type": "object", "properties": {
            "caminho": {"type": "string"}}, "required": []}}},
    {"type": "function", "function": {"name": "rodar_comando",
        "description": "Executa um comando do Windows (o usuÃ¡rio confirma antes).",
        "parameters": {"type": "object", "properties": {
            "comando": {"type": "string"}}, "required": ["comando"]}}},
    {"type": "function", "function": {"name": "git",
        "description": "Usa o Git: acoes = status, log, commit, init.",
        "parameters": {"type": "object", "properties": {
            "acao": {"type": "string", "enum": ["status", "log", "commit", "init"]},
            "mensagem": {"type": "string", "description": "mensagem do commit"}}, "required": ["acao"]}}},
    {"type": "function", "function": {"name": "tarefas",
        "description": "Gerencia a lista de tarefas do usuÃ¡rio. acao: listar, adicionar, concluir, apagar. Para adicionar, mande o texto; para concluir/apagar, mande o numero (da listagem).",
        "parameters": {"type": "object", "properties": {
            "acao": {"type": "string", "enum": ["listar", "adicionar", "concluir", "apagar"]},
            "texto": {"type": "string"},
            "numero": {"type": "string"}}, "required": ["acao"]}}},
    {"type": "function", "function": {"name": "info_pc",
        "description": "Mostra RAM livre, uso de CPU, nÃºcleos e bateria do PC do usuÃ¡rio.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "gerar_senha",
        "description": "Cria uma senha forte aleatÃ³ria e segura.",
        "parameters": {"type": "object", "properties": {
            "tamanho": {"type": "string", "description": "ex: 16"}}}}},
    {"type": "function", "function": {"name": "capturar_tela",
        "description": "Tira uma captura de tela do PC, salva e abre para o usuÃ¡rio.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "calcular",
        "description": "Faz uma conta matemÃ¡tica exata (soma, subtraÃ§Ã£o, multiplicaÃ§Ã£o, divisÃ£o, potÃªncia com ^). Use sempre para cÃ¡lculos, nÃ£o calcule de cabeÃ§a.",
        "parameters": {"type": "object", "properties": {
            "expressao": {"type": "string", "description": "ex: (15 + 7) * 2"}}, "required": ["expressao"]}}},
    {"type": "function", "function": {"name": "pesquisar_web",
        "description": "Abre a pesquisa do Google no navegador com o que o usuÃ¡rio quer saber.",
        "parameters": {"type": "object", "properties": {
            "consulta": {"type": "string"}}, "required": ["consulta"]}}},
    {"type": "function", "function": {"name": "salvar_memoria",
        "description": "Memoriza para sempre um fato sobre o usuÃ¡rio: nome, escola, gostos, projetos, matÃ©rias ou preferÃªncias (ex: 'prefere respostas curtas'). Use SEMPRE que ele contar algo pessoal ou expressar uma preferÃªncia.",
        "parameters": {"type": "object", "properties": {
            "fato": {"type": "string"}}, "required": ["fato"]}}},
    {"type": "function", "function": {"name": "ver_memoria",
        "description": "LÃª o que vocÃª jÃ¡ sabe sobre o usuÃ¡rio.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "criar_lembrete",
        "description": "Cria um lembrete que toca sozinho na hora marcada (pop-up + voz). 'quando' aceita '2026-11-17T20:00', 'amanhÃ£ 20:00' ou 'em 10 minutos'.",
        "parameters": {"type": "object", "properties": {
            "quando": {"type": "string"},
            "texto": {"type": "string"}}, "required": ["quando", "texto"]}}},
]

EXECUTAR = {
    "criar_arquivo": lambda a: t_criar_arquivo(a.get("caminho", ""), a.get("conteudo", "")),
    "editar_arquivo": lambda a: t_editar_arquivo(a.get("caminho", ""), a.get("texto_antigo", ""), a.get("texto_novo", "")),
    "abrir_arquivo": lambda a: t_abrir_arquivo(a.get("caminho", "")),
    "abrir_site":    lambda a: t_abrir_site(a.get("url", "")),
    "ler_site":      lambda a: t_ler_site(a.get("url", "")),
    "ler_arquivo":   lambda a: t_ler_arquivo(a.get("caminho", ".")),
    "listar_pasta":  lambda a: t_listar_pasta(a.get("caminho", ".")),
    "rodar_comando": lambda a: t_rodar_comando(a.get("comando", "")),
    "git":           lambda a: t_git(a.get("acao", "status"), a.get("mensagem", "")),
    "salvar_memoria": lambda a: t_salvar_memoria(a.get("fato", "")),
    "ver_memoria":   lambda a: t_ver_memoria(),
    "criar_lembrete": lambda a: t_criar_lembrete(a.get("quando", ""), a.get("texto", "")),
    "calcular":      lambda a: t_calcular(a.get("expressao", "")),
    "pesquisar_web": lambda a: t_pesquisar_web(a.get("consulta", "")),
    "tarefas":       lambda a: t_tarefas(a.get("acao", "listar"),
                                         a.get("texto", ""),
                                         a.get("numero", "")),
    "info_pc":       lambda a: t_info_pc(),
    "gerar_senha":   lambda a: t_gerar_senha(a.get("tamanho", "16")),
    "capturar_tela": lambda a: t_capturar_tela(),
}

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  CÃ‰REBRO: CHAMADA Ã€ IA (local ou nuvem)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def sistema_prompt():
    """Personalidade + memÃ³ria: o Jarvis sabe quem vocÃª Ã©."""
    nome = CFG.get("nome_user") or "chefe"
    agora = datetime.now()
    dias_sem = ("segunda", "terÃ§a", "quarta", "quinta", "sexta", "sÃ¡bado",
                "domingo")
    texto = (
        f"VocÃª Ã© o MINI-JARVIS, uma IA de verdade â€” assistente pessoal leal, "
        f"estilo Jarvis do Homem de Ferro. VocÃª chama o usuÃ¡rio de {nome}. "
        "Responda SEMPRE em portuguÃªs do Brasil, com simpatia e frases curtas. "
        f"Agora sÃ£o {agora.strftime('%H:%M')} de {dias_sem[agora.weekday()]}, "
        f"{agora.strftime('%d/%m/%Y')} â€” use isso para perguntas de hora/data. "
        "Para contas matemÃ¡ticas, USE calcular. Para o usuÃ¡rio pesquisar algo "
        "na internet, USE pesquisar_web. Para a lista de tarefas dele (ex: "
        "'adiciona tarefa...'), USE tarefas. Se ele perguntar sobre o PC "
        "(RAM, CPU, bateria), USE info_pc. Para ele pedir senha forte, USE "
        "gerar_senha. Para print de tela, USE capturar_tela. "
        "VocÃª Ã© especialista em CRIAR e EDITAR ARQUIVOS: para algo novo, USE "
        "criar_arquivo; para mudar um trecho de arquivo existente (inclusive o "
        "cÃ³digo deste prÃ³prio programa), USE editar_arquivo. Para tarefas "
        "grandes (como criar um site ou projeto), divida em passos e execute "
        "um por um com as ferramentas, contando o progresso.\n"
        "QUANDO O USUÃRIO CONTAR ALGO PESSOAL (nome, escola, gostos, projetos, "
        "matÃ©rias) OU EXPRESSAR UMA PREFERÃŠNCIA (ex: 'prefiro respostas "
        "curtas'), USE salvar_memoria na hora. Se precisar saber o que jÃ¡ "
        "sabe dele, USE ver_memoria. Se ele pedir um lembrete, USE "
        "criar_lembrete e confirme a hora criada."
    )
    mem = carregar_memoria()
    if mem:
        texto += "\n\nO que vocÃª jÃ¡ sabe sobre ele:\n- " + "\n- ".join(mem[-30:])
    return texto

# compatibilidade com o modo terminal
SISTEMA = sistema_prompt()

def cortar_historico(mensagens, manter=10):
    return [m for m in mensagens if m["role"] == "system"] + \
           [m for m in mensagens if m["role"] != "system"][-manter:]

def chamada_local(mensagens, modelo):
    corpo = {"model": modelo, "messages": mensagens, "stream": False,
             "tools": FERRAMENTAS,
             "options": {"num_ctx": 2048, "num_predict": 400},
             "keep_alive": "2m"}
    req = urllib.request.Request("http://localhost:11434/api/chat",
                                 data=json.dumps(corpo).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        dados = json.loads(r.read().decode("utf-8"))
    return dados.get("message", {})

def chamada_local_stream(mensagens, modelo, ao_receber=None):
    """VersÃ£o em tempo real: chama ao_receber(texto_acumulado) a cada pedaÃ§o."""
    corpo = {"model": modelo, "messages": mensagens, "stream": True,
             "tools": FERRAMENTAS,
             "options": {"num_ctx": 2048, "num_predict": 400},
             "keep_alive": "2m"}
    req = urllib.request.Request("http://localhost:11434/api/chat",
                                 data=json.dumps(corpo).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    fala = ""
    ferramentas = []
    args_parciais = {}
    with urllib.request.urlopen(req, timeout=600) as r:
        for linha in r:
            try:
                pedaco = json.loads(linha.decode("utf-8", errors="replace"))
            except Exception:
                continue
            msg = pedaco.get("message", {})
            texto = msg.get("content", "")
            if texto:
                fala += texto
                if ao_receber:
                    ao_receber(fala)
            for tc in msg.get("tool_calls", []):
                fn = tc.get("function", {})
                nome = fn.get("name", "")
                args = fn.get("arguments", "")
                if isinstance(args, str):
                    args_parciais[nome] = args_parciais.get(nome, "") + args
                else:
                    args_parciais[nome] = args
                ferramentas = [{"function": {"name": n, "arguments": a}}
                               for n, a in args_parciais.items()]
            if pedaco.get("done"):
                break
    saida = {"content": fala}
    if ferramentas:
        saida["tool_calls"] = ferramentas
    return saida

def chamada_nuvem(mensagens, cfg):
    corpo = {"model": cfg.get("modelo_nuvem"), "messages": mensagens,
             "tools": FERRAMENTAS}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
                                 data=json.dumps(corpo).encode("utf-8"),
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer " + cfg["chave_nuvem"]})
    with urllib.request.urlopen(req, timeout=120) as r:
        dados = json.loads(r.read().decode("utf-8"))
    msg = dados["choices"][0]["message"]
    saida = {"content": msg.get("content", "")}
    if msg.get("tool_calls"):
        saida["tool_calls"] = [{"function": {"name": t["function"]["name"],
            "arguments": json.loads(t["function"]["arguments"] or "{}")}}
            for t in msg["tool_calls"]]
    return saida

def chamada_nuvem_stream(mensagens, cfg, ao_receber=None):
    """Nuvem EM TEMPO REAL (SSE): palavras aparecem desde o 1Âº segundo."""
    corpo = {"model": cfg.get("modelo_nuvem"), "messages": mensagens,
             "tools": FERRAMENTAS, "stream": True}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
                                 data=json.dumps(corpo).encode("utf-8"),
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer " + cfg["chave_nuvem"],
                                          "HTTP-Referer": "https://github.com/bernardoalvescaetano888-glitch/MINI-JARVIS",
                                          "X-Title": "MINI-JARVIS"})
    fala = ""
    ferramentas = []
    args_parciais = {}
    with urllib.request.urlopen(req, timeout=120) as r:
        for linha in r:
            linha = linha.decode("utf-8", errors="replace").strip()
            if not linha.startswith("data:"):
                continue
            dados = linha[5:].strip()
            if dados == "[DONE]":
                break
            try:
                pedaco = json.loads(dados)
            except Exception:
                continue
            delta = pedaco.get("choices", [{}])[0].get("delta", {})
            texto = delta.get("content") or ""
            if texto:
                fala += texto
                if ao_receber:
                    ao_receber(fala)
            for tc in delta.get("tool_calls") or []:
                fn = tc.get("function", {}) or {}
                chave = tc.get("index", 0)
                nome = fn.get("name", "")
                if nome:
                    args_parciais.setdefault(chave, {"name": nome, "args": ""})
                if chave in args_parciais:
                    if nome:
                        args_parciais[chave]["name"] = nome
                    args_parciais[chave]["args"] += fn.get("arguments") or ""
    for chave, tc in args_parciais.items():
        ferramentas.append({"function": {"name": tc["name"],
                                          "arguments": tc["args"] or "{}"}})
    saida = {"content": fala}
    if ferramentas:
        saida["tool_calls"] = ferramentas
    return saida

def pensar(mensagens, cfg, online):
    if online and cfg.get("chave_nuvem"):
        try:
            return chamada_nuvem(cortar_historico(mensagens), cfg), "â˜"
        except Exception:
            pass  # cai pro modo local silenciosamente
    return chamada_local(cortar_historico(mensagens), cfg["modelo"]), "âš¡"

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  CHATS SALVOS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def novo_chat():
    os.makedirs(PASTA_CHATS, exist_ok=True)
    nome = datetime.now().strftime("chat_%Y-%m-%d_%Hh%M.json")
    return {"arquivo": os.path.join(PASTA_CHATS, nome),
            "mensagens": [{"role": "system", "content": sistema_prompt()}]}

def salvar_chat(chat, modelo):
    dados = {"modelo": modelo, "salvo": datetime.now().isoformat(timespec="seconds"),
             "mensagens": chat["mensagens"]}
    with open(chat["arquivo"], "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def abrir_chat():
    os.makedirs(PASTA_CHATS, exist_ok=True)
    arquivos = sorted(os.listdir(PASTA_CHATS))[-10:]
    if not arquivos:
        print(aviso("  Nenhum chat salvo ainda.")); return None
    for i, a in enumerate(arquivos, 1):
        print(f"  {cor('destaque')}[{i}]{fim()} {a[:-5]}")
    r = perguntar("Qual chat abrir? (nÃºmero / Enter cancela)")
    if r.isdigit() and 1 <= int(r) <= len(arquivos):
        arquivo = os.path.join(PASTA_CHATS, arquivos[int(r) - 1])
        try:
            with open(arquivo, encoding="utf-8") as f:
                dados = json.load(f)
            return {"arquivo": arquivo, "mensagens": dados["mensagens"]}
        except Exception as e:
            print(erro(f"  NÃ£o consegui abrir: {e}"))
    return None

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  PLUGINS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def carregar_plugins():
    plugins = []
    if not os.path.isdir(PASTA_PLUGS):
        return plugins
    for nome in sorted(os.listdir(PASTA_PLUGS)):
        if not nome.endswith(".py") or nome.startswith("_"):
            continue
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "plugin_" + nome[:-3], os.path.join(PASTA_PLUGS, nome))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            plugins.append({"nome": mod.info.get("nome", nome[:-3]),
                            "desc": mod.info.get("desc", ""),
                            "comando": mod.info.get("comando", "/" + nome[:-3]),
                            "executar": mod.executar})
        except Exception as e:
            print(aviso(f"  Plugin {nome} com problema: {e}"))
    return plugins

def rodar_plugin(plugins, comando, chat):
    for p in plugins:
        if comando.lower().startswith(p["comando"]):
            args = comando[len(p["comando"]):].strip()
            try:
                p["executar"](args)
            except Exception as e:
                print(erro(f"  O plugin falhou: {e}"))
            return True
    return False

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  PAINEL LATERAL (sites, plugins, chats, ajustes)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def painel(exe):
    while True:
        print()
        linha()
        print(titulo("PAINEL LATERAL"))
        linha()
        print(f"  ðŸŒ {cor('primario')}SITES{fim()}")
        for i, (nome, url) in enumerate(CFG["sites"], 1):
            print(f"     [{i}] {nome}  {dim(url)}")
        print(f"     [+adicionar] digite: + nome | url")
        print(f"  ðŸ”Œ {cor('primario')}PLUGINS{fim()}")
        for p in PLUGINS:
            print(f"     {p['comando']:<12} {dim(p['desc'])}")
        if not PLUGINS:
            print(dim("     (nenhum â€” coloque .py em plugins/)"))
        print(f"  âš™ {cor('primario')}AJUSTES{fim()}  [t] tema  [m] trocar IA  [v] chave da nuvem")
        linha()
        r = perguntar("")
        if r in ("s", "sair", "x"):
            return
        if r == "t":
            CFG["tema"] = "claro" if CFG["tema"] == "escuro" else "escuro"
            salvar_cfg(CFG); banner()
            print(ok(f"  âœ” Tema {CFG['tema']} ativado!"))
        elif r == "m":
            novo = tela_selecao(exe)
            if novo: return
        elif r == "v":
            chave = perguntar("Chave da API gratuita (openrouter.ai/keys) ou Enter p/ limpar:")
            CFG["chave_nuvem"] = chave or None; salvar_cfg(CFG)
            print(ok("  âœ” Modo nuvem configurado! Com internet, usarei a IA mais inteligente."))
        elif r.startswith("+"):
            try:
                _, resto = r.split("+", 1)
                nome, url = resto.split("|")
                CFG["sites"].append([nome.strip(), url.strip()]); salvar_cfg(CFG)
                print(ok("  âœ” Site adicionado!"))
            except Exception:
                print(erro("  Formato: + nome | url"))
        elif r.isdigit() and 1 <= int(r) <= len(CFG["sites"]):
            webbrowser.open(CFG["sites"][int(r) - 1][1])
            print(dim("  â†’ abrindo no navegador..."))
        elif rodar_plugin(PLUGINS, r, None):
            pass

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  CONVERSA PRINCIPAL
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def conversar(chat, exe):
    modelo = CFG["modelo"]
    while True:
        texto = perguntar("")
        if not texto:
            continue
        if texto in ("sair", "exit", "x"):
            salvar_chat(chat, modelo)
            print(dim("  Chat salvo. AtÃ© logo! ðŸ‘‹"))
            return
        if texto == "limpar":
            limpar(); banner(); continue
        if texto == "painel":
            painel(exe); limpar(); banner(); continue
        if texto == "abrir":
            novo = abrir_chat()
            if novo:
                chat = novo; modelo = CFG["modelo"]
                print(ok("  âœ” Chat retomado!"))
            continue
        if texto == "tema":
            CFG["tema"] = "claro" if CFG["tema"] == "escuro" else "escuro"
            salvar_cfg(CFG); limpar(); banner()
            print(ok(f"  âœ” Tema {CFG['tema']} ativado!")); continue
        if texto == "modelo":
            novo = tela_selecao(exe)
            if novo: modelo = novo
            continue
        if texto.startswith("git "):
            acao = texto.split()[1]
            msg = texto[texto.find(acao) + len(acao):].strip().strip('"')
            print(t_git("commit" if acao == "commit" else acao, msg)); continue
        if rodar_plugin(PLUGINS, texto, chat):
            continue
        # ---- manda pra IA ----
        online = tem_internet()
        modo = ok("ONLINE") if online else aviso("OFFLINE")
        print(f"\n  {dim(f'[jarvis {modo}]')} {dim('pensando...')}")
        chat["mensagens"].append({"role": "user", "content": texto})
        try:
            for _ in range(5):  # atÃ© 5 ferramentas seguidas
                resposta, origem = pensar(chat["mensagens"], CFG, online)
                chamadas = resposta.get("tool_calls")
                fala = resposta.get("content") or ""
                if chamadas:
                    if fala:
                        print(f"\n  {cor('primario')}ðŸ¤–{fim()} {fala}")
                    chat["mensagens"].append({"role": "assistant",
                        "content": fala, "tool_calls": chamadas})
                    for c in chamadas:
                        nome = c["function"]["name"]
                        args = c["function"].get("arguments", {})
                        if isinstance(args, str):
                            args = json.loads(args or "{}")
                        resultado = EXECUTAR.get(nome, lambda a: "ferramenta inexistente")(args)
                        print(f"     {dim('â†’')} {resultado.splitlines()[0][:90]}")
                        chat["mensagens"].append({"role": "tool",
                            "content": str(resultado), "name": nome})
                    continue
                print(f"\n  {cor('primario')}ðŸ¤–{fim()} {fala or '(sem resposta)'}\n")
                chat["mensagens"].append({"role": "assistant", "content": fala})
                break
        except Exception as e:
            print(erro(f"  Erro na IA: {e}"))
        salvar_chat(chat, modelo)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  INÃCIO
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def main():
    global PLUGINS
    PLUGINS = carregar_plugins()

    if "--tela" in sys.argv:          # modo demonstraÃ§Ã£o da vitrine
        tela_selecao(achar_ollama())
        return

    banner()
    linha()
    online = tem_internet()
    estado = ok("ONLINE (hÃ­brido disponÃ­vel)") if online else aviso("100% OFFLINE")
    print(f"  Internet: {estado}")
    linha()

    exe = achar_ollama()
    if not exe:
        if not instalar_ollama():
            print(aviso("  Continuando sem o motor local..."))
            time.sleep(2)
    elif not iniciar_servidor(exe):
        print(erro("  NÃ£o consegui ligar o servidor do Ollama."))

    exe = achar_ollama()
    if exe and not CFG.get("modelo"):
        tela_selecao(exe)
    if not CFG.get("modelo") and not CFG.get("chave_nuvem"):
        print(erro("  Sem IA local e sem chave da nuvem. Configure em painel â†’ [v]."))
        return

    chat = novo_chat()
    print(ok(f"\n  â•â• MINI-JARVIS PRONTO! (IA: {CFG['modelo'] or 'nuvem'}) â•â•"))
    print(dim("  Comandos: painel | abrir | tema | modelo | git status | sair"))
    conversar(chat, exe)

if __name__ == "__main__":
    main()
