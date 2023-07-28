import json
    
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from backend import settings
from channels.layers import get_channel_layer
from chat.models import GroupChat , Member

@database_sync_to_async
def searchClientIsMemberGroup(group_id , user_email_chat ):
    members = Member.objects.filter( group_id__id = group_id )
    list_client = []
    for member in members:
     if user_email_chat != member.user_id.email :
        client = searchClientEmail(member.user_id.email)
        if client != False:
            list_client.append(client)
    return list_client
def deleteLoggedInCLient(id_client):
    for i in settings.CLIENTS_ARRAY:
        if i['id'] == id_client :
            settings.CLIENTS_ARRAY.remove(i)
def searchClientById(id):
    for i in settings.CLIENTS_ARRAY:
        # print("email _ search" , address , len(settings.CLIENTS_ARRAY) )
        # print("client:", i['id'], "email:", i['user_from'], 'conversation:', i['conversation'])
        if i['id'] == id:
            return i
    return False

def searchClient(address, port):
    for i in settings.CLIENTS_ARRAY:
        # print("email _ search" , address , len(settings.CLIENTS_ARRAY) )
        # print("client:", i['id'], "email:", i['user_from'], 'conversation:', i['conversation'])
        if i['address'] == address and i['port'] == port :
            return i
    return False
def searchClientEmail(email):
    for i in settings.CLIENTS_ARRAY:
        if i['user_from'] == email:
            return i
    return False
def deleteClientDisconnect(address , port):
    for i in settings.CLIENTS_ARRAY:
        # print("email _ search" , address)
        # print("client:", i['id'], "email:", i['user_from'], 'conversation:', i['conversation'])
        if i['address'] == address and i['port'] == port :
            settings.CLIENTS_ARRAY.remove(i)

def changeInformationClient(client_id , user_from , user_to , conversation):
    for i in range(len(settings.CLIENTS_ARRAY)):
        if client_id == settings.CLIENTS_ARRAY[i]['id']:
            settings.CLIENTS_ARRAY[i]['user_from'] = user_from
            settings.CLIENTS_ARRAY[i]['user_to']= user_to
            settings.CLIENTS_ARRAY[i]['conversation'] = conversation
def changInforGroupClient(client_id , user_from , conversation , group_id):
    for i in range(len(settings.CLIENTS_ARRAY)):
        if client_id == settings.CLIENTS_ARRAY[i]['id']:
            settings.CLIENTS_ARRAY[i]['user_from'] = user_from
            settings.CLIENTS_ARRAY[i]['conversation'] = conversation
            settings.CLIENTS_ARRAY[i]['group_id'] = group_id
def initClient(client_id , user_from):
    for i in range(len(settings.CLIENTS_ARRAY)):
        if client_id == settings.CLIENTS_ARRAY[i]['id']:
            settings.CLIENTS_ARRAY[i]['user_from']= user_from

def displayClient():
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    for i in settings.CLIENTS_ARRAY:
        print("client:", i['id'], "email:", i['user_from'] , i['group_id'])
        print("----------------------------------------------------------------------------------------")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        id_client = self.scope["url_route"]["kwargs"]["id_client"]
        try:
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_group_name = "chat_%s" % self.room_name
            await self.channel_layer.group_add(
                self.room_group_name, self.channel_name
            )
        except:
            pass
        self.room_notify = id_client
        await self.channel_layer.group_add(
            self.room_notify, self.channel_name
        )
        #join infor client
        deleteLoggedInCLient(id_client)
        if (
            searchClient(self.scope["client"][0], self.scope["client"][1]) == False
        ):
            clientNew = {
                "id" : id_client ,
                "user_from": False,
                'address': self.scope["client"][0],
                'port' : self.scope["client"][1], 
                'conversation': False,
                'user_to': False,
                'channel_name' : id_client, 
                'group_id' : False
            }
            settings.CLIENTS_ARRAY.append(clientNew)

        # Join room group
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        clients = settings.CLIENTS
        try:
            deleteClientDisconnect(self.scope['client'][0] , self.scope['client'][1])
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        except Exception as e:
            print(e)
        try:
            await self.channel_layer.group_discard(self.room_notify, self.channel_name)
        except Exception as e:
            print(e)
        displayClient()
    # Receive message from WebSocket
    async def receive(self, text_data):
        clients = settings.CLIENTS
        text_data_json = json.loads(text_data)
        init = text_data_json['init_socket']
        client_id = text_data_json['client_id']

        clientCurrent = searchClient(self.scope['client'][0] , self.scope['client'][1] )
        print("clientCurrent",clientCurrent)
        print("intit: " , init)
        if init == 0:
            if clientCurrent != False :
                initClient(client_id,  text_data_json['user_from'])
            displayClient()
        elif init == 1:
            if clientCurrent != False :
                changeInformationClient(
                    client_id , text_data_json['user_from'] , 
                    text_data_json['user_to'] , text_data_json['conversation']
                )
            displayClient()
        # Send message to room group
        elif init == 2:
            if clientCurrent != False:
                message = text_data_json["message"]

                await self.channel_layer.group_send(
                    self.room_group_name, {
                        "type": "chat_message", "message": message , 
                        "email_user_chat" : text_data_json['email_user_chat'] ,
                        "client_id" : text_data_json['client_id'] ,
                        "client" : clientCurrent
                    }
                )
                user_to_value = clientCurrent['user_to']
                clientTo =searchClientEmail(user_to_value)
                if clientTo != False:
                    print('clientTo: ',clientTo)
                    if clientTo != False:
                        channel_name_value = str(clientTo['channel_name'])
                        await self.channel_layer.group_send(
                            channel_name_value, {
                                "type": "chat_message_notification", "message": message , 
                                "email_user_chat" : text_data_json['email_user_chat'] , 
                                "type_chat" : 'NTFCT' 
                            }
                        )
        # init chat group          
        elif init == 3:
            if clientCurrent != False :
                changInforGroupClient(
                    client_id , text_data_json['user_from'] , 
                    text_data_json['conversation'] ,  text_data_json['group_id']
                )
            print("init Group chat")
            displayClient()
        elif init == 4:
            if clientCurrent != False:
                message = text_data_json["message"]

                await self.channel_layer.group_send(
                    self.room_group_name, {
                        "type": "chat_message", "message": message , 
                        "email_user_chat" : text_data_json['email_user_chat'] ,
                        "client_id" : text_data_json['client_id'] ,
                        "client" : clientCurrent
                    }
                )
                listClient = await  searchClientIsMemberGroup(clientCurrent['group_id'] , text_data_json['email_user_chat'] )
                for i in listClient:
                    channel_name_value = str(i['channel_name'])
                    await self.channel_layer.group_send(
                        channel_name_value, {
                            "type": "chat_message_notification", "message": message , 
                            "email_user_chat" : text_data_json['email_user_chat'] , 
                            "type_chat" : 'NTFCG' , "group_id" : clientCurrent['group_id']
                        }
                    )



    # Receive message from room group
    async def chat_message(self, event):
        try:
            message = event["message"]
            client = event["client"]
            emailUserChat = event['email_user_chat']
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                "content": message , 
                "user_to" : client['user_to'],
                "user_from" : client['user_from'] ,
                'email_user_chat' : emailUserChat ,
                "is_chat" : True
            }))
        except Exception as e:
            print("ERROR: " , e)
            pass
    async def chat_message_notification(self, event):
        try:
            message = event["message"]
            emailUserChat = event['email_user_chat']
            typeChat = event["type_chat"]
            try:
                groupId = event["group_id"]
            except:
                groupId = False
            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                "content": message , 
                'email_user_chat' : emailUserChat ,
                'is_chat' : False ,
                'type' : typeChat ,
                'group_id' : groupId
            }))
        except Exception as e:
            print("ERROR: " , e)
            pass
