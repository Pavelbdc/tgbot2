import os
import datetime
import requests
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
HF_TOKEN = HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def generate_compliment():
    prompt = (
        "Write one short, warm, positive compliment for my girlfriend in a group chat. "
        "Make it human, natural, and different each time."
    )

    response = requests.post(
        API_URL,
        headers=headers,
        json={
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 60,
                "temperature": 0.9
            }
        },
        timeout=30
    )

    result = response.json()

    if isinstance(result, list):
        return result[0]["generated_text"]
    else:
        return "You make this day brighter just by being here."

async def send_daily(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    compliment = generate_compliment()
    await context.bot.send_message(chat_id=chat_id, text=compliment)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    await update.message.reply_text(
        "Бот активирован. Ежедневные комплименты включены ✨"
    )

    context.job_queue.run_daily(
        send_daily,
        time=datetime.time(hour=9, minute=0),
        chat_id=chat_id
    )

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))


app.run_polling()
