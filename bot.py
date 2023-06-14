import os
from pyrogram import Client
import config
from handlers.database import Database

from aiohttp import web
from datetime import datetime

routes = web.RouteTableDef()
BOT_USERNAME = ''

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response(F"Bot @{BOT_USERNAME} is successfully running...")

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

class Bot(Client):
    def __init__(self):
        super().__init__(
            "BroadcastBot",
            bot_token=config.BOT_TOKEN,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            plugins={
                "root": "plugins"
            },
        )

    async def start(self):
        global BOT_USERNAME
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()
        BOT_USERNAME = usr_bot_me.username
        print(f"@{usr_bot_me.username} Bot Running..!")
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, os.environ.get("PORT", "8080")).start()

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped.")