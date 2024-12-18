// filename: Chat.tsx

import React, { useEffect, useState, useRef } from "react";
import "./Chat.css"; // 用于自定义样式

// 定义消息的类型
interface Message {
  content: string;
  role: "user" | "assistant";
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState<string>("");
  const [chat_id, setChatId] = useState<string>("");
  const [isDisabled, setIsDisabled] = useState<boolean>(false);

  const messagesRef = useRef<Message[]>(messages);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const relativePath = "/api";

  // 初始化 chat_id
  useEffect(() => {
    const savedChatId = localStorage.getItem("chat_id");
    if (savedChatId) {
      setChatId(savedChatId);
    } else {
      fetchChatId();
    }
  }, []);

  // 更新 isDisabled 时，自动聚焦输入框
  useEffect(() => {
    if (isDisabled) {
      inputRef.current?.blur();
    } else {
      inputRef.current?.focus();
    }
  }, [isDisabled]);

  // 更新 messages 时，自动滚动到底部
  useEffect(() => {
    messagesRef.current = messages;
    scrollToBottom();
  }, [messages]);

  // 当 chat_id 改变时，获取聊天历史记录
  useEffect(() => {
    if (!chat_id) return;

    fetch(`${relativePath}/chat-history?chat_id=${chat_id}`)
      .then((response) => response.json())
      .then((data) => {
        setMessages(data.history as Message[]);
      })
      .catch((error) => {
        console.error("Error fetching chat history:", error);
      });
  }, [chat_id]);

  // 滚动到底部
  const scrollToBottom = () => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // 获取 Chat ID
  const fetchChatId = async () => {
    try {
      const response = await fetch(`${relativePath}/chat-id`, {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });

      if (response.ok) {
        const data = await response.json();
        const savedChatId = data.chat_id;
        setChatId(savedChatId);
        localStorage.setItem("chat_id", savedChatId);
      } else {
        console.error("Failed to fetch chat ID");
      }
    } catch (error) {
      console.error("Error fetching chat ID:", error);
    }
  };

  // 发送消息
  const handleSendMessage = () => {
    if (input.trim()) {
      setMessages((prev) => [...prev, { content: input, role: "user" }]);
      setInput("");
      getResponse(input);
    }
  };

  // 获取响应
  const getResponse = async (input: string) => {
    if (!chat_id) {
      console.error("Chat ID not found");
      return;
    }

    setIsDisabled(true);

    const response = await fetch(`${relativePath}/chat-stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id, message: input }),
    });

    if (!response.body) {
      console.error("Failed to get response");
      setIsDisabled(false);
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let responseText = "";

    setMessages((prev) => [...prev, { content: "", role: "assistant" }]);

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        setIsDisabled(false);
        break;
      }
      responseText += decoder.decode(value, { stream: true });
      const updatedMessages = [...messagesRef.current];
      updatedMessages[updatedMessages.length - 1] = {
        content: responseText,
        role: "assistant",
      };
      setMessages(updatedMessages);
    }
  };

  // 输入框变化
  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
  };

  // 回车发送消息
  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // 输入框自适应高度
  const handleInput = () => {
    if (inputRef.current) {
      inputRef.current.style.height = "auto";
      const height = Math.min(inputRef.current.scrollHeight - 36, 200);
      inputRef.current.style.height = `${height}px`;
    }
  };

  return (
    <div className="root">
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
        <button onClick={fetchChatId} disabled={isDisabled}>
          New Chat
        </button>
        <textarea
          className="chat-input"
          placeholder="Type your message..."
          value={input}
          onChange={handleInputChange}
          onKeyDown={handleKeyPress}
          onInput={handleInput}
          ref={inputRef}
          disabled={isDisabled}
        />
        <button onClick={handleSendMessage} disabled={isDisabled}>
          Send
        </button>
      </div>
    </div>
  );
};

export default Chat;
