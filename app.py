import logging

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher.webhook import get_new_configured_app
from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from config import load_config, Config
from filters.admin import AdminFilter
from handlers import setup_handlers
from middlewares.database import DatabaseMiddleware
from middlewares.role import RoleMiddleware
from middlewares.throttling import ThrottlingMiddleware
from utils.notify_admins import notify_admins
from utils.set_bot_commands import set_default_commands

from database.base import Base


async def on_startup(web_app: web.Application) -> None:
    dp: Dispatcher = web_app.get('dp')
    config: Config = web_app.get('config')

    await dp.bot.set_webhook(f'{config.bot.webhook_url}/bot{config.bot.token}', drop_pending_updates=True)

    await set_default_commands(dp)
    await notify_admins(dp, config.bot.admins)

    logging.warning('Bot started!')


async def on_shutdown(web_app: web.Application) -> None:
    dp: Dispatcher = web_app.get('dp')
    engine: AsyncEngine = web_app.get('engine')

    await dp.storage.close()
    await dp.storage.wait_closed()
    await dp.bot.delete_webhook()
    await (await dp.bot.get_session()).close()
    await engine.dispose()

    logging.warning('Bot stopped!')


def main():
    logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s | %(name)s - %(levelname)s - %(message)s')

    config = load_config()
    if config.bot.use_redis:
        storage = RedisStorage2('localhost', 6379, db=5, pool_size=10)
    else:
        storage = MemoryStorage()

    engine: AsyncEngine = create_async_engine(
        f'postgresql+asyncpg://{config.db.username}:{config.db.password}@{config.db.host}/'
        f'{config.db.database}', echo=False, future=True)
    db_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    bot = Bot(token=config.bot.token)
    dp = Dispatcher(bot, storage=storage)

    dp.middleware.setup(ThrottlingMiddleware(limit=1))
    dp.middleware.setup(RoleMiddleware(config.bot.admins))
    dp.middleware.setup(DatabaseMiddleware(db_session))

    dp.filters_factory.bind(AdminFilter)

    setup_handlers(dp)

    app = get_new_configured_app(dispatcher=dp, path=f'/bot{config.bot.token}')
    app['dp'] = dp
    app['config'] = config
    app['engine'] = engine

    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    web.run_app(app, port=3001)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        pass
