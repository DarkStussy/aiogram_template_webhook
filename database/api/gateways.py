import typing

from sqlalchemy import select

from database.models.account import User


class BaseGateway:
    def __init__(self, session):
        self.session = session


class Gateway(BaseGateway):
    """Database gateway"""

    async def merge(self, model):
        """
        Merge models
        Example: await gateway.merge(User(id=1, username='user'))
        """
        async with self.session() as s:
            await s.merge(model)
            await s.commit()

    async def delete(self, model):
        """
        Delete models
        Example: await gateway.delete(user)
        """
        async with self.session() as s:
            await s.delete(model)
            await s.commit()

    @property
    def user(self):
        return UserGateway(self.session)


class UserGateway(BaseGateway):
    async def get_by_chat_id(self, chat_id: int) -> User:
        async with self.session() as s:
            user = await s.get(User, chat_id)
        return user

    async def get_all(self) -> typing.Iterable[User]:
        async with self.session() as s:
            users = await s.execute(select(User))
        return users.scalars()

    async def create_new_user(self, chat_id: int, username: str) -> User:
        async with self.session() as s:
            user = await s.merge(User(id=chat_id, username=username))
            await s.commit()
        return user
