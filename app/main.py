import os
import discord
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment variables from .env
load_dotenv()

TOKEN = os.getenv("TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


class Message(BaseModel):
    message: str


@app.post("/send")
async def send_msg(data: Message):
    try:
        channel = await client.fetch_channel(DISCORD_CHANNEL_ID)

        await channel.send(f"📨 Web Message: {data.message}")

        print("✅ Sent:", data.message)

        return {"detail": "Message sent to Discord!"}

    except Exception as e:
        print("❌", e)
        return {"detail": str(e)}


@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")


async def main():
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info",
    )

    server = uvicorn.Server(config)

    await client.login(TOKEN)

    await asyncio.gather(
        client.connect(),
        server.serve(),
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())