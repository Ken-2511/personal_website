import React from "react";
import "./Chat.css";

function Chat() {
    function handleSend() {
        const input = document.getElementById("chat-input");
        const message = input.value;
        if (message) {
            // alert(`You typed: ${message}`);
            fetch("/api/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message: message }),
            })
            .then((response) => response.json())
            .then((data) => {
                alert(data.response);
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("An error occurred while sending your message.");
            });
            input.value = "";
        }
    }
    return (
        <div className="Chat">
        <p>Chat with me!</p>
        <input type="text" placeholder="Type a message..." id="chat-input" />
        <button onClick={handleSend}>Send</button>
        </div>
    );
}

export default Chat;