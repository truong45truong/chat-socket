const chatSocket = new WebSocket(
  'ws://'
  + window.location.host
  + '/ws/chat/'
  + 123
  + '/'
);

chatSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);
};

chatSocket.onclose = function(e) {
  console.error('Chat socket closed unexpectedly');
};
