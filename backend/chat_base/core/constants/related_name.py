from enum import Enum


class RelatedName(str , Enum):
    USERS = "users"
    USER_CHAT = "users_chats"
    USER_GROUP = "users_groups"
    USER_MEMBERS = "users_members"
    MEMBER_GROUP = "members_groups"
    USER_FROM_CONVERSATIONS = 'user_from_conversations'
    USER_TO_CONVERSATIONS = 'user_to_conversations'
    CONVERSATION_GROUP = 'conversations_groups'
    CHATS_USER = 'chats_users'
    CHAT_CONVERSATION = 'conversations'
    NOTIFICATION_USER = 'notifications_user'
    NOTIFICATION_CONVERSATION = 'notifications_conversations'
