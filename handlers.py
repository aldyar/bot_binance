from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
#from monitoring import monitor  # Импортируем функцию мониторинга
import asyncio
from request import fetch_data, check_red_candles
from pairs import pairs
import keyboards as kb

monitoring_active = False
router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    """
    Обработчик команды /start. Приветствует пользователя.
    """
    await message.answer("Привет! Я бот для мониторинга криптовалют.", reply_markup=kb.main)


@router.message(F.text == 'Старт мониторинга🚀')
async def monitor_handler(message: Message):
    """
    Обработчик команды /monitor. Запускает мониторинг криптовалют.
    """
    global monitoring_active
    if monitoring_active:
        await message.answer("Мониторинг уже запущен!")
    else:
        monitoring_active = True  # Запускаем мониторинг
        await message.answer("Мониторинг криптовалют начат! Это может занять время...⏳")
        await monitor(message)


@router.message(F.text == 'Стоп⏸️')
async def stop_monitoring_handler(message: Message):
    """
    Обработчик команды /stop. Останавливает мониторинг криптовалют.
    """
    global monitoring_active
    if monitoring_active:
        monitoring_active = False  # Останавливаем мониторинг
        await message.answer("Мониторинг был остановлен.")
    else:
        await message.answer("Мониторинг не был запущен.")








async def monitor(message):
    """
    Главная функция для мониторинга криптовалют.
    """
    global monitoring_active
    symbols = pairs  # Добавьте нужные пары
    while monitoring_active:  # Пока флаг true, мониторинг работает
        for symbol in symbols:
            ohlcv = await fetch_data(symbol)
            if ohlcv and check_red_candles(ohlcv):
                await message.answer(f"🚨 Уведомление: у {symbol} шесть подряд красных свечей!")
        await asyncio.sleep(14400)  # Интервал проверки (14400 секунд)