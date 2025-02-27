from database.models import async_session
from database.models import TradeSignal
from sqlalchemy import select, update, delete, desc
from decimal import Decimal
from datetime import datetime

def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner


@connection
async def set_user(session, tg_id):
    #async with async_session() as session:
    user = await session.scalar(select(User).where(User.tg_id == tg_id))

    if not user:
        session.add(User(tg_id=tg_id, balance='0.05'))
        await session.commit()


@connection
async def create_trade_signal(session, symbol, entry_price, market_cap, rank):
    # Получаем текущий день недели
    day_of_week = datetime.now().strftime('%A')
    
    # Создаем объект TradeSignal
    trade_signal = TradeSignal(
        symbol=symbol,
        date=datetime.now().date(),
        entry_price=entry_price,
        exit_price=0.0,  # Пока что 0
        market_cap=market_cap,
        rank=rank,
        volume_24h=0.0,  # Пока что 0
        day_of_week=day_of_week
    )
    
    # Добавляем в сессию и коммитим
    session.add(trade_signal)
    await session.commit()


