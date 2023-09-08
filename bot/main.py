from redis import asyncio as aioredis
import aiohttp
from aiogram import Bot, Dispatcher, types

import config

BOT_INFO_MSG = """
Привет! Это бот на базе <a href="https://huggingface.co/tinkoff-ai/ruDialoGPT-medium">ruDialoGPT-medium</a>, предназначенный для изучения языка программирования Scala. Исходная модель была дообучена на истории чата 
<a href="https://t.me/scala_learn">Scala Learning & Education: Ask for Review & Noob questions</a>.

Команды:
/start, /help - вывести это сообщение
/clear - очистить контекст модели
"""

# Connect to Redis
redis = aioredis.from_url(config.REDIS_URL)

# Create an instance of the bot and the dispatcher
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


async def generate_response(message: str, chat_id: int) -> str:
    context = await redis.get(f"chat_context_{chat_id}")
    context = [] if not context else context

    async with aiohttp.ClientSession() as session:
        async with session.post(
            config.MODEL_URL,
            json={"data": context + [message]},
        ) as response:
            result = await response.json()
            bot_response = result["data"]

    return bot_response


@dp.message_handler(commands=["clear"])
async def clear_chat_context(message: types.Message):
    chat_id = message.chat.id

    # Clear chat context in Redis
    await redis.delete(f"chat_context_{chat_id}")
    await message.reply("Контекст модели очищен!")


@dp.message_handler(commands=["start", "help"])
async def get_bot_info(message: types.Message):
    user_message = message.text
    chat_id = message.chat.id
    await message.reply(BOT_INFO_MSG, parse_mode=types.ParseMode.HTML)
    await redis.lpush(f"chat_history_{chat_id}", user_message, BOT_INFO_MSG)
    await redis.ltrim(f"chat_history_{chat_id}", 0, 2)


@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_message(message: types.Message):
    await message.answer_chat_action("typing")
    user_message = message.text
    chat_id = message.chat.id

    bot_response = await generate_response(user_message, chat_id)
    await message.answer(bot_response)

    # Store the user message and bot response in chat history
    await redis.lpush(f"chat_history_{chat_id}", user_message, bot_response)
    await redis.ltrim(f"chat_history_{chat_id}", 0, 2)


def main():
    # Start the bot
    from aiogram import executor

    executor.start_polling(dp)


if __name__ == "__main__":
    main()
