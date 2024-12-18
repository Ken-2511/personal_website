// filename: Chat.js

import React, { useEffect, useState, useRef } from "react";
import './Chat.css'; // 用于自定义样式

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [chat_id, setChatId] = useState("");
  const messagesRef = useRef(messages);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);
  const [isDisabled, setIsDisabled] = useState(false);

  const relativePath = "/api";
  // const relativePath = "http://chengyongkang.me:8000/api"; // when deploying, change it to be the relative path

  // initialize chat_id, if not exist, get a new one from the server
  useEffect(() => {
    let savedChatId = localStorage.getItem("chat_id");

    if (savedChatId) {
      setChatId(savedChatId);
    } else {
      fetchChatId();
    }
  }, []);

  // 更新 isDisabled 时，自动聚焦输入框
  useEffect(() => {
    if (isDisabled) {
      if (inputRef.current)
        inputRef.current.blur();
    } else {
      if (inputRef.current)
        inputRef.current.focus();
    }
  }, [isDisabled]);

  // 更新 message 时，更新 ref
  useEffect(() => {
    messagesRef.current = messages;
    scrollToBottom();
  }, [messages]);

  // get chat history when chat_id changes
  useEffect(() => {
    if (!chat_id) {
      return;
    }
    console.log("Fetching chat history for chat ID:", chat_id);
    fetch(`${relativePath}/chat-history?chat_id=${chat_id}`)
      .then((response) => response.json())
      .then((data) => {
        setMessages(data.history);
        console.log("Chat history fetched:", data.history);
        // 如果消息列表是空的，自动发送一次消息请求自我介绍
        // if (data.history.length === 0) {
        //   getResponse("Who are you?");
        // }
      })
      .catch((error) => {
        console.error("Error fetching chat history:", error);
      });
  }
  , [chat_id]);

  const scrollToBottom = () => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  async function getResponse(input) {
    if (!chat_id) {
      console.error("Chat ID not found");
      return;
    }
    // 设置禁用状态，防止用户发送多次请求
    setIsDisabled(true);
    const response = await fetch(`${relativePath}/chat-stream`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        chat_id: chat_id,
        message: input,
      }),
    });

    if (!response.body) {
      console.error("Failed to get response");
      setIsDisabled(false);
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let responseText = "";

    // 添加一个初始的空消息到消息列表中
    setMessages((messages) => [...messages, { content: "", role: "assistant" }]);

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        setIsDisabled(false);
        break;
      }
      const chunk = decoder.decode(value, { stream: true });
      responseText += chunk;

      // 直接更新所有消息，而不是在回调中引用原变量
      const updatedMessages = [...messagesRef.current];
      updatedMessages[updatedMessages.length - 1] = {
        content: responseText,
        role: "assistant",
      }
      setMessages(updatedMessages);
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
    // 回复期间禁用输入
    if (input.trim()) {
      setMessages((messages) => [...messages, { content: input, role: "user" }]);
      setInput("");
      // 等待更新状态完成后再获取回复
      setTimeout(() => {
        getResponse(input);
      }, 0);
    }
  };

  // 处理输入框内容变化
  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  // 修改回车键的处理逻辑，按下 Enter 发送消息，Shift + Enter 换行
  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault(); // 防止默认行为，即在 textarea 中换行
      handleSendMessage();
    }
  };

  // 处理输入框高度自适应
  const handleInput = (e) => {
    if (inputRef.current) {
      inputRef.current.style.height = "auto";
      const height = Math.min(inputRef.current.scrollHeight - 36, 200);
      inputRef.current.style.height = `${height}px`;
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
          <div className="gap" ref={bottomRef} />
        </div>
      </div>
      <div className="input-container">
        <button 
        onClick={fetchChatId}
        disabled={isDisabled}
        >New Chat</button>
        <textarea
            className="chat-input"
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={handleInputChange}
            onKeyDown={handleKeyPress}
            onInput={handleInput}
            ref={inputRef}
            disabled={isDisabled}
          />
        <button 
          onClick={handleSendMessage}
          disabled={isDisabled}
        >Send</button>
      </div>
    </div>
  );
};

export default Chat;
