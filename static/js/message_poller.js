const messageContainer = document.getElementById("messages");

function scrollToBottom() {
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

async function updateMessages() {
    if (document.hidden) return;

    const atBottom =
        messageContainer.scrollHeight -
        messageContainer.scrollTop -
        messageContainer.clientHeight < 100;

    try {
        const response = await fetch(
            "/chat/{{chat.id}}/messages"
        );

        if (!response.ok) return;

        const html = await response.text();

        if (messageContainer.innerHTML !== html) {
            messageContainer.innerHTML = html;

            if (atBottom) {
                scrollToBottom();
            }
        }

    } catch (error) {
        console.log("Message update failed:", error);
    }
}

updateMessages();
scrollToBottom();
setInterval(updateMessages, 3000);