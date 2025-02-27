from sqlalchemy import ForeignKey, String, BigInteger, DateTime, Boolean, Float, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from datetime import datetime


engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3',
                             echo=True)
    
    
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class TradeSignal(Base):
    __tablename__ = 'trade_signals'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    symbol: Mapped[str] = mapped_column(String, nullable=False)  # 1. Символ криптовалюты
    date: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today)  # 2. Дата (не Unix)
    entry_price: Mapped[float] = mapped_column(Float)  # 3. Точка входа (значение с запятой)
    exit_price: Mapped[float] = mapped_column(Float)  # 4. Точка выхода (значение с запятой)
    market_cap: Mapped[float] = mapped_column(Float)  # 5. Капитализация монеты (значение с запятой)
    rank: Mapped[int] = mapped_column(Integer)  # 6. Место в рейтинге
    status: Mapped[str | None] = mapped_column(String, nullable=True, default=None)  # 7. Статус сделки (NULL по умолчанию)
    volume_24h: Mapped[float] = mapped_column(Float)  # 8. Объем торгов за 24 часа (значение с запятой)
    day_of_week: Mapped[str] = mapped_column(String)  # 9. День недели
    holding_time: Mapped[float | None] = mapped_column(Float, nullable=True, default=None)  # 10. Время удержания сделки (NULL по умолчанию)
    





async def async_main():
    async with engine.begin() as conn:
        """await conn.run_sync(Base.metadata.create_all)"""