from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
#from monitoring import monitor  # Импортируем функцию мониторинга
import asyncio
from request import fetch_data, check_candle_pattern, get_cmc_info, get_volume_24h
from pairs import pairs
import keyboards as kb
import time
from database.request_db import create_trade_signal
monitoring_active = False
router = Router()
import logging

logging.basicConfig(level=logging.INFO)
@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Я бот для мониторинга криптовалют.", reply_markup=kb.main)


@router.message(F.text == 'Старт мониторинга🚀')
async def monitor_handler(message: Message):
    global monitoring_active
    if monitoring_active:
        await message.answer("Мониторинг уже запущен!")
    else:
        monitoring_active = True  # Запускаем мониторинг
        await message.answer("Мониторинг криптовалют начат! Это может занять время...⏳")
        await monitor(message)


@router.message(F.text == 'Стоп⏸️')
async def stop_monitoring_handler(message: Message):
    global monitoring_active
    if monitoring_active:
        monitoring_active = False  # Останавливаем мониторинг
        await message.answer("Мониторинг был остановлен.")
    else:
        await message.answer("Мониторинг не был запущен.")


async def monitor(message):

    #Главная функция для мониторинга криптовалют.

    global monitoring_active
    symbols = pairs  # Добавьте нужные пары
    while monitoring_active:  # Пока флаг true, мониторинг работает
        start_time = time.time()  # Фиксируем время начала итерации
        for symbol in symbols:
            ohlcv = await fetch_data(symbol)
            result = check_candle_pattern(ohlcv)
            if ohlcv and result:
                binance_symbol = symbol.replace('/', '_')
                binance_link = f"https://www.binance.com/ru/trade/{binance_symbol}?type=spot"
                # Получаем данные из CoinMarketCap

                entry_price = ohlcv[-1][4]  # Используем цену закрытия последней свечи как цену входа
                volume = await get_volume_24h(binance_symbol)

                filtered_pair = binance_symbol.split("/")[0]
                cmc_info = await get_cmc_info(filtered_pair)
                # Создаем объект TradeSignal
                await create_trade_signal(symbol, entry_price, cmc_info['market_cap'], cmc_info['rank'], volume)

                logging.info(f"Отправляем уведомление для {symbol}")
                await message.answer(
                    f"🚨 Уведомление: у {symbol} обнаружено {result} подряд красных свечей!\n"
                    f"💹 Ссылка на биржу: [Binance]({binance_link})",
                    disable_web_page_preview=True, parse_mode='Markdown'  # Отключить предпросмотр ссылки
                )
        elapsed_time = time.time() - start_time
        logging.info(f"Функция monitor заняла {elapsed_time:.2f} секунд")
        await asyncio.sleep(14400)  # Интервал проверки (14400 секунд)

@router.message(F.text == 'test')
async def test(message: Message):
    binance_symbol = 'TWT/USDT'
    ohlcv = await fetch_data('TWT/USDT')
    entry_price = ohlcv[-1][4]  # Используем цену закрытия последней свечи как цену входа
    volume = await get_volume_24h(binance_symbol)
    cmc_info = await get_cmc_info('TWT')
    await create_trade_signal(binance_symbol, entry_price, cmc_info['market_cap'], cmc_info['rank'], volume)