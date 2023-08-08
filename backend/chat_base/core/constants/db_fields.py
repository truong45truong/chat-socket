from enum import Enum


class DBUserFields(str, Enum):
    ID = 'id'
    EMAIL = 'email'
    PASSWORD = 'password'
    IS_ACTIVE = 'is_active'
    IS_STAFF = 'is_staff'
    IS_SUPERUSER = 'is_superuser'
    NAME = 'name'
    CREATED_AT = 'created_at'
    UPDATED_AT = 'updated_at'  
class DBGroupChatFields(str , Enum):
    ID = 'id'
    NAME ='name'
    DESCRIPTION = 'description'

class DBMemberFields(str , Enum):
    ID = 'id'
    NAME ='name'
    DESCRIPTION = 'description'

class DBConversationFields(str , Enum):
    ID = 'id'
    GROUP_ID = 'group_id'
    CONTENT_LAST = 'content_last'
    USER_FROM ='user_from'
    USER_TO = 'user_to'
    CREATED_AT ='created_at'
    LIST_USER_SEEM ='list_user_seen'
    LIST_MESSAGE_SENT = 'list_message_sent'
class DBChatFields (str , Enum ):
    ID = 'id'
    USER_ID = 'user_id'
    CONVERSATION_ID = 'conversation_id'
    CONTENT = 'content'
    CREATED_AT ='created_at'
class DBNotificationFields (str , Enum):
    ID = 'id'

class DBMemberShipFields ( str , Enum):
    FROM_USER = 'from_user'
    TO_USER = 'to_user'