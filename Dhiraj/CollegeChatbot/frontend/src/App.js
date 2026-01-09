import React, { useState } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, sender: 'user', timestamp: new Date().toLocaleTimeString() }]);
      setIsLoading(true);
      try {
        const response = await fetch('http://localhost:5001/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: input }),
        });
        const data = await response.json();
        setMessages(prev => [...prev, { text: data.response, sender: 'bot', timestamp: new Date().toLocaleTimeString() }]);
      } catch (error) {
        setMessages(prev => [...prev, { text: 'Bot: Error connecting to server', sender: 'bot', timestamp: new Date().toLocaleTimeString() }]);
      }
      setIsLoading(false);
      setInput('');
    }
  };

  const handleClearChat = () => {
    setMessages([]);
  };

  return (
    <div className="app">
      <div className="header">
        <h1>College Chatbot</h1>
      </div>
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.sender === 'user' ? 'user' : 'bot'}`}
          >
            <div>{msg.text}</div>
            <div className="timestamp">{msg.timestamp}</div>
          </div>
        ))}
        {isLoading && <div className="loading">Loading...</div>}
      </div>
      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about courses, deadlines, or faculty..."
          disabled={isLoading}
        />
        <button onClick={handleSend} disabled={isLoading}>
          Send
        </button>
        <button onClick={handleClearChat} className="clear-button">
          Clear Chat
        </button>
      </div>
    </div>
  );
}

export default App;