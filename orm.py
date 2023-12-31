from sqlalchemy import Column, ForeignKey, Integer, String, Text, select
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import asyncio

# Create a base class for declarative models
Base = declarative_base()

# Define the User class
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    email = Column(String)
    comments = relationship("Comment", back_populates='user')

    def __repr__(self) -> str:
        return f"<User username={self.username}>"

# Define the Comment class
class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    text = Column(Text, nullable=False)
    user = relationship("User", back_populates='comments')

    def __repr__(self) -> str:
        return f"<Comment text={self.text} by {self.user.username}>"

async def insert_data(sessionmaker: AsyncSession):
    async with sessionmaker() as session:
        async with session.begin():
            user1 = User(
                username='michelle',
                email='username@domain.com',
                comments=[
                    Comment(text='kindly subscribe'),
                    Comment(text='you may comment on my videos to support')
                ]
            )
            session.add(user1)

            user2 = User(
                username='toyinmary',
                email='username@domain.com',
                comments=[
                    Comment(text='click the like button'),
                    Comment(text='check my profile for more videos')
                ]
            )
            session.add(user2)

            session.commit()

#select, update data
async def select_update(sessionmaker: AsyncSession):

    async with sessionmaker() as session:
        statement = select(User).where(
            User.username == 'michelle'
        )

        result = await session.execute(statement)

        print(result.all())

async def async_main():
    engine = create_async_engine(
        "sqlite+aiosqlite:///database2.db",
        echo=True
    )

    # Create session with async_sessionmaker
    async_session = sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession
    )

    async with engine.begin() as conn:
        # Use conn.run_sync to execute DDL (Data Definition Language) statements
        await conn.run_sync(Base.metadata.create_all)

        # await insert_data(async_session)
        await select_update(async_session)

# Run the async_main function
asyncio.run(async_main())
