from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from telegram import BotCommand

# 1. Garante o carregamento do arquivo .env
load_dotenv()

import app.rotas.telegram as telegram_module
from app.rotas.telegram import router as telegram_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔄 Inicializando aplicação e Bot do Telegram...")

    try:
        # Criar e inicializar a aplicação do Telegram
        telegram_module.bot_app = telegram_module.criar_bot_app()
        await telegram_module.bot_app.initialize()
        await telegram_module.bot_app.start()

        # Tenta registrar o menu de comandos (sem derrubar o servidor caso falhe)
        try:
            await telegram_module.bot_app.bot.set_my_commands(
                [
                    BotCommand("conversar", "📝 Iniciar envio de texto literário"),
                    BotCommand("cancelar", "❌ Cancelar submissão em andamento"),
                ]
            )
            print("✅ Comandos registrados no menu do Telegram!")
        except Exception as cmd_err:
            print(
                f"⚠️ Aviso: Não foi possível registrar os comandos no menu: {cmd_err}"
            )

        print("🚀 Servidor FastAPI e Bot rodando com sucesso!")

    except Exception as e:
        print(f"❌ Erro durante a inicialização do Bot: {e}")

    yield

    # Desligamento gracioso da aplicação
    if telegram_module.bot_app:
        try:
            await telegram_module.bot_app.stop()
            await telegram_module.bot_app.shutdown()
            print("🛑 Bot do Telegram encerrado com sucesso.")
        except Exception as e:
            print(f"⚠️ Erro ao desligar o bot: {e}")


app = FastAPI(title="Vozes do Grapiúna", lifespan=lifespan)

# Inclui as rotas do Telegram
app.include_router(telegram_router)
