import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import openai
import sys

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

class Reference:
    def __init__(self):
        self.reference = ""


reference = Reference()
model_name = "gpt-3.5-turbo"


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot created by AndyGrigs!\nHow can I help you?")

def clear_reference():
    reference.reference = ""

@dp.message_handler(commands=["clear"])
async def clear_reference_command(message: types.Message):
    clear_reference()
    await message.reply("Reference cleared")

@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    help_command = """
    /start - Start the bot
    /help - Show this help message
    /clear - Clear the reference
    """
    await message.reply(help_command)


# function to generate response
@dp.message_handler()
async def generate_response(message: types.Message):
    print(message.text)
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[
            {"role": "system", "content": reference.reference},
            {"role": "user", "content": message.text}
        ],
        temperature=0.7,
    )
    reference.response = response["choices"][0]["message"]["content"]
    print(reference.response)
    await bot.send_message(message.chat.id, reference.response)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)