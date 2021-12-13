from channels.generic.websocket import AsyncJsonWebsocketConsumer

class NotificationConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        grp = 'comment_like_notifications_{}'.format(user.username)
        await self.channel_layer.group_add(grp, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        user = self.scope['user']
        grp = 'comment_like_notifications_{}'.format(user.username)
        await self.channel_layer.group_discard(grp, self.channel_name)

    async def notify(self, event):
        await self.send_json(event)
