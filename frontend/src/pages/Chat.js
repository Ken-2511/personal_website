// filename: Chat.js

import React, { useEffect, useState } from 'react';
import './Chat.css'; // 用于自定义样式

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [chat_id, setChatId] = useState("");
  const relativePath = "http://chengyongkang.me:8000/api"; // when deploying, change it to be the relative path

  // initialize chat_id, if not exist, get a new one from the server
  useEffect(() => {
    let savedChatId = localStorage.getItem("chat_id");

    if (savedChatId) {
      setChatId(savedChatId);
    } else {
      fetchChatId();
    }
  }, []);

  // get chat history when chat_id changes
  useEffect(() => {
    if (chat_id) {
      console.log("Fetching chat history for chat ID:", chat_id);
      fetch(`${relativePath}/chat-history?chat_id=${chat_id}`)
        .then((response) => response.json())
        .then((data) => {
          setMessages(data.history);
          console.log("Chat history fetched:", data.history);
        })
        .catch((error) => {
          console.error("Error fetching chat history:", error);
        });
    }
  }
  , [chat_id]);

  async function getResponse(input) {
    if (!chat_id) {
      console.error("Chat ID not found");
      return;
    }
    const response = await fetch(`${relativePath}/chat-stream`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                },
            body: JSON.stringify({
                chat_id: chat_id,
                message: input,
            }),
        }
    );
    if (!response.body) {
      console.error("Failed to get response");
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let responseText = "";
    setMessages((messages) => [...messages, { content: "", role: "assistant" }]);
    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        break;
      }
      const chunk = decoder.decode(value, { stream: true });
      responseText += chunk;
      setMessages((messages) => {
        messages[messages.length - 1].content = responseText;
        return [...messages];
      });
    }
  }

  // Define an async function to fetch chat ID
  const fetchChatId = async () => {
    try {
      const response = await fetch(`${relativePath}/chat-id`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        const data = await response.json();
        let savedChatId = data.chat_id;
        setChatId(savedChatId);
        localStorage.setItem("chat_id", savedChatId);
      } else {
        console.error("Failed to fetch chat ID");
      }
    } catch (error) {
      console.error("Error fetching chat ID:", error);
    }
  };

  // 处理发送消息
  const handleSendMessage = () => {
    if (input.trim()) {
      setMessages((messages) => [...messages, { content: input, role: "user" }]);
      setInput("");
      getResponse(input);
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
            <div key={index} className={`chat-message ${message.role}`}>
              {message.content}
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
        <button onClick={fetchChatId}>New Chat</button>
      </div>
    </div>
  );
};

export default Chat;
