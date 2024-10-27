// Chat.js

import React, { useState } from 'react';
import './Chat.css'; // 用于自定义样式

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  async function getResponse(input) {
    const response = await fetch(`/api/chat`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                },
            body: JSON.stringify({ message: input })
        }
    );
    const data = await response.json();
    return data.response;
  }

  // 处理发送消息
  const handleSendMessage = () => {
    if (input.trim()) {
      setMessages((messages) => [...messages, { text: input, sender: "user" }]);
      setInput("");
      getResponse(input).then((data) => {
        setMessages((messages) => [...messages, { text: data, sender: "bot" }]);
      });
    }
  };

  // 处理输入框内容变化
  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  // 处理回车键发送消息
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSendMessage();
    }
  };

  return (
    <div className="root">
      {/* <Header /> */}
      <div className="chat-container">
        <div className="chat-box">
          {messages.map((message, index) => (
            <div key={index} className={`chat-message ${message.sender}`}>
              {message.text}
            </div>
          ))}
        </div>
        
      </div>
      <div className="input-container">
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={handleInputChange}
          onKeyDown={handleKeyPress}
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chat;
