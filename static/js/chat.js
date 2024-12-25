document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('message-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') 
    {
        sendMessage();
    }
});

async function sendMessage() 
{
    const inputField = document.getElementById('message-input');
    const message = inputField.value.trim();
    
    if (message !== "") 
    {
        displayMessage(message, 'user');
        inputField.value = '';
      
        try 
        {
            const response = await sendToServer(message);
            if (response.ok) {
              const botMessage = await response.json();  // Giả sử server trả về JSON
              displayMessage(botMessage.response, 'bot');  // Hiển thị phản hồi từ server
            } else {
              displayMessage("Sorry, there was an error processing your message.", 'bot');
            }
        } 
        catch (error) 
        {
            console.error("Error sending message:", error);
            displayMessage("An error occurred. Please try again.", 'bot');
        }

    }
  }
  
function displayMessage(message, sender) 
{
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);

    const messageText = document.createElement('p');
    messageText.textContent = message;

    messageElement.appendChild(messageText);
    chatBox.appendChild(messageElement);

    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendToServer(message) {
    const url = '/ask';  // URL server nhận tin nhắn
  
    const data = {
      message: message,  // Gửi tin nhắn dưới dạng 'message'
    };
  
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',  // Gửi dữ liệu dưới dạng JSON
      },
      body: JSON.stringify(data),  // Chuyển đối tượng thành JSON string
    });
  
    return response;  // Trả về phản hồi từ server
  }

