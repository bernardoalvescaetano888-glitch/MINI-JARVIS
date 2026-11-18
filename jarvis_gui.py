#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
═══════════════════════════════════════════════════════════════
 MINI-JARVIS 2.2 — Interface profissional (estilo ChatGPT)
═══════════════════════════════════════════════════════════════
 Mensagens do Jarvis em texto limpo • suas em bolha verde
 chips de ferramenta • animação de pensamento • tema duplo
═══════════════════════════════════════════════════════════════
"""

import contextlib
import io
import json
import os
import subprocess
import sys
import threading
import time
import tkinter.messagebox as mbox
import urllib.request
import webbrowser

try:
    import winsound
except Exception:
    winsound = None
from datetime import datetime

import customtkinter as ctk

import jarvis as nucleo

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ══════════════════════════════════════════════════════════════
#  PALETA (tupla = (modo claro, modo escuro))
# ══════════════════════════════════════════════════════════════
LATERAL     = ("#f7f7f8", "#171717")
FUNDO       = ("#fafafa", "#212121")
CARD        = ("#ffffff", "#262627")
CARD_MENU   = ("#ececee", "#2a2a2b")
BOLHA_VOCE  = ("#10a37f", "#10a37f")
CHIP        = ("#e8e8ea", "#26262a")
TXT         = ("gray10",    "#ececf1")
TXT_MEDIO   = ("gray30",    "#b4b4b4")
TXT_FRACO   = ("gray45",    "#8e8e8e")
ACENTO      = "#10a37f"
ACENTO_2    = "#0b8a67"
LARANJA     = ("#b45309", "#f59e0b")
VERMELHO    = ("#dc2626", "#ef4444")
HOVER_ITEM  = ("#e2e2e4", "#2f2f30")

FONTE      = ("Segoe UI", 14)
FONTE_G    = ("Segoe UI", 19, "bold")
FONTE_M    = ("Segoe UI", 13)
FONTE_P    = ("Segoe UI", 11)
FONTE_COD  = ("Consolas", 12)

# ══════════════════════════════════════════════════════════════
#  FERRAMENTAS (com diálogos de permissão)
# ══════════════════════════════════════════════════════════════
def ferramenta_gui(nome, args):
    if nome == "criar_arquivo":
        alvo = nucleo.caminho_seguro(args.get("caminho", ""))
        if nucleo.PASTA_BASE.lower() not in alvo.lower():
            if not mbox.askyesno("Permissão",
                    f"Criar arquivo FORA da pasta do projeto?\n\n{alvo}"):
                return "Cancelado pelo usuário."
        os.makedirs(os.path.dirname(alvo), exist_ok=True)
        with open(alvo, "w", encoding="utf-8") as f:
            f.write(args.get("conteudo", ""))
        return f"Arquivo criado: {alvo}"

    if nome == "editar_arquivo":
        alvo, conteudo_novo, erro = nucleo.planejar_edicao(
            args.get("caminho", ""), args.get("texto_antigo", ""),
            args.get("texto_novo", ""))
        if erro:
            return f"FALHA: {erro}"
        if not mbox.askyesno("Permissão para editar",
                f"O Jarvis quer editar:\n\n{alvo}\n\n"
                f"ANTES:\n{args.get('texto_antigo', '')[:200]}\n\n"
                f"DEPOIS:\n{args.get('texto_novo', '')[:200]}\n\n"
                f"Confirma? (é criado um backup .bak)"):
            return "Cancelado pelo usuário."
        return nucleo.aplicar_edicao(alvo, conteudo_novo)

    if nome == "ler_arquivo":
        alvo = nucleo.caminho_seguro(args.get("caminho", ""))
        try:
            with open(alvo, encoding="utf-8", errors="replace") as f:
                return f.read(4000)
        except Exception as e:
            return f"Erro ao ler: {e}"

    if nome == "listar_pasta":
        alvo = nucleo.caminho_seguro(args.get("caminho", "."))
        try:
            itens = os.listdir(alvo)
            return "\n".join(("📁 " if os.path.isdir(os.path.join(alvo, i)) else "📄 ") + i
                             for i in itens[:50]) or "(pasta vazia)"
        except Exception as e:
            return f"Erro: {e}"

    if nome == "rodar_comando":
        comando = args.get("comando", "")
        if any(p in comando.lower() for p in nucleo.COMANDOS_PROIBIDOS):
            return "BLOQUEADO: comando perigoso."
        if not mbox.askyesno("Permissão",
                f"O Jarvis quer executar:\n\n{comando}\n\nPermite?"):
            return "Cancelado pelo usuário."
        try:
            r = subprocess.run(comando, shell=True, capture_output=True, text=True,
                               timeout=120, encoding="utf-8", errors="replace",
                               cwd=nucleo.PASTA_BASE)
            saida = (r.stdout or "") + (("\n[erro]\n" + r.stderr) if r.stderr else "")
            return (saida or "(sem saída)")[:4000]
        except Exception as e:
            return f"Erro: {e}"

    if nome == "abrir_arquivo":
        alvo = nucleo.caminho_seguro(args.get("caminho", ""))
        if not os.path.exists(alvo):
            return f"FALHA: arquivo não encontrado: {alvo}"
        ext = os.path.splitext(alvo)[1].lower()
        if ext in (".html", ".htm"):
            webbrowser.open("file:///" + alvo.replace("\\", "/"))
            return f"Arquivo aberto no navegador: {alvo}"
        if ext in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".pdf", ".docx",
                   ".xlsx", ".pptx", ".mp3", ".mp4", ".wav"):
            os.startfile(alvo)
            return f"Arquivo aberto no programa padrão: {alvo}"
        try:
            with open(alvo, encoding="utf-8", errors="replace") as f:
                return (f"Conteúdo de {alvo} ({ext or 'sem extensão'}):\n"
                        + f.read(4000))
        except Exception as e:
            return f"Erro ao ler: {e}"

    if nome == "abrir_site":
        return nucleo.t_abrir_site(args.get("url", ""))

    if nome == "ler_site":
        return nucleo.t_ler_site(args.get("url", ""))

    if nome == "git":
        return nucleo.t_git(args.get("acao", "status"), args.get("mensagem", ""))

    if nome == "salvar_memoria":
        return nucleo.t_salvar_memoria(args.get("fato", ""))

    if nome == "ver_memoria":
        return nucleo.t_ver_memoria()

    if nome == "criar_lembrete":
        return nucleo.t_criar_lembrete(args.get("quando", ""),
                                       args.get("texto", ""))

    if nome == "calcular":
        return nucleo.t_calcular(args.get("expressao", ""))

    if nome == "pesquisar_web":
        return nucleo.t_pesquisar_web(args.get("consulta", ""))

    if nome == "tarefas":
        return nucleo.t_tarefas(args.get("acao", "listar"),
                                args.get("texto", ""), args.get("numero", ""))

    if nome == "info_pc":
        return nucleo.t_info_pc()

    if nome == "gerar_senha":
        return nucleo.t_gerar_senha(args.get("tamanho", "16"))

    if nome == "capturar_tela":
        return nucleo.t_capturar_tela()

    return f"Ferramenta desconhecida: {nome}"

def executar_plugin_gui(plugins, comando):
    for p in plugins:
        if comando.lower().startswith(p["comando"]):
            args = comando[len(p["comando"]):].strip()
            captura = io.StringIO()
            try:
                with contextlib.redirect_stdout(captura):
                    p["executar"](args)
            except Exception as e:
                return f"⚠ O plugin falhou: {e}"
            return captura.getvalue() or "(plugin rodou sem saída)"
    return None

# ══════════════════════════════════════════════════════════════
#  APLICATIVO
# ══════════════════════════════════════════════════════════════
class JarvisApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode(nucleo.CFG["tema"])
        ctk.set_default_color_theme("dark-blue")
        self.configure(fg_color=FUNDO)
        self.title("MINI-JARVIS")
        self.geometry("1060x680")
        self.minsize(900, 580)
        try:
            self.iconbitmap(os.path.join(nucleo.PASTA_BASE, "logo.ico"))
        except Exception:
            pass

        self.plugins = nucleo.carregar_plugins()
        self.chat = nucleo.novo_chat()
        self.online = nucleo.tem_internet()
        self.baixando = False
        self.pensando = None
        self._anim_id = None

        self._montar_lateral()
        self._montar_area()
        threading.Thread(target=self._vigiar_lembretes,
                         daemon=True).start()
        threading.Thread(target=self._atalho_global,
                         daemon=True).start()

        self.after(400, self._arranque)
        self.protocol("WM_DELETE_WINDOW", self._sair)

    # ── ARRANQUE ─────────────────────────────────────────────
    def _arranque(self):
        exe = nucleo.achar_ollama()
        if not exe:
            if mbox.askyesno("MINI-JARVIS",
                    "O motor da IA (Ollama, ~1 GB) não está instalado.\n"
                    "Instalar agora? Fica 100% offline depois."):
                self._instalar_ollama()
                return
        elif not nucleo.servidor_no_ar():
            nucleo.iniciar_servidor(exe)
            time.sleep(2)
        if nucleo.achar_ollama() and not nucleo.CFG.get("modelo"):
            self.mostrar("vitrine")
        self._atualizar_status()
        # primeira vez: pergunta o nome e memoriza (personalidade)
        if not nucleo.CFG.get("nome_user"):
            try:
                nome = mbox.askstring("MINI-JARVIS",
                                      "Como você quer que eu te chame?",
                                      initialvalue="chefe") or "chefe"
            except Exception:
                nome = "chefe"
            nucleo.CFG["nome_user"] = nome.strip() or "chefe"
            nucleo.salvar_cfg(nucleo.CFG)
            nucleo.lembrar(f"O nome do usuário é {nucleo.CFG['nome_user']}")

        # dica única: online sem chave de nuvem → sugerir a chave grátis
        if (self.online and not nucleo.CFG.get("chave_nuvem")
                and not nucleo.CFG.get("dica_nuvem_dada")):
            nucleo.CFG["dica_nuvem_dada"] = True
            nucleo.salvar_cfg(nucleo.CFG)
            self._bolha("🌐 Você está online! Dica: com uma chave gratuita do "
                        "OpenRouter (crie em openrouter.ai/keys e cole em "
                        "FERRAMENTAS → Ajustes), eu passo a usar uma IA de "
                        "nuvem muito mais inteligente sempre que houver "
                        "internet — e volto pra IA local quando ficar offline.",
                        ferramenta=True)

        # saudação com personalidade (apenas conversas novas)
        if len(self.chat["mensagens"]) <= 1:
            h = datetime.now().hour
            if 5 <= h < 12:
                parte = "Bom dia"
            elif 12 <= h < 18:
                parte = "Boa tarde"
            else:
                parte = "Boa noite"
            nome = nucleo.CFG.get("nome_user")
            frase = (f"{parte}{', ' + nome if nome else ''}! 🤖 "
                     "Jarvis à disposição. Pode digitar, falar 🎤, "
                     "anexar 📎 ou me dar uma missão grande — eu executo "
                     "passo por passo!")
            # clima ao vivo na saudação (API grátis, sem chave)
            if self.online:
                try:
                    req = urllib.request.Request("https://wttr.in/?format=3",
                                                 headers={"User-Agent": "curl/8"})
                    clima = urllib.request.urlopen(req, timeout=6).read(
                        200).decode("utf-8", errors="replace").strip()
                    if clima:
                        frase = clima + "\n" + frase
                except Exception:
                    pass
            self._bolha(frase)
            if nucleo.CFG.get("falar"):
                threading.Thread(
                    target=self._falar,
                    args=(f"{parte}{', ' + nome if nome else ''}! "
                          "Jarvis à disposição.",),
                    daemon=True).start()
        # se ainda está sem nome, ensina o comando
        if nucleo.CFG.get("nome_user", "chefe") == "chefe":
            self._bolha("💬 Eu ainda te chamo de \"chefe\". Me diga "
                        "\"me chame de [seu nome]\" e eu memorizo pra sempre!",
                        ferramenta=True)

    def _atalho_global(self):
        """⌨️ Ctrl+Alt+J traz o Jarvis de qualquer lugar do Windows."""
        import ctypes
        import ctypes.wintypes
        user32 = ctypes.windll.user32
        MOD_CONTROL, MOD_ALT, VK_J = 0x0002, 0x0001, 0x4A
        if not user32.RegisterHotKey(None, 9001,
                                     MOD_CONTROL | MOD_ALT, VK_J):
            return  # atalho já usado por outro programa
        msg = ctypes.wintypes.MSG()
        while user32.GetMessageW(ctypes.byref(msg), None, 0, 0) > 0:
            if msg.message == 0x0312:  # WM_HOTKEY
                self.after(0, self._despertar)

    def _despertar(self):
        try:
            self.deiconify()
            self.lift()
            self.focus_force()
            self.entrada.focus_set()
        except Exception:
            pass

    def _vigiar_lembretes(self):
        """⏰ Fica de olho nos lembretes; quando dá a hora, dispara o alarme."""
        while True:
            try:
                agora = time.time()
                todos = nucleo.carregar_lembretes()
                restantes = []
                for l in todos:
                    if l.get("quando_ts", 0) <= agora:
                        texto = l.get("texto", "Lembrete")
                        self.after(0, lambda t=texto: self._alarme(t))
                    else:
                        restantes.append(l)
                if len(restantes) != len(todos):
                    nucleo.salvar_lembretes(restantes)
            except Exception:
                pass
            time.sleep(15)

    def _alarme(self, texto):
        self._bolha(f"⏰ LEMBRETE: {texto}", ferramenta=True)
        try:
            mbox.showinfo("⏰ MINI-JARVIS — Lembrete", texto)
        except Exception:
            pass
        if nucleo.CFG.get("falar"):
            threading.Thread(target=self._falar,
                             args=(f"Atenção! Lembrete: {texto}",),
                             daemon=True).start()

    def _instalar_ollama(self):
        self._status("Baixando o motor da IA (~1 GB)...")
        def trabalho():
            try:
                subprocess.run(["powershell", "-NoProfile", "-Command",
                                "irm https://ollama.com/install.ps1 | iex"],
                               timeout=1800)
            except Exception:
                pass
            ok = nucleo.iniciar_servidor(nucleo.achar_ollama())
            self.after(0, lambda: self._pos_instalacao(ok))
        threading.Thread(target=trabalho, daemon=True).start()

    def _pos_instalacao(self, ok):
        if ok:
            self.mostrar("vitrine")
        else:
            self._status("Instalação falhou — tente novamente.")
        self._atualizar_status()

    def _atualizar_status(self):
        self.online = nucleo.tem_internet()
        modelo = nucleo.CFG.get("modelo") or "configure na vitrine"
        nuvem = " + nuvem" if nucleo.CFG.get("chave_nuvem") else ""
        rede = "Online" if self.online else "Offline"
        bolinha = "#10b981" if self.online else "#ef4444"
        self.card_ponto.configure(fg_color=bolinha)
        self.card_rede.configure(text=rede)
        self.card_modelo.configure(text=f"IA: {modelo}{nuvem}")
        # painel do sistema: RAM e CPU, atualiza a cada 5s
        if not getattr(self, "_monitorando", False):
            self._monitorando = True
            self.after(5000, self._monitorar_sistema)

    def _monitorar_sistema(self):
        try:
            import psutil
            ram = psutil.virtual_memory().percent
            self.card_rede.configure(
                text=("Online" if self.online else "Offline")
                + f" · RAM {ram}%"
                + f" · CPU {int(psutil.cpu_percent())}%")
            # modo economia: RAM apertada → sugerir IA mais leve (1 vez)
            if (ram >= 85 and not nucleo.CFG.get("aviso_ram_dado")
                    and nucleo.CFG.get("modelo") not in ("qwen2.5:0.5b",
                                                         "smollm2:360m")):
                nucleo.CFG["aviso_ram_dado"] = True
                nucleo.salvar_cfg(nucleo.CFG)
                self._bolha("🟡 Sua RAM está muito cheia! Sugestão: troque "
                            "para uma IA mais leve na Vitrine (qwen2.5:0.5b) "
                            "pra não travar.", ferramenta=True)
        except Exception:
            pass
        self.after(5000, self._monitorar_sistema)

    def _status(self, texto):
        self.card_modelo.configure(text=texto)

    # ── BARRA LATERAL ────────────────────────────────────────
    def _montar_lateral(self):
        self.lateral = ctk.CTkFrame(self, width=210, fg_color=LATERAL,
                                    corner_radius=0)
        self.lateral.pack(side="left", fill="y")
        self.lateral.pack_propagate(False)

        logo = ctk.CTkFrame(self.lateral, fg_color="transparent")
        logo.pack(fill="x", padx=16, pady=(22, 4))
        ctk.CTkLabel(logo, text="🤖", font=("Segoe UI Emoji", 26)).pack(side="left")
        nome = ctk.CTkFrame(logo, fg_color="transparent")
        nome.pack(side="left", padx=(10, 0))
        ctk.CTkLabel(nome, text="MINI-JARVIS", font=("Segoe UI", 16, "bold"),
                     text_color=TXT).pack(anchor="w")
        ctk.CTkLabel(nome, text="v3.1", font=("Consolas", 10),
                     text_color=TXT_FRACO).pack(anchor="w")

        ctk.CTkLabel(self.lateral, text="  MENU", font=("Segoe UI", 10, "bold"),
                     text_color=TXT_FRACO).pack(fill="x", pady=(20, 4))

        self.botoes = {}
        for chave, rotulo in [("chat", "💬     Conversar"),
                              ("historico", "🗂     Histórico")]:
            self._botao_menu(chave, rotulo)

        ctk.CTkLabel(self.lateral, text="  FERRAMENTAS", font=("Segoe UI", 10, "bold"),
                     text_color=TXT_FRACO).pack(fill="x", pady=(14, 4))
        for chave, rotulo in [("vitrine", "🧠     Vitrine de IAs"),
                              ("agenda", "🗓     Agenda"),
                              ("sites", "🌐     Sites"),
                              ("plugins", "🔌     Plugins"),
                              ("ajustes", "⚙️     Ajustes")]:
            self._botao_menu(chave, rotulo)

        # cartão de status no rodapé
        rodape = ctk.CTkFrame(self.lateral, fg_color="transparent")
        rodape.pack(side="bottom", fill="x", padx=12, pady=14)
        ctk.CTkButton(rodape, text="⭐ v3.1 · estrela no GitHub", height=28,
                      corner_radius=8, font=("Segoe UI", 11),
                      fg_color="transparent", hover_color=HOVER_ITEM,
                      text_color=ACENTO, anchor="w",
                      command=lambda: webbrowser.open(
                          "https://github.com/"
                          "bernardoalvescaetano888-glitch/MINI-JARVIS")
                      ).pack(anchor="w", fill="x", pady=(0, 6))
        ctk.CTkSwitch(rodape, text="🗣 Jarvis fala", progress_color=ACENTO,
                      command=self._trocar_fala).pack(anchor="w", pady=(0, 8))
        cartao = ctk.CTkFrame(rodape, fg_color=CARD, corner_radius=12)
        cartao.pack(fill="x")
        topo_cartao = ctk.CTkFrame(cartao, fg_color="transparent")
        topo_cartao.pack(fill="x", padx=12, pady=(10, 0))
        self.card_ponto = ctk.CTkFrame(topo_cartao, width=9, height=9,
                                       corner_radius=5, fg_color="#10b981")
        self.card_ponto.pack(side="left")
        self.card_rede = ctk.CTkLabel(topo_cartao, text="...", font=FONTE_P,
                                      text_color=TXT_MEDIO)
        self.card_rede.pack(side="left", padx=6)
        self.card_modelo = ctk.CTkLabel(cartao, text="IA: ...", font=FONTE_P,
                                        text_color=TXT_FRACO, wraplength=160,
                                        justify="left", anchor="w")
        self.card_modelo.pack(fill="x", padx=12, pady=(2, 10))

    def _botao_menu(self, chave, rotulo):
        b = ctk.CTkButton(self.lateral, text=rotulo, anchor="w",
                          height=40, corner_radius=10, font=FONTE_M,
                          fg_color="transparent", text_color=TXT,
                          hover_color=HOVER_ITEM,
                          command=lambda c=chave: self.mostrar(c))
        b.pack(fill="x", padx=10, pady=2)
        self.botoes[chave] = b

    def _trocar_tema(self):
        nucleo.CFG["tema"] = "claro" if nucleo.CFG["tema"] == "escuro" else "escuro"
        nucleo.salvar_cfg(nucleo.CFG)
        ctk.set_appearance_mode(nucleo.CFG["tema"])
        self.configure(fg_color=FUNDO)
        for tela in self.telas.values():
            for w in tela.winfo_children():
                if isinstance(w, ctk.CTkScrollableFrame):
                    w.configure(fg_color=CARD)
        self.after(50, self._atualizar_status)

    def _trocar_fala(self):
        nucleo.CFG["falar"] = not nucleo.CFG.get("falar")
        nucleo.salvar_cfg(nucleo.CFG)
        estado = "ativada 🗣" if nucleo.CFG["falar"] else "desativada"
        self._bolha(f"Voz {estado}. Agora eu falo minhas respostas!"
                    if nucleo.CFG["falar"] else f"Voz {estado}.", ferramenta=True)

    # ── ÁREA PRINCIPAL ───────────────────────────────────────
    def _montar_area(self):
        self.area = ctk.CTkFrame(self, fg_color="transparent")
        self.area.pack(side="right", fill="both", expand=True)
        self.telas = {}
        for chave, construtor in [("chat", self._tela_chat),
                                  ("vitrine", self._tela_vitrine),
                                  ("agenda", self._tela_agenda),
                                  ("sites", self._tela_sites),
                                  ("plugins", self._tela_plugins),
                                  ("historico", self._tela_historico),
                                  ("ajustes", self._tela_ajustes)]:
            tela = ctk.CTkFrame(self.area, fg_color="transparent")
            self.telas[chave] = tela
            construtor(tela)

    def mostrar(self, chave):
        for nome, tela in self.telas.items():
            if nome == chave:
                tela.pack(fill="both", expand=True, padx=20, pady=18)
                if nome == "vitrine":
                    self._recarregar_vitrine()
                elif nome == "agenda":
                    self._recarregar_agenda()
                elif nome == "historico":
                    self._recarregar_historico()
                elif nome == "plugins":
                    self._recarregar_plugins()
                elif nome == "sites":
                    self._recarregar_sites()
            else:
                tela.pack_forget()
        for nome, b in self.botoes.items():
            if nome == chave:
                b.configure(fg_color=CARD_MENU, text_color=ACENTO)
            else:
                b.configure(fg_color="transparent", text_color=TXT)
        self._atualizar_status()

    def _cabecalho(self, tela, emoji, titulo, subtitulo):
        topo = ctk.CTkFrame(tela, fg_color="transparent")
        topo.pack(fill="x")
        ctk.CTkLabel(topo, text=f"{emoji}  {titulo}", font=FONTE_G,
                     text_color=TXT).pack(side="left")
        sub = ctk.CTkLabel(topo, text=subtitulo, font=FONTE_P,
                           text_color=TXT_FRACO)
        sub.pack(side="left", padx=(14, 0), pady=(7, 0))
        return topo

    # ── TELA: CHAT ───────────────────────────────────────────
    def _tela_chat(self, tela):
        self.chat_scroll = ctk.CTkScrollableFrame(tela, fg_color="transparent")
        self.chat_scroll.pack(fill="both", expand=True)

        barra = ctk.CTkFrame(tela, fg_color="transparent", height=64)
        barra.pack(fill="x", side="bottom", pady=(12, 0))
        self.entrada = ctk.CTkEntry(barra, placeholder_text=
            "   Envie uma mensagem…   (ex: crie um arquivo poema.txt)",
            height=48, corner_radius=24, font=FONTE,
            fg_color=CARD, text_color=TXT,
            border_width=1, border_color=("gray70", "#3a3a3b"))
        self.entrada.pack(side="left", fill="x", expand=True)
        self.entrada.bind("<Return>", lambda e: self._enviar())
        ctk.CTkButton(barra, text="📎", width=44, height=48,
                      corner_radius=16, font=("Segoe UI", 15),
                      fg_color=CARD, hover_color=HOVER_ITEM,
                      text_color=TXT, command=self._anexar
                      ).pack(side="left", padx=(10, 0))
        ctk.CTkButton(barra, text="🎤", width=44, height=48,
                      corner_radius=16, font=("Segoe UI", 15),
                      fg_color=CARD, hover_color=HOVER_ITEM,
                      text_color=TXT, command=self._microfone
                      ).pack(side="left", padx=(6, 0))
        ctk.CTkButton(barra, text="➤", width=48, height=48,
                      corner_radius=24, font=("Segoe UI", 17, "bold"),
                      fg_color=ACENTO, hover_color=ACENTO_2,
                      text_color="#ffffff",
                      command=self._enviar).pack(side="left", padx=(6, 0))

    def _anexar(self):
        """📎 Anexa um arquivo na conversa para o Jarvis ler."""
        from tkinter import filedialog
        caminho = filedialog.askopenfilename(
            title="Escolha um arquivo para o Jarvis ler")
        if not caminho:
            return
        ext = os.path.splitext(caminho)[1].lower()
        nome = os.path.basename(caminho)
        self._bolha(f"📎 anexou: {nome}", minha=True)

        # PDF: extrai o texto (até 30 páginas) e manda pra IA ler
        if ext == ".pdf":
            try:
                from pypdf import PdfReader
                leitor = PdfReader(caminho)
                texto = ""
                for pag in leitor.pages[:30]:
                    texto += (pag.extract_text() or "") + "\n"
                if not texto.strip():
                    self._bolha("⚠ Esse PDF parece ser só imagem (escaneado). "
                                "Consegui abrir, mas não tem texto pra ler.",
                                ferramenta=True)
                    return
                self._enviar_texto(
                    f"O usuário anexou o PDF '{nome}' ({len(leitor.pages)} "
                    f"páginas). Conteúdo:\n{texto[:6000]}\n\n"
                    "Faça o que o usuário pedir sobre ele; se ele não pediu "
                    "nada, resuma.")
            except Exception as e:
                self._bolha(f"⚠ Não consegui ler o PDF: {e}", ferramenta=True)
            return

        # Word (.docx): extrai o texto do XML interno (sem biblioteca extra)
        if ext == ".docx":
            try:
                import re as _re
                from zipfile import ZipFile
                with ZipFile(caminho) as z:
                    xml = z.read("word/document.xml").decode(
                        "utf-8", errors="replace")
                texto = _re.sub(r"<[^>]+>", " ", xml)
                texto = _re.sub(r"\s+", " ", texto).strip()
                self._enviar_texto(
                    f"O usuário anexou o documento Word '{nome}'. Conteúdo:"
                    f"\n{texto[:6000]}\n\n"
                    "Faça o que o usuário pedir sobre ele; se ele não pediu "
                    "nada, resuma.")
            except Exception as e:
                self._bolha(f"⚠ Não consegui ler o Word: {e}", ferramenta=True)
            return

        # imagens: aparecem DENTRO da conversa 🖼️
        if ext in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"):
            try:
                from PIL import Image
                pil = Image.open(caminho)
                pil.thumbnail((420, 420))
                foto = ctk.CTkImage(light_image=pil, dark_image=pil,
                                    size=pil.size)
                moldura = ctk.CTkFrame(self.chat_scroll,
                                       fg_color="transparent")
                moldura.pack(fill="x", pady=4, padx=(90, 0))
                ctk.CTkLabel(moldura, image=foto, text="").pack(side="right",
                                                                padx=8)
                self._rolar_fim()
                self._enviar_texto(
                    f"O usuário anexou a imagem '{nome}' (ela apareceu "
                    "acima na conversa). Responda de forma simpática e "
                    "pergunte o que ele quer fazer com ela.")
            except Exception as e:
                self._bolha(f"⚠ Não consegui mostrar a imagem: {e}",
                            ferramenta=True)
            return

        # mídia e outros binários: abre no programa padrão
        if ext in (".xlsx", ".pptx", ".mp3", ".mp4"):
            resultado = ferramenta_gui("abrir_arquivo", {"caminho": caminho})
            self._bolha(resultado, ferramenta=True)
            return

        try:
            with open(caminho, encoding="utf-8", errors="replace") as f:
                conteudo = f.read(4000)
        except Exception as e:
            mbox.showerror("Erro", f"Não consegui ler: {e}")
            return
        self._enviar_texto(
            f"O usuário anexou o arquivo '{nome}'. Conteúdo:\n{conteudo}\n\n"
            "Analise este arquivo e diga o que achou.")

    def _microfone(self):
        """🎤 Botão de voz: tenta ouvir; sem microfone, usa o ditado do Windows."""
        def trabalho():
            texto = None
            try:
                import speech_recognition as sr
                recon = sr.Recognizer()
                with sr.Microphone() as fonte:
                    recon.adjust_for_ambient_noise(fonte, duration=0.4)
                    audio = recon.listen(fonte, timeout=6, phrase_time_limit=15)
                texto = recon.recognize_google(audio, language="pt-BR")
            except Exception:
                texto = None
            self.after(0, lambda: self._pos_microfone(texto))
        self._bolha("🎤 ouvindo… fale agora", ferramenta=True)
        threading.Thread(target=trabalho, daemon=True).start()

    def _pos_microfone(self, texto):
        if texto:
            self._enviar_texto(texto)
            return
        # sem microfone configurável → ditado nativo do Windows (Win+H)
        try:
            import ctypes
            self.entrada.focus_set()
            ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0x48, 0, 0, 0)
            ctypes.windll.user32.keybd_event(0x48, 0, 2, 0)
            ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0)
            self._bolha("🎤 Ditado do Windows ativado — fale! "
                        "(o Windows digita na caixinha; Enter envia)",
                        ferramenta=True)
        except Exception:
            self._bolha("🎤 Não consegui ouvir. Verifique o microfone "
                        "(Configurações → Privacidade → Microfone).",
                        ferramenta=True)

    def _falar(self, texto):
        """🗣 Jarvis fala a resposta em voz alta."""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty("rate", 170)
            for v in engine.getProperty("voices"):
                if "portug" in v.name.lower() or "pt" in v.id.lower():
                    engine.setProperty("voice", v.id)
                    break
            engine.say(texto[:400])
            engine.runAndWait()
        except Exception:
            pass

    def _nova_conversa(self):
        self.chat = nucleo.novo_chat()
        for w in self.chat_scroll.winfo_children():
            w.destroy()
        self.mostrar("chat")
        self._bolha("Nova conversa começada! Estou ouvindo. 💫")

    def _rolar_fim(self):
        try:
            self.chat_scroll.after(90, lambda:
                self.chat_scroll._parent_canvas.yview_moveto(1.0))
        except Exception:
            pass

    def _bolha(self, texto, minha=False, ferramenta=False):
        if self.pensando:
            self._fim_pensando()
        if ferramenta:
            linha = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
            linha.pack(fill="x", pady=3, padx=(36, 40))
            chip = ctk.CTkFrame(linha, fg_color=CHIP, corner_radius=10)
            chip.pack(side="left", anchor="w")
            ctk.CTkLabel(chip, text=f"⚙  {texto}", justify="left",
                         font=FONTE_COD, text_color=LARANJA
                         ).pack(padx=12, pady=7)
            self._rolar_fim()
            return
        if minha:
            linha = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
            linha.pack(fill="x", pady=5, padx=(90, 0))
            bolha = ctk.CTkFrame(linha, fg_color=BOLHA_VOCE, corner_radius=18)
            bolha.pack(side="right", anchor="e")
            ctk.CTkLabel(bolha, text=texto, justify="left", wraplength=520,
                         text_color="#ffffff", font=FONTE
                         ).pack(padx=16, pady=10)
            self._rolar_fim()
            return
        # mensagem do Jarvis: estilo ChatGPT (limpo, sem bolha)
        linha = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        linha.pack(fill="x", pady=4, padx=(0, 80))
        cabecalho = ctk.CTkFrame(linha, fg_color="transparent")
        cabecalho.pack(anchor="w")
        avatar = ctk.CTkFrame(cabecalho, width=30, height=30, corner_radius=15,
                              fg_color=ACENTO)
        avatar.pack(side="left")
        ctk.CTkLabel(avatar, text="J", font=("Segoe UI", 14, "bold"),
                     text_color="#ffffff").pack(padx=0, pady=0)
        ctk.CTkLabel(cabecalho, text="  Jarvis", font=("Segoe UI", 12, "bold"),
                     text_color=TXT_MEDIO).pack(side="left", padx=6)
        ctk.CTkLabel(linha, text=texto, justify="left", wraplength=620,
                     text_color=TXT, font=FONTE
                     ).pack(anchor="w", padx=(40, 0), pady=(4, 2))
        self._rolar_fim()

    def _animar_pensando(self):
        if not self.pensando:
            return
        self._n_dots = (getattr(self, "_n_dots", 0) + 1) % 4
        try:
            decorrido = int(time.time() - getattr(self, "_t0", time.time()))
            self.pensando_lb.configure(text="💭 Jarvis está pensando"
                                       + " ●" * self._n_dots
                                       + f"   ({decorrido}s)")
        except Exception:
            return
        self._anim_id = self.after(500, self._animar_pensando)

    def _enviar(self):
        texto = self.entrada.get().strip()
        if not texto or self.baixando or self.pensando:
            return
        self.entrada.delete(0, "end")

        saida_plugin = executar_plugin_gui(self.plugins, texto)
        if saida_plugin is not None:
            self._bolha(texto, minha=True)
            self._bolha(saida_plugin)
            return

        if texto in ("sair", "exit"):
            self._sair(); return

        # comando direto: "me chame de ..." (à prova de falhas, sem IA)
        baixo = texto.lower()
        if baixo.startswith("me chame de ") or baixo.startswith("me chama de "):
            nome = texto.split(" de ", 1)[1].strip().strip(".!? ")
            self._bolha(texto, minha=True)
            if nome:
                nucleo.CFG["nome_user"] = nome[:30]
                nucleo.salvar_cfg(nucleo.CFG)
                nucleo.lembrar(f"O nome do usuário é {nome[:30]}")
                resposta = (f"Perfeito, {nome}! 🤝 De agora em diante eu te "
                            "chamo assim — memorizei pra sempre.")
            else:
                resposta = "Me diga assim: me chame de Pedro"
            self._bolha(resposta)
            if nucleo.CFG.get("falar"):
                threading.Thread(target=self._falar, args=(resposta,),
                                 daemon=True).start()
            return

        if texto.startswith("/") and not self.plugins:
            nomes = "  ".join(p["comando"] for p in self.plugins) or "nenhum"
            self._bolha(f"Esse plugin não existe. Instalados: {nomes}",
                        ferramenta=True)
            return

        self._enviar_texto(texto)

    def _enviar_texto(self, texto):
        """Mostra a mensagem, a animação de pensando e chama a IA."""
        if self.pensando:
            return
        self._bolha(texto, minha=True)
        self.pensando = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
        self.pensando.pack(fill="x", pady=4, padx=(0, 80))
        self.pensando_lb = ctk.CTkLabel(self.pensando, text="💭 Jarvis está pensando",
                                        font=FONTE_M, text_color=TXT_FRACO)
        self.pensando_lb.pack(anchor="w", padx=40)
        self._n_dots = 0
        self._t0 = time.time()
        self._animar_pensando()
        self._rolar_fim()
        threading.Thread(target=self._pipeline, args=(texto,),
                         daemon=True).start()

    def _fim_pensando(self):
        if self._anim_id:
            try:
                self.after_cancel(self._anim_id)
            except Exception:
                pass
            self._anim_id = None
        if self.pensando:
            try:
                self.pensando.destroy()
            except Exception:
                pass
            self.pensando = None

    def _pipeline(self, texto):
        mensagens = self.chat["mensagens"]
        # memória sempre atualizada (o Jarvis "relembra" a cada mensagem)
        if mensagens and mensagens[0].get("role") == "system":
            mensagens[0]["content"] = nucleo.sistema_prompt()
        mensagens.append({"role": "user", "content": texto})
        estado = {"viva": None}

        def criar_viva():
            """Transforma o 'pensando' na resposta ao vivo (streaming)."""
            self._fim_pensando()
            linha = ctk.CTkFrame(self.chat_scroll, fg_color="transparent")
            linha.pack(fill="x", pady=4, padx=(0, 80))
            cabecalho = ctk.CTkFrame(linha, fg_color="transparent")
            cabecalho.pack(anchor="w")
            avatar = ctk.CTkFrame(cabecalho, width=30, height=30,
                                  corner_radius=15, fg_color=ACENTO)
            avatar.pack(side="left")
            ctk.CTkLabel(avatar, text="J", font=("Segoe UI", 14, "bold"),
                         text_color="#ffffff").pack()
            ctk.CTkLabel(cabecalho, text="  Jarvis",
                         font=("Segoe UI", 12, "bold"),
                         text_color=TXT_MEDIO).pack(side="left", padx=6)
            estado["viva"] = ctk.CTkLabel(linha, text="", justify="left",
                                          wraplength=620, text_color=TXT,
                                          font=FONTE)
            estado["viva"].pack(anchor="w", padx=(40, 0), pady=(4, 2))
            self._rolar_fim()

        def ao_receber(texto_total):
            # agrupa as letras num único atualização (interface leve)
            estado["pendente"] = texto_total
            self.after(0, lambda: _drenar())

        def _drenar():
            texto = estado.pop("pendente", None)
            if texto is None:
                return  # outra chamada já drenou
            if estado["viva"] is None:
                criar_viva()
            estado["viva"].configure(text=texto)
            self._rolar_fim()

        try:
            for passo in range(10):
                # com internet + chave → IA da nuvem (mais inteligente);
                # sem internet → IA local em tempo real
                if self.online and nucleo.CFG.get("chave_nuvem"):
                    try:
                        resposta = nucleo.chamada_nuvem_stream(
                            nucleo.cortar_historico(mensagens), nucleo.CFG,
                            ao_receber)
                    except Exception:
                        resposta = nucleo.chamada_local_stream(
                            nucleo.cortar_historico(mensagens),
                            nucleo.CFG["modelo"], ao_receber)
                else:
                    resposta = nucleo.chamada_local_stream(
                        nucleo.cortar_historico(mensagens),
                        nucleo.CFG["modelo"], ao_receber)
                chamadas = resposta.get("tool_calls")
                fala = resposta.get("content") or ""
                if chamadas:
                    mensagens.append({"role": "assistant", "content": fala,
                                      "tool_calls": chamadas})
                    for c in chamadas:
                        nome = c["function"]["name"]
                        args = c["function"].get("arguments", {})
                        if isinstance(args, str):
                            args = json.loads(args or "{}")
                        resultado = ferramenta_gui(nome, args)
                        resumo = str(resultado).splitlines()[0][:70]
                        self.after(0, lambda n=nome, r=resumo, p=passo + 1:
                                   (self._fim_pensando(),
                                    self._bolha(f"🪜 passo {p} · {n}  ·  {r}",
                                                ferramenta=True)))
                        mensagens.append({"role": "tool",
                                          "content": str(resultado), "name": nome})
                    continue
                self.after(0, lambda: self._fim_pensando())
                if not fala:
                    self.after(0, lambda: self._bolha("(sem resposta)"))
                mensagens.append({"role": "assistant", "content": fala})
                # 🔔 som curto de resposta (estilo JARVIS)
                if winsound:
                    threading.Thread(
                        target=lambda: (winsound.Beep(880, 90),
                                        winsound.Beep(1174, 130)),
                        daemon=True).start()
                if nucleo.CFG.get("falar") and fala:
                    threading.Thread(target=self._falar, args=(fala,),
                                     daemon=True).start()
                break
        except Exception as e:
            self.after(0, lambda: (self._fim_pensando(),
                                   self._bolha(f"⚠ Erro: {e}", ferramenta=True)))
        nucleo.salvar_chat(self.chat, nucleo.CFG["modelo"])
        self.after(0, self._atualizar_status)

    # ── TELA: VITRINE ────────────────────────────────────────
    def _tela_vitrine(self, tela):
        topo = self._cabecalho(tela, "🧠", "Vitrine de IAs",
                               "escolha pela chance de funcionar no seu PC")
        self.vit_aviso = ctk.CTkLabel(topo, text="", font=FONTE_P,
                                      text_color=ACENTO)
        self.vit_aviso.pack(side="right", pady=(7, 0))
        self.vit_lista = ctk.CTkScrollableFrame(tela, fg_color=CARD,
                                                corner_radius=16)
        self.vit_lista.pack(fill="both", expand=True, pady=12)
        self.vit_barra = ctk.CTkProgressBar(tela, mode="indeterminate",
                                            progress_color=ACENTO, height=6)
        self.vit_barra.pack(fill="x", side="bottom")
        self.vit_barra.set(0); self.vit_barra.stop()

    def _recarregar_vitrine(self):
        for w in self.vit_lista.winfo_children():
            w.destroy()
        instaladas = []
        exe = nucleo.achar_ollama()
        if exe:
            instaladas = nucleo.listar_modelos_instalados(exe)
        ctk.CTkLabel(self.vit_lista, text="  MODELO                TIPO            TAMANHO      DESEMPENHO",
                     font=("Consolas", 10), text_color=TXT_FRACO
                     ).pack(fill="x", pady=(10, 4), padx=14)
        for apelido, modelo, mb, chance, tag in nucleo.CATALOGO:
            linha = ctk.CTkFrame(self.vit_lista, fg_color="transparent")
            linha.pack(fill="x", pady=7, padx=14)
            ctk.CTkLabel(linha, text=apelido, width=185, anchor="w",
                         font=("Segoe UI", 14, "bold"),
                         text_color=TXT).pack(side="left")
            ctk.CTkLabel(linha, text=tag, width=115, anchor="w",
                         font=FONTE_P, text_color=TXT_MEDIO).pack(side="left")
            ctk.CTkLabel(linha, text=(f"{mb/1000:.1f} GB" if mb >= 1000
                                      else f"{mb} MB"), width=70, anchor="w",
                         font=FONTE_P, text_color=TXT_MEDIO).pack(side="left")
            barra = ctk.CTkProgressBar(linha, width=125, corner_radius=6, height=8)
            barra.set(chance / 100); barra.pack(side="left", padx=8)
            cor = "#10b981" if chance >= 70 else (("#f59e0b", "#f59e0b")[0] if chance >= 40 else "#ef4444")
            barra.configure(progress_color=cor)
            ctk.CTkLabel(linha, text=f"{chance:>3}%", width=42,
                         font=("Segoe UI", 12, "bold"),
                         text_color=cor).pack(side="left")
            if modelo in instaladas:
                ctk.CTkButton(linha, text="usar", width=84, height=32,
                              corner_radius=16, font=FONTE_P,
                              fg_color=CARD_MENU, hover_color=HOVER_ITEM,
                              text_color=ACENTO,
                              command=lambda m=modelo: self._usar_modelo(m)
                              ).pack(side="right", padx=(8, 0))
                ctk.CTkLabel(linha, text="✔ instalada", width=90, font=FONTE_P,
                             text_color=ACENTO).pack(side="right")
            else:
                ctk.CTkButton(linha, text="⬇ instalar", width=104, height=32,
                              corner_radius=16, font=FONTE_P,
                              fg_color=ACENTO, hover_color=ACENTO_2,
                              text_color="#ffffff",
                              command=lambda m=modelo, c=chance, mb_=mb:
                              self._baixar_modelo(m, c, mb_)
                              ).pack(side="right")

    def _usar_modelo(self, modelo):
        nucleo.CFG["modelo"] = modelo
        nucleo.salvar_cfg(nucleo.CFG)
        self.mostrar("chat")
        self._bolha(f"Agora estou usando a IA {modelo}! 🧠")

    def _baixar_modelo(self, modelo, chance, mb):
        if self.baixando:
            mbox.showinfo("Aguarde", "Já tem um download em andamento!")
            return
        livre = nucleo.espaco_livre_mb()
        if livre < mb:
            mbox.showerror("Sem espaço", f"Disco com só {livre} MB livres!")
            return
        if chance < 60 and not mbox.askyesno(
                "IA arriscada", f"Esta IA tem só {chance}% de chance de rodar bem.\n"
                "Mesmo assim instalar?"):
            return
        self.baixando = True
        self.vit_barra.start()
        self.vit_aviso.configure(text=f"⬇ Baixando {modelo}…")
        exe = nucleo.achar_ollama()
        def trabalho():
            codigo = subprocess.run([exe, "pull", modelo]).returncode
            self.after(0, lambda: self._pos_baixar(modelo, codigo))
        threading.Thread(target=trabalho, daemon=True).start()

    def _pos_baixar(self, modelo, codigo):
        self.baixando = False
        self.vit_barra.stop(); self.vit_barra.set(0)
        if codigo == 0:
            nucleo.CFG["modelo"] = modelo
            nucleo.salvar_cfg(nucleo.CFG)
            self.mostrar("chat")
            self._bolha(f"{modelo} instalada e pronta! Manda a primeira mensagem 😄")
        else:
            self.vit_aviso.configure(text="✘ download falhou")
        self._recarregar_vitrine()

    # ── TELA: AGENDA (lembretes + tarefas) ───────────────────
    def _tela_agenda(self, tela):
        self._cabecalho(tela, "🗓", "Agenda", "lembretes que tocam sozinhos e tarefas")
        barra = ctk.CTkFrame(tela, fg_color=CARD, corner_radius=14)
        barra.pack(fill="x", pady=(4, 10))
        self.tarefa_entrada = ctk.CTkEntry(
            barra, placeholder_text="  nova tarefa (ex: entregar trabalho de história)",
            height=40, corner_radius=10, fg_color="transparent",
            border_width=1, border_color=("gray70", "#3a3a3b"))
        self.tarefa_entrada.pack(side="left", fill="x", expand=True,
                                 padx=10, pady=10)
        ctk.CTkButton(barra, text="＋ Tarefa", width=110, height=40,
                      corner_radius=10, font=FONTE_P,
                      fg_color=ACENTO, hover_color=ACENTO_2,
                      text_color="#ffffff",
                      command=self._add_tarefa).pack(side="left", padx=(0, 10))
        self.agenda_lista = ctk.CTkScrollableFrame(tela, fg_color=CARD,
                                                   corner_radius=16)
        self.agenda_lista.pack(fill="both", expand=True)

    def _recarregar_agenda(self):
        for w in self.agenda_lista.winfo_children():
            w.destroy()
        from datetime import datetime as _dt
        # lembretes agendados
        lembretes = nucleo.carregar_lembretes()
        if lembretes:
            ctk.CTkLabel(self.agenda_lista, text="⏰ Lembretes agendados",
                         font=("Segoe UI", 13, "bold"),
                         text_color=ACENTO).pack(anchor="w", padx=14,
                                                 pady=(12, 4))
            for l in sorted(lembretes, key=lambda x: x.get("quando_ts", 0)):
                quando = str(l.get("quando", ""))[:16].replace("T", " ")
                linha = ctk.CTkFrame(self.agenda_lista,
                                     fg_color="transparent")
                linha.pack(fill="x", pady=5, padx=14)
                ctk.CTkLabel(linha, text=f"⏰  {quando}", width=120,
                             anchor="w", font=("Consolas", 12),
                             text_color=TXT_MEDIO).pack(side="left")
                ctk.CTkLabel(linha, text=l.get("texto", ""), anchor="w",
                             font=("Segoe UI", 13), text_color=TXT
                             ).pack(side="left", fill="x", expand=True)
                ctk.CTkButton(linha, text="✖", width=34, height=30,
                              corner_radius=10, font=FONTE_P,
                              fg_color="transparent", hover_color=HOVER_ITEM,
                              text_color=TXT_MEDIO,
                              command=lambda i=l: self._apagar_lembrete(i)
                              ).pack(side="left")
        # tarefas
        tarefas = nucleo.carregar_tarefas()
        ctk.CTkLabel(self.agenda_lista, text="📝 Lista de tarefas",
                     font=("Segoe UI", 13, "bold"),
                     text_color=ACENTO).pack(anchor="w", padx=14,
                                             pady=(14, 4))
        if not tarefas:
            ctk.CTkLabel(self.agenda_lista,
                         text="(nenhuma tarefa — peça ao Jarvis pelo chat!)",
                         font=FONTE_P, text_color=TXT_FRACO
                         ).pack(anchor="w", padx=14)
        for i, t in enumerate(tarefas):
            linha = ctk.CTkFrame(self.agenda_lista, fg_color="transparent")
            linha.pack(fill="x", pady=5, padx=14)
            feito = t.get("feita", False)
            texto = ("✔ " + t["texto"]) if feito else t["texto"]
            cor = TXT_FRACO if feito else TXT
            ctk.CTkButton(linha, text="✅" if feito else "⬜", width=34,
                          height=30, corner_radius=10, font=FONTE_P,
                          fg_color="transparent", hover_color=HOVER_ITEM,
                          text_color=cor,
                          command=lambda n=i: self._alternar_tarefa(n)
                          ).pack(side="left")
            ctk.CTkLabel(linha, text=texto, anchor="w",
                         font=("Segoe UI", 13, "overstrike" if feito else "normal"),
                         text_color=cor).pack(side="left", fill="x",
                                              expand=True)
            if not feito:
                ctk.CTkButton(linha, text="✖", width=34, height=30,
                              corner_radius=10, font=FONTE_P,
                              fg_color="transparent", hover_color=HOVER_ITEM,
                              text_color=TXT_MEDIO,
                              command=lambda n=i: self._apagar_tarefa(n)
                              ).pack(side="left")

    def _add_tarefa(self):
        texto = self.tarefa_entrada.get().strip()
        if not texto:
            return
        self.tarefa_entrada.delete(0, "end")
        tarefas = nucleo.carregar_tarefas()
        tarefas.append({"texto": texto, "feita": False})
        nucleo.salvar_tarefas(tarefas)
        self._recarregar_agenda()

    def _alternar_tarefa(self, indice):
        tarefas = nucleo.carregar_tarefas()
        if 0 <= indice < len(tarefas):
            tarefas[indice]["feita"] = not tarefas[indice].get("feita", False)
            nucleo.salvar_tarefas(tarefas)
        self._recarregar_agenda()

    def _apagar_tarefa(self, indice):
        tarefas = nucleo.carregar_tarefas()
        if 0 <= indice < len(tarefas):
            tarefas.pop(indice)
            nucleo.salvar_tarefas(tarefas)
        self._recarregar_agenda()

    def _apagar_lembrete(self, item):
        lembretes = nucleo.carregar_lembretes()
        lembretes = [l for l in lembretes if l is not item]
        nucleo.salvar_lembretes(lembretes)
        self._recarregar_agenda()

    # ── TELA: SITES ──────────────────────────────────────────
    def _tela_sites(self, tela):
        self._cabecalho(tela, "🌐", "Meus sites", "abrem no navegador com 1 clique")
        barra = ctk.CTkFrame(tela, fg_color=CARD, corner_radius=14)
        barra.pack(fill="x", pady=(4, 10))
        self.site_nome = ctk.CTkEntry(barra, placeholder_text="  nome",
                                      width=140, height=40, corner_radius=10,
                                      fg_color="transparent", border_width=1,
                                      border_color=("gray70", "#3a3a3b"))
        self.site_nome.pack(side="left", padx=10, pady=10)
        self.site_url = ctk.CTkEntry(barra, placeholder_text="  https://...",
                                     height=40, corner_radius=10,
                                     fg_color="transparent", border_width=1,
                                     border_color=("gray70", "#3a3a3b"))
        self.site_url.pack(side="left", fill="x", expand=True, pady=10)
        ctk.CTkButton(barra, text="Adicionar", width=110, height=40,
                      corner_radius=10, font=FONTE_P,
                      fg_color=ACENTO, hover_color=ACENTO_2,
                      text_color="#ffffff",
                      command=self._add_site).pack(side="left", padx=(0, 10))
        self.sites_lista = ctk.CTkScrollableFrame(tela, fg_color=CARD,
                                                  corner_radius=16)
        self.sites_lista.pack(fill="both", expand=True)

    def _recarregar_sites(self):
        for w in self.sites_lista.winfo_children():
            w.destroy()
        for nome, url in nucleo.CFG["sites"]:
            linha = ctk.CTkFrame(self.sites_lista, fg_color="transparent")
            linha.pack(fill="x", pady=7, padx=14)
            ctk.CTkLabel(linha, text=f"🔗  {nome}", width=170, anchor="w",
                         font=("Segoe UI", 14, "bold"),
                         text_color=TXT).pack(side="left")
            ctk.CTkLabel(linha, text=url, anchor="w", font=FONTE_P,
                         text_color=TXT_MEDIO).pack(side="left", fill="x",
                                                    expand=True)
            ctk.CTkButton(linha, text="abrir", width=78, height=30,
                          corner_radius=10, font=FONTE_P,
                          fg_color=CARD_MENU, hover_color=HOVER_ITEM,
                          text_color=ACENTO,
                          command=lambda u=url: webbrowser.open(u)).pack(side="left")
            ctk.CTkButton(linha, text="✖", width=34, height=30,
                          corner_radius=10, font=FONTE_P,
                          fg_color="transparent", hover_color=HOVER_ITEM,
                          text_color=VERMELHO,
                          command=lambda n=nome: self._del_site(n)
                          ).pack(side="left", padx=(6, 0))

    def _add_site(self):
        nome = self.site_nome.get().strip()
        url = self.site_url.get().strip()
        if nome and url:
            nucleo.CFG["sites"].append([nome, url])
            nucleo.salvar_cfg(nucleo.CFG)
            self.site_nome.delete(0, "end"); self.site_url.delete(0, "end")
            self._recarregar_sites()

    def _del_site(self, nome):
        nucleo.CFG["sites"] = [s for s in nucleo.CFG["sites"] if s[0] != nome]
        nucleo.salvar_cfg(nucleo.CFG)
        self._recarregar_sites()

    # ── TELA: PLUGINS ────────────────────────────────────────
    def _tela_plugins(self, tela):
        topo = self._cabecalho(tela, "🔌", "Plugins", "poderes extras do Jarvis")
        ctk.CTkButton(topo, text="↻ Recarregar", width=110, height=36,
                      corner_radius=10, font=FONTE_P,
                      fg_color=CARD_MENU, hover_color=HOVER_ITEM,
                      text_color=TXT,
                      command=self._reload_plugins).pack(side="right")
        ctk.CTkLabel(tela, text="Coloque arquivos .py na pasta plugins/ "
                     "(veja TEMPLATE.py) e eles aparecem aqui automaticamente!",
                     font=FONTE_P, text_color=TXT_FRACO).pack(anchor="w", pady=4)
        self.plug_lista = ctk.CTkScrollableFrame(tela, fg_color=CARD,
                                                 corner_radius=16)
        self.plug_lista.pack(fill="both", expand=True)

    def _reload_plugins(self):
        self.plugins = nucleo.carregar_plugins()
        self._recarregar_plugins()

    def _recarregar_plugins(self):
        for w in self.plug_lista.winfo_children():
            w.destroy()
        if not self.plugins:
            ctk.CTkLabel(self.plug_lista, text="(nenhum plugin ainda)",
                         font=FONTE_P, text_color=TXT_FRACO).pack(pady=12)
        for p in self.plugins:
            linha = ctk.CTkFrame(self.plug_lista, fg_color="transparent")
            linha.pack(fill="x", pady=8, padx=14)
            ctk.CTkLabel(linha, text=p["comando"], width=110, anchor="w",
                         font=("Consolas", 13, "bold"),
                         text_color=ACENTO).pack(side="left")
            ctk.CTkLabel(linha, text=p["desc"], anchor="w", font=FONTE_M,
                         text_color=TXT).pack(side="left", fill="x",
                                              expand=True)
            ctk.CTkButton(linha, text="rodar", width=78, height=30,
                          corner_radius=10, font=FONTE_P,
                          fg_color=ACENTO, hover_color=ACENTO_2,
                          text_color="#ffffff",
                          command=lambda c=p["comando"]: self._rodar_plugin(c)
                          ).pack(side="left")

    def _rodar_plugin(self, comando):
        saida = executar_plugin_gui(self.plugins, comando) or "(sem saída)"
        janela = ctk.CTkToplevel(self)
        janela.title(f"Plugin {comando}")
        janela.geometry("480x290")
        janela.configure(fg_color=CARD)
        janela.attributes("-topmost", True)
        box = ctk.CTkTextbox(janela, wrap="word", font=FONTE_COD,
                             fg_color=CARD, text_color=TXT)
        box.pack(fill="both", expand=True, padx=12, pady=12)
        box.insert("end", saida)

    # ── TELA: HISTÓRICO ──────────────────────────────────────
    def _tela_historico(self, tela):
        topo = self._cabecalho(tela, "🗂", "Histórico", "suas conversas salvas")
        ctk.CTkButton(topo, text="💬 Nova conversa", width=130, height=36,
                      corner_radius=10, font=FONTE_P,
                      fg_color=ACENTO, hover_color=ACENTO_2, text_color="#ffffff",
                      command=self._nova_conversa).pack(side="right")
        self.hist_lista = ctk.CTkScrollableFrame(tela, fg_color=CARD,
                                                 corner_radius=16)
        self.hist_lista.pack(fill="both", expand=True, pady=12)

    def _recarregar_historico(self):
        for w in self.hist_lista.winfo_children():
            w.destroy()
        os.makedirs(nucleo.PASTA_CHATS, exist_ok=True)
        arquivos = sorted(os.listdir(nucleo.PASTA_CHATS))[-30:][::-1]
        if not arquivos:
            ctk.CTkLabel(self.hist_lista, text="(nenhuma conversa salva ainda)",
                         font=FONTE_P, text_color=TXT_FRACO).pack(pady=12)
        for a in arquivos:
            linha = ctk.CTkFrame(self.hist_lista, fg_color="transparent")
            linha.pack(fill="x", pady=6, padx=14)
            ctk.CTkLabel(linha, text=f"🗂  {a[:-5]}", anchor="w", font=FONTE_M,
                         text_color=TXT).pack(side="left", fill="x",
                                              expand=True)
            ctk.CTkButton(linha, text="abrir", width=78, height=30,
                          corner_radius=10, font=FONTE_P,
                          fg_color=ACENTO, hover_color=ACENTO_2,
                          text_color="#ffffff",
                          command=lambda arq=a: self._abrir_chat(arq)).pack(side="left")

    def _abrir_chat(self, arquivo):
        caminho = os.path.join(nucleo.PASTA_CHATS, arquivo)
        try:
            with open(caminho, encoding="utf-8") as f:
                dados = json.load(f)
            self.chat = {"arquivo": caminho, "mensagens": dados["mensagens"]}
        except Exception as e:
            mbox.showerror("Erro", f"Não consegui abrir: {e}")
            return
        for w in self.chat_scroll.winfo_children():
            w.destroy()
        for m in self.chat["mensagens"]:
            if m["role"] == "user":
                self._bolha(m["content"], minha=True)
            elif m["role"] == "assistant" and m.get("content"):
                self._bolha(m["content"])
        self.mostrar("chat")

    # ── TELA: AJUSTES ────────────────────────────────────────
    def _tela_ajustes(self, tela):
        self._cabecalho(tela, "⚙️", "Ajustes", "configure seu Jarvis")

        card_nuvem = ctk.CTkFrame(tela, fg_color=CARD, corner_radius=16)
        card_nuvem.pack(fill="x", pady=10)
        ctk.CTkLabel(card_nuvem, text="☁️   Modo nuvem (opcional)",
                     font=("Segoe UI", 14, "bold"),
                     text_color=TXT).pack(anchor="w", padx=16, pady=(14, 2))
        ctk.CTkLabel(card_nuvem, text="Com internet, usa uma IA mais inteligente.\n"
                     "Chave GRATUITA em: openrouter.ai/keys",
                     font=FONTE_P, justify="left",
                     text_color=TXT_MEDIO).pack(anchor="w", padx=16)
        barra = ctk.CTkFrame(card_nuvem, fg_color="transparent")
        barra.pack(fill="x", padx=16, pady=(8, 14))
        self.chave_entry = ctk.CTkEntry(barra, width=330, height=40,
                                        corner_radius=10,
                                        fg_color="transparent",
                                        border_width=1,
                                        border_color=("gray70", "#3a3a3b"),
                                        placeholder_text="  sk-or-… (cole aqui)")
        self.chave_entry.pack(side="left")
        ctk.CTkButton(barra, text="Salvar", width=86, height=40, corner_radius=10,
                      font=FONTE_P, fg_color=ACENTO, hover_color=ACENTO_2,
                      text_color="#ffffff",
                      command=self._salvar_chave).pack(side="left", padx=6)
        ctk.CTkButton(barra, text="Limpar", width=86, height=40, corner_radius=10,
                      font=FONTE_P, fg_color="transparent",
                      hover_color=HOVER_ITEM, text_color=VERMELHO,
                      command=lambda: self._salvar_chave(limpar=True)).pack(side="left")

        card_info = ctk.CTkFrame(tela, fg_color=CARD, corner_radius=16)
        card_info.pack(fill="x", pady=6)
        ctk.CTkLabel(card_info, text=f"📁   Pasta do projeto\n{nucleo.PASTA_BASE}",
                     font=FONTE_P, justify="left", text_color=TXT_MEDIO
                     ).pack(anchor="w", padx=16, pady=10)
        ctk.CTkLabel(card_info, text=f"🗂   Chats salvos em\n{nucleo.PASTA_CHATS}",
                     font=FONTE_P, justify="left", text_color=TXT_MEDIO
                     ).pack(anchor="w", padx=16, pady=(0, 12))

    def _salvar_chave(self, limpar=False):
        nucleo.CFG["chave_nuvem"] = None if limpar else \
            (self.chave_entry.get().strip() or None)
        nucleo.salvar_cfg(nucleo.CFG)
        self._atualizar_status()
        mbox.showinfo("OK", "Configuração salva! Com internet + chave, "
                      "uso a IA grande da nuvem. ☁")

    # ── SAIR ─────────────────────────────────────────────────
    def _sair(self):
        try:
            nucleo.salvar_chat(self.chat, nucleo.CFG["modelo"])
        except Exception:
            pass
        # despedida: o Jarvis fala "até logo" antes de fechar
        nome = nucleo.CFG.get("nome_user")
        vocativo = f", {nome}" if nome else ""
        self.title("MINI-JARVIS — até logo… 👋")
        self._bolha(f"Até logo{vocativo}! 👋 Qualquer coisa, é só me chamar. "
                    "Estou sempre aqui.", ferramenta=True)

        def despedir_e_fechar():
            if nucleo.CFG.get("falar"):
                self._falar(f"Até logo{vocativo}! Qualquer coisa, "
                            "é só me chamar.")
            time.sleep(1.0)
            self.after(0, self.destroy)

        threading.Thread(target=despedir_e_fechar, daemon=True).start()

# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = JarvisApp()
    app.mainloop()
