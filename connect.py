from sqlalchemy import Table, Column, Integer, MetaData, String, Text, select
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

meta = MetaData()

user_table = Table(
    'users',
    meta,
    Column('id', Integer, primary_key=True),
    Column('username', String, nullable=True),
    Column('email', String, nullable=False),
    Column('bio', Text, nullable=False)
)

async def async_main():
    engine = create_async_engine("sqlite+aiosqlite:///database.db", echo=True)

    async with engine.begin() as conn:
        # Create database tables
        await conn.run_sync(meta.create_all)

        # Insert data into the 'users' table
        await conn.execute(
            user_table.insert(),
            [
                {'username': 'toyinmary', 'email': 'username@domain.com', 'bio': 'welcome to my world'},
                {'username': 'michelle', 'email': 'username@domain.com', 'bio': 'welcome to my world too'}
            ]
        )

    async with engine.connect() as conn:
        # Perform a select query
        statement = select(user_table).where(user_table.c.username == 'michelle')
        result = await conn.execute(statement)
        rows = result.fetchall()

        print(rows)

if __name__ == "__main__":
    asyncio.run(async_main())
