from fastapi import WebSocket
from typing import Dict, List

class WebSocketManager:
    def __init__(self):
        self.user_sockets: Dict[str, WebSocket] = {}  
        self.followers: Dict[str, List[str]] = {}  
        self.community_members: Dict[str, List[str]] = {}  

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.user_sockets[username] = websocket  

    async def disconnect(self, username: str):
        if username in self.user_sockets:
            del self.user_sockets[username]

    async def send_to_user(self, username: str, message: str):
        if username in self.user_sockets:
            await self.user_sockets[username].send_text(message)

    async def send_to_users(self, usernames: List[str], message: str):
        for user in usernames:
            if user in self.user_sockets:
                await self.user_sockets[user].send_text(message)

    def add_follower(self, followed: str, follower: str):
        if followed not in self.followers:
            self.followers[followed] = []
        self.followers[followed].append(follower)

    def add_community_member(self, community: str, username: str):
        if community not in self.community_members:
            self.community_members[community] = []
        self.community_members[community].append(username)

    async def notify_follow(self, followed: str, follower: str):
        if followed in self.user_sockets:
            await self.send_to_user(followed, f"{follower} followed you!")

    async def notify_new_post(self, username: str):
        if username in self.followers:
            await self.send_to_users(self.followers[username], f"{username} posted a new update!")

    async def notify_post_vote(self, post_owner: str, voter: str, vote_type: str):
        if post_owner in self.user_sockets:
            await self.send_to_user(post_owner, f"{voter} {vote_type} your post!")

    async def notify_comment_reply(self, comment_owner: str, replier: str):
        if comment_owner in self.user_sockets:
            await self.send_to_user(comment_owner, f"{replier} replied to your comment!")

    async def notify_community_post(self, community: str, username: str):
        if community in self.community_members:
            await self.send_to_users(self.community_members[community], f"{username} posted in {community} community!")

websocket_manager = WebSocketManager()
