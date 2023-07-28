


const chatSocket = new WebSocket(
  'ws://'
  + "0.0.0.0:8000"
  + '/ws/chat/'
  + "room_1"
  + '/'
);

chatSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);
  console.log(data)
};
console.log(chatSocket)
chatSocket.onclose = function(e) {
  console.error('Chat socket closed unexpectedly');
};
chatSocket.send(JSON.stringify({
          'message': "hahaha"
      }));