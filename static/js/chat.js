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
    const webSearch = document.getElementById('web-search').checked;
    
    if (message !== "") 
    {
        displayMessage(message, 'user');
        inputField.value = '';
      
        try 
        {
            const response = await sendToServer(message, webSearch);
            if (response.ok) {
              const botMessage = await response.json(); 
              const links = botMessage.links;
              addlinks(links);
              displayMessage(botMessage.response, 'bot');  
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

async function sendToServer(message, webSearch) {
    const url = '/ask'; 

    const data = {
      message: message,  
      webSearch : webSearch
    };
  
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',  
      },
      body: JSON.stringify(data),  
    });
  
    return response; 
  }

function addlinks(links)
{
  const refLink = document.getElementById('link-box')
  refLink.innerHTML = ``;
  links.forEach(link => {
    const adiv = document.createElement('div');
    adiv.innerHTML = `<a href='${link}'>${link}</a><br><br>`;
    refLink.appendChild(adiv);
  });
}