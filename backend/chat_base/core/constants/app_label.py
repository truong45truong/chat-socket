from enum import Enum


class ModelAppLabel(str, Enum):
    USER = 'user'
    GROUPCHAT ='chat'
    MEMBER = 'chat'
    CONVERSATION = 'chat'
    CHAT = 'chat'
    NOTIFICATION = 'chat'
    MEMBERSHIP = 'user'