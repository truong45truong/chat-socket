from enum import Enum


class DBTable(str, Enum):
    USER = 'users'
    GROUPCHAT ='groupchats'
    MEMBER = 'members'
    CONVERSATION = 'conversations'
    CHAT = 'chats'
    NOTIFICATION = 'notifications'
    MEMBERSHIP = 'memberships'