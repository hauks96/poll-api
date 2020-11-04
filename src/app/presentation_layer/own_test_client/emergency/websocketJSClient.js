// CONNECTION CLOSES AFTER ONE SUCCESSFUL MESSAGE :(

// Create WebSocket connection.
let socket = new WebSocket('ws://localhost:8080/');

function sendMessage () {
    console.log("Trying to send: " + document.getElementById("messageIn").value);
    // socket.send(document.getElementById("messageIn").value);
    let data = document.getElementById("messageIn").value;
    socket.send(data);
}

// Listen for messages
socket.addEventListener('message', function (event) {
    var serverDiv = document.getElementById("serverRecv");
    var newP = document.createElement("p");
    var ret_data = JSON.parse(event.data)
    console.log("response: " + ret_data);
    newP.innerHTML = "Message: " + syntaxHighlight(ret_data);
    serverDiv.appendChild(newP);
});

socket.onerror = function(event) {
    console.log("WebSocket error observed:", event);
  };

  socket.onclose = function(event) {
    if (event.wasClean) {
        console.log(`[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`);
    } else {
      // e.g. server process killed or network down
      // event.code is usually 1006 in this case
      console.log('[close] Connection died');
    }
  };

function syntaxHighlight(json) {
    if (typeof json != 'string') {
         json = JSON.stringify(json, undefined, 2);
    }
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}
