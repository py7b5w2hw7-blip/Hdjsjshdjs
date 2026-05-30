import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# Твой токен уже на месте
BOT_TOKEN = '8894468235:AAGM1iscR8NyV1hzvOPXl50g_2ASHxiaPHk' 

# Включаем логирование, чтобы видеть работу бота в консоли
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 1. Ловим команду /start и отправляем счет на 100 звёзд
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Оплата услуг",
        description="Пополнение баланса бота на 100 звёзд",
        payload="user_deposit_100", # Внутренний ID платежа
        provider_token="",          # Для Telegram Stars оставляем ПУСТЫМ
        currency="XTR",             # Валюта Telegram Stars
        prices=[
            types.LabeledPrice(label="Telegram Stars", amount=100) # 100 звёзд
        ]
    )

# 2. Подтверждаем, что бот готов обработать этот платеж
@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# 3. Ловим успешную оплату
@dp.message(lambda message: message.successful_payment is not None)
async def on_successful_payment(message: types.Message):
    payment_info = message.successful_payment
    await message.answer(
        f"🎉 Спасибо за оплату! Вы успешно перевели {payment_info.total_amount} звёзд."
    )

# Запуск бота
async def main():
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
