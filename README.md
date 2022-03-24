# Aiogram Bot template

start developing your telegram bot right away!

I built this project, so i could develop my bots faster.

this bot doesn't do anything useful but it's a template for building fully functional bots.

it's an example implementation, you can do it however you like and change it to your liking!

project will be updated and new features will be added soon...

#### some other templates for Aiogram that this project is inspired by them:

- [aiogram-structured](https://github.com/amirho3inf/aiogram-structured)
- [aiogram_bot_template](https://github.com/nacknime-official/aiogram_bot_template)
- [bot](https://github.com/aiogram/bot)


## Features

this template project uses:

- [Aiogram](https://github.com/aiogram/aiogram/) (Telegram-Bot API Framework)
- [Tortoise-ORM](https://github.com/tortoise/tortoise-orm) (Db ORM)
- [Aerich](https://github.com/tortoise/aerich) (Database migrations)
- [aiomysql](https://github.com/aio-libs/aiomysql) (MySql database driver for asyncio)
- [aioredis](https://github.com/aio-libs/aioredis-py) (FSM and in memory db)

Develpment tools:  

- [flake8](https://github.com/PyCQA/flake8) (Linter)
- [Black](https://github.com/psf/black) (Formatter)
- [aiohttp-autoreload](https://github.com/anti1869/aiohttp_autoreload) (Auto reload on saving files)


## installation

### local installation for Linux

you need git and python +3.7 installed in your system

clone the repository:

first Fork this project on your github account if you want.

clone the repository: 

example:

`git clone https://github.com/sinaebrahimi1/aiogram-template.git`

change directory to project's direcotry:

`cd aiogram-template`

install `virtualenv` with pip if you don't have it:

`pip install virtualenv`

create a new virtualenv and enable it:

`python -m virtualenv .venv`

`source .venv/bin/activate`

now you need to install needed libraries:

`pip install -r requirements.txt`

now you need MySql installed on your system(or in a docker container) and also redis.

make sure to install these two dependencies for your linux distro.

you can also use sqlite or postgresql or anything else that is supported by Tortoise-ORM.

now it's time to create `.env` file and enter your configuration:

`mv .env.example .env`

open the `.env` file in your editor and complete the required variables and any other configuration you want based on `app/config.py` file.

`PROXY_URL` is optional, it's useful if you live in a country that telegram is banned.

I'ts done!

now you can test it:

first make `bot.py` file executable: `chmod +x app/bot.py`

run the bot: `app/bot.py` or `cd app && ./bot.py`

also you can run the bot in auto-reload mode 
so it will reload the application every time you change a file:

`./bot.py --reload`



## Deployment

### deploy with docker

- soon...

## TODO

- [ ] None

## 

If you have any question or it's anything wrong with the app just open a github issue.

Any suggestion or contribution will be appreciated.