# 🤖 MINI-JARVIS

Assistente de IA **100% seu**: roda no seu PC, **sem limite de tokens, sem assinatura, sem custo** — e fica **100% offline** depois de instalado.

## ✨ O que ele faz

| Recurso | Como usar |
|---|---|
| 🧠 Conversar | só digite na conversa |
| 📄 Criar arquivos | "crie um arquivo trabalho.txt com..." |
| 📂 Ler / listar | "o que tem na pasta?" |
| ⚡ Rodar comandos | ele pede sua permissão antes |
| 🌿 Git | `/git status`, `/git log`, `/git commit mensagem` |
| 💬 Chats salvos | salvam sozinhos em `chats/` — `abrir` retoma |
| 🌗 Tema claro/escuro | `tema` |
| 📌 Painel lateral | `painel` (sites, plugins, chats, ajustes) |
| 🔌 Plugins | solte um `.py` na pasta `plugins/` (veja `TEMPLATE.py`) |
| ☁ Modo híbrido | `painel` → `[v]` coloque chave gratuita do openrouter.ai — com internet usa IA maior |

## 🚀 Primeira vez

```
executar.bat          (ou: python jarvis.py)
```

1. Se o **Ollama** (motor da IA) não estiver instalado, o programa pede sua **permissão avançada** e instala sozinho (~1 GB).
2. Aparece a **vitrine de IAs** com a **% de chance de funcionar** no seu PC — as marcadas `⛔ NÃO INSTALE` vão travar um PC de 4 GB.
3. Escolha o número → baixa com barra de progresso → pronto!

## 📦 Gerar instalador (Inno Setup)

1. Baixe o [Inno Setup](https://jrsoftware.org/isdl.php)
2. Abra o `jarvis.iss` e clique em **Compile**
3. Sai um `Instalador-MINI-JARVIS.exe` pra distribuir 💿

## 🛡️ Segurança

- Comandos perigosos (format, del, shutdown...) são **bloqueados**
- Todo comando do Jarvis pede **confirmação sua** antes
- Comandos rodam em **prioridade baixa de CPU** (não trava o PC)
