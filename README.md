# DESCRIPTION

Very simple aiogram bot template. Reference and idea: https://github.com/Tishka17/tgbot_template

Stack: aiogram, PostgreSQL (SQLAlchemy + asyncpg), aioschedule, redis, alembic + psycopg2.

# How to use

### 1. Create and activate virtual environment
### 2. Then install requirements

```
python install -r requirements.txt
```

### 3. Initialize alembic in terminal
```
alembic init database/migrations
```
##### Configurate alembic.ini
```
sqlalchemy.url = postgresql+psycopg2://username:password@localhost/dbname
```

##### Edit env.py and add the following lines
```
from app import Base
target_metadata = Base.metadata
```

##### Then create a revision file in terminal
```
alembic revision --autogenerate -m "init"
```
##### And running upgrade
```
alembic upgrade heads
```

### Create .env file:

```
BOT_TOKEN=  <-(Here bot token from BotFather

PG_HOST=localhost
PG_USERNAME=postgres
PG_PASSWORD= <-(your postgres password)
PG_DATABASE= <-(here database name)

WEBHOOK_URL= <-(here webhook url)
```

### 5. Change admin IDs in config.py (line 34)

### 6. Now start bot to check
```
python app.py
```

