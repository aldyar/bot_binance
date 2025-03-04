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

days_mapping = {
    "Monday": "Понедельник",
    "Tuesday": "Вторник",
    "Wednesday": "Среда",
    "Thursday": "Четверг",
    "Friday": "Пятница",
    "Saturday": "Суббота",
    "Sunday": "Воскресенье"
}
@connection
async def create_trade_signal(session, symbol, entry_price,test, market_cap, rank, volume):
    
    # Создаем объект TradeSignal
    trade_signal = TradeSignal(
        symbol=symbol,
        #date=datetime.now().date(),
        entry_price=entry_price,
        exit_price=test, 
        market_cap = int(market_cap),
        rank=rank,
        status = 'open',
        volume_24h=int(volume),  
        day_of_week = days_mapping[datetime.now().strftime('%A')]

    )
    
    # Добавляем в сессию и коммитим
    session.add(trade_signal)
    await session.commit()


