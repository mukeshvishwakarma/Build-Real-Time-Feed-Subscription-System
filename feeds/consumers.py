import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import websockets

class FeedConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Connect to Binance WebSocket API
        self.binance_uri = "wss://dstream.binance.com/stream?streams=btcusd_perp@bookTicker"
        self.websocket = await websockets.connect(self.binance_uri)

        # Start listening for messages
        await self.channel_layer.group_add("feed_updates", self.channel_name)

        # Start receiving messages from Binance WebSocket API
        await self.receive_messages()

    async def disconnect(self, close_code):
        # Disconnect from Binance WebSocket API
        await self.websocket.close()

        # Remove from group
        await self.channel_layer.group_discard("feed_updates", self.channel_name)

    async def receive_messages(self):
        while True:
            try:
                message = await self.websocket.recv()
                await self.send(json.loads(message))
            except websockets.exceptions.ConnectionClosed:
                break

    async def send_feed_update(self, event):
        # Send feed updates to clients
        await self.send(text_data=json.dumps(event))
