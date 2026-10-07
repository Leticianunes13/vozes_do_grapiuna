import os
from fastapi import APIRouter, Request, Response, status
from sqlalchemy.orm import Session
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegram.request import HTTPXRequest

# Importações internas do seu projeto
from database.infraestruturadb import SessionLocal
from database.models import Vitrine

# Roteador FastAPI
router = APIRouter(prefix="/telegram", tags=["Telegram Bot"])

# Token do Bot
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Estados da conversa
NOME, TITULO, GENERO, TEXTO, CONTATO = range(5)

# Instância global da aplicação do bot
bot_app: Application = None


def criar_bot_app() -> Application:
    """Inicializa e configura o Application do python-telegram-bot."""
    if not TELEGRAM_TOKEN:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN não foi encontrado nas variáveis de ambiente."
        )

    # Configuração de timeout para evitar erros de conexão
    request_config = HTTPXRequest(connect_timeout=20.0, read_timeout=20.0)

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).request(request_config).build()

    # Handlers do fluxo de conversa
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler(["start", "conversar", "iniciar"], boas_vindas),
            CallbackQueryHandler(iniciar_fluxo_callback, pattern="^iniciar_fluxo$"),
        ],
        states={
            NOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_nome)],
            TITULO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receber_titulo),
                CallbackQueryHandler(pular_titulo_callback, pattern="^pular_titulo$"),
            ],
            GENERO: [CallbackQueryHandler(receber_genero_callback, pattern="^genero_")],
            TEXTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_texto)],
            CONTATO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receber_contato),
                CallbackQueryHandler(pular_contato_callback, pattern="^pular_contato$"),
            ],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
    )

    app.add_handler(conv_handler)
    return app


# ==========================================
# FUNÇÕES DE FLUXO E MENSAGENS DO TELEGRAM
# ==========================================


async def boas_vindas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envia a mensagem inicial com o botão 'Iniciar Submissão'."""
    teclado = [
        [InlineKeyboardButton("📝 Iniciar Submissão", callback_data="iniciar_fluxo")]
    ]
    reply_markup = InlineKeyboardMarkup(teclado)

    mensagem = (
        "✨ *Bem-vindo(a) ao Vozes do Grapiúna!*\n\n"
        "Este canal foi criado com o intuito de formar e promover a literatura da nossa comunidade.\n\n"
        "Clique no botão abaixo para começar a enviar sua obra literária:"
    )

    if update.message:
        await update.message.reply_text(
            mensagem, parse_mode="Markdown", reply_markup=reply_markup
        )
    return ConversationHandler.END


async def iniciar_fluxo_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback acionado ao clicar no botão 'Iniciar Submissão'."""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text=(
            "Perfeito! Vamos começar.\n\nQual é o seu **Nome** ou **Pseudônimo** de"
            " autor(a)?"
        ),
        parse_mode="Markdown",
    )
    return NOME


async def receber_nome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Guarda o nome do autor e solicita o título da obra."""
    context.user_data["nome_autor"] = update.message.text.strip()

    teclado = [
        [InlineKeyboardButton("⏩ Pular / Sem Título", callback_data="pular_titulo")]
    ]
    reply_markup = InlineKeyboardMarkup(teclado)

    await update.message.reply_text(
        f"Prazer, *{context.user_data['nome_autor']}*!\n\n"
        "Qual é o **Título** da sua obra?\n"
        "_(Se a obra não tiver título, você pode clicar no botão para pular)_",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )
    return TITULO


async def receber_titulo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Guarda o título digitado e exibe a seleção de gênero literário."""
    context.user_data["titulo_texto"] = update.message.text.strip()
    return await solicitar_genero(update.message)


async def pular_titulo_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Caso o usuário decida pular a inclusão do título."""
    query = update.callback_query
    await query.answer()

    context.user_data["titulo_texto"] = None
    return await solicitar_genero(query.message, edit=True)


async def solicitar_genero(target_message, edit: bool = False):
    """Exibe os botões inline para escolha do gênero literário."""
    teclado = [
        [
            InlineKeyboardButton("📜 Poesia", callback_data="genero_Poesia"),
            InlineKeyboardButton("📖 Conto", callback_data="genero_Conto"),
        ],
        [
            InlineKeyboardButton("🖋️ Crônica", callback_data="genero_Crônica"),
            InlineKeyboardButton("✨ Outro", callback_data="genero_Outro"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(teclado)
    texto = "Selecione o **Gênero Literário** da sua obra:"

    if edit:
        await target_message.edit_text(
            texto, parse_mode="Markdown", reply_markup=reply_markup
        )
    else:
        await target_message.reply_text(
            texto, parse_mode="Markdown", reply_markup=reply_markup
        )

    return GENERO


async def receber_genero_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Guarda o gênero selecionado via botão e solicita o texto da obra."""
    query = update.callback_query
    await query.answer()

    genero_escolhido = query.data.replace("genero_", "")
    context.user_data["genero"] = genero_escolhido

    # Usa edit_message_text no query
    await query.edit_message_text(
        text=(
            f"Gênero selecionado: *{genero_escolhido}*\n\nAgora, digite ou cole o"
            " **Texto / Conteúdo** da sua obra literária aqui no chat:"
        ),
        parse_mode="Markdown",
    )
    return TEXTO


async def receber_texto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Guarda o texto da obra e solicita dados opcionais de contato."""
    context.user_data["texto"] = update.message.text.strip()

    teclado = [
        [
            InlineKeyboardButton(
                "⏩ Finalizar Sem Contato", callback_data="pular_contato"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(teclado)

    await update.message.reply_text(
        "Texto recebido com sucesso!\n\n"
        "Para finalizarmos: informe um **Contato** (Instagram, e-mail ou WhatsApp) para podermos divulgar e dar os devidos créditos no projeto:\n"
        "_(Ou clique no botão abaixo para concluir sem informar contato)_",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )
    return CONTATO


async def receber_contato(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Salva o contato digitado e finaliza a submissão."""
    context.user_data["contato"] = update.message.text.strip()
    return await salvar_submissao_no_banco(update.message, context)


async def pular_contato_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Finaliza a submissão gravando 'Não informado' para cumprir o NOT NULL."""
    query = update.callback_query
    await query.answer()

    context.user_data["contato"] = "Não informado"
    return await salvar_submissao_no_banco(query.message, context, edit=True)


async def salvar_submissao_no_banco(
    target_message, context: ContextTypes.DEFAULT_TYPE, edit: bool = False
):
    """Persiste os dados coletados na tabela Vitrine e envia confirmação."""
    dados = context.user_data
    db: Session = SessionLocal()

    try:
        nova_submissao = Vitrine(
            nome_autor=dados.get("nome_autor"),
            titulo_texto=dados.get("titulo_texto"),
            genero=dados.get("genero"),
            texto=dados.get("texto"),
            contato=dados.get("contato") or "Não informado",
        )
        db.add(nova_submissao)
        db.commit()
        db.refresh(nova_submissao)

        resumo = (
            "🎉 *Submissão realizada com sucesso!*\n\n"
            f"👤 *Autor(a):* {nova_submissao.nome_autor}\n"
            f"📌 *Título:* {nova_submissao.titulo_texto or 'Sem Título'}\n"
            f"📖 *Texto:* {nova_submissao.texto[:100]}...\n"
            f"🎭 *Gênero:* {nova_submissao.genero}\n"
            f"📞 *Contato:* {nova_submissao.contato}\n\n"
            "Muito obrigado por contribuir com o projeto *Vozes do Grapiúna*! Sua obra foi registrada e na proxima rodada já será publicada na nossa vitrine. Fique atento(a) às novidades e compartilhe com seus amigos e familiares!"
        )

        if edit:
            await target_message.edit_text(resumo, parse_mode="Markdown")
        else:
            await target_message.reply_text(resumo, parse_mode="Markdown")

    except Exception as e:
        db.rollback()
        msg_erro = "❌ Houve um erro ao salvar sua submissão no sistema. Por favor, tente novamente."
        if edit:
            await target_message.edit_text(msg_erro)
        else:
            await target_message.reply_text(msg_erro)
        print(f"Erro ao salvar submissão: {e}")

    finally:
        db.close()
        context.user_data.clear()

    return ConversationHandler.END


async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancela o processo de submissão a qualquer momento."""
    context.user_data.clear()
    await update.message.reply_text(
        "❌ Submissão cancelada.\nQuando quiser enviar um texto, digite /conversar ou clique no menu de opções.",
        parse_mode="Markdown",
    )
    return ConversationHandler.END


# ==========================================
# ENDPOINT DO WEBHOOK PARA O FASTAPI
# ==========================================


@router.post("/webhook")
async def telegram_webhook(request: Request):
    """Recebe as atualizações de mensagens do Telegram via Webhook."""
    global bot_app

    if not bot_app:
        return Response(
            content="Bot do Telegram não inicializado",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    try:
        data = await request.json()
        update = Update.de_json(data, bot_app.bot)
        await bot_app.process_update(update)
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        print(f"Erro ao processar Webhook do Telegram: {e}")
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
