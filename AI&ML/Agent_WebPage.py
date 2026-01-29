"""
Simple AI Agent using pydantic-ai with Web Interface
This agent can answer questions, perform calculations, and search for information
"""

import os
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import json

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import asyncio


# Define the dependencies that the agent can use
@dataclass
class AgentDeps:
    """Dependencies available to the agent"""
    user_name: str
    context: dict[str, str] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}


# Create the agent - returns str by default
agent = Agent(
    'openai:gpt-4o-mini',
    deps_type=AgentDeps,
    system_prompt=(
        "You are a helpful AI assistant named AIBotic. "
        "You can help users with questions, perform calculations, and provide information. "
        "Always be friendly, clear, and concise in your responses. "
        "When greeting users, use their name if available. "
        "When you use tools, incorporate the results naturally into your response. "
        "Always respond with plain text, not JSON or structured data."
    )
)


# Define tools for the agent
@agent.tool
def calculate(ctx: RunContext[AgentDeps], expression: str) -> str:
    """
    Perform mathematical calculations.
    
    Args:
        ctx: The context containing dependencies
        expression: A mathematical expression to evaluate (e.g., "2 + 2", "10 * 5")
    
    Returns:
        String with the calculation result
    """
    try:
        # Use eval safely with limited scope
        # Allow basic math operations
        allowed_names = {
            'abs': abs, 'round': round, 'min': min, 'max': max,
            'sum': sum, 'pow': pow
        }
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"


@agent.tool
def search_knowledge(ctx: RunContext[AgentDeps], topic: str) -> str:
    """
    Search for information about a topic.
    
    Args:
        ctx: The context containing dependencies
        topic: The topic to search for
    
    Returns:
        String with information about the topic
    """
    # Simple knowledge base (in a real application, this would query a database or API)
    knowledge_base = {
        "python": {
            "summary": "Python is a high-level programming language known for its simplicity and readability.",
            "sources": ["python.org", "Python documentation"]
        },
        "ai": {
            "summary": "Artificial Intelligence involves creating systems that can perform tasks requiring human intelligence.",
            "sources": ["AI research papers", "Machine learning textbooks"]
        },
        "pydantic": {
            "summary": "Pydantic is a data validation library using Python type hints.",
            "sources": ["pydantic-docs.helpmanual.io"]
        },
        "fastapi": {
            "summary": "FastAPI is a modern, fast web framework for building APIs with Python based on standard Python type hints.",
            "sources": ["fastapi.tiangolo.com"]
        },
        "javascript": {
            "summary": "JavaScript is a programming language commonly used for web development.",
            "sources": ["developer.mozilla.org"]
        }
    }
    
    topic_lower = topic.lower()
    for key, value in knowledge_base.items():
        if key in topic_lower:
            sources_str = ", ".join(value["sources"])
            return f"{value['summary']} Sources: {sources_str}"
    
    return f"I don't have specific information about {topic} in my knowledge base, but I'd be happy to discuss it based on general knowledge."


@agent.tool
def save_user_preference(ctx: RunContext[AgentDeps], key: str, value: str) -> str:
    """
    Save a user preference for later reference.
    
    Args:
        ctx: The context containing dependencies
        key: The preference key (e.g., "favorite_color")
        value: The preference value (e.g., "blue")
    
    Returns:
        Confirmation message
    """
    ctx.deps.context[key] = value
    return f"I've saved your preference: {key} = {value}"


@agent.tool
def get_user_preference(ctx: RunContext[AgentDeps], key: str) -> str:
    """
    Retrieve a saved user preference.
    
    Args:
        ctx: The context containing dependencies
        key: The preference key to retrieve
    
    Returns:
        The preference value or a message if not found
    """
    value = ctx.deps.context.get(key)
    if value:
        return f"Your {key} is: {value}"
    return f"I don't have a saved preference for {key}"


@agent.tool
def get_current_time(ctx: RunContext[AgentDeps]) -> str:
    """
    Get the current date and time.
    
    Args:
        ctx: The context containing dependencies
    
    Returns:
        Current date and time as a string
    """
    now = datetime.now()
    return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"


# Main interaction function
async def run_agent(user_message: str, user_name: str = "User", deps: AgentDeps = None) -> str:
    """
    Run the agent with a user message.
    
    Args:
        user_message: The message from the user
        user_name: The name of the user
        deps: Optional existing dependencies to maintain context
    
    Returns:
        The agent's response as a string
    """
    if deps is None:
        deps = AgentDeps(user_name=user_name)
    
    try:
        result = await agent.run(user_message, deps=deps)
        # Convert result to string
        response = str(result.data) if hasattr(result, 'data') else str(result)
        return response
    except Exception as e:
        print(f"Error in run_agent: {e}")
        return f"I apologize, but I encountered an error: {str(e)}"


# Example usage (CLI)
async def main():
    """Main function demonstrating the agent"""
    print("=" * 60)
    print("AI Agent Demo - pydantic-ai")
    print("=" * 60)
    print()
    
    deps = AgentDeps(user_name="Alice")
    
    # Example 1: Simple greeting
    print("Example 1: Greeting")
    response = await run_agent("Hello! My name is Alice.", user_name="Alice", deps=deps)
    print(f"User: Hello! My name is Alice.")
    print(f"Agent: {response}")
    print()
    
    # Example 2: Calculation
    print("Example 2: Calculation")
    response = await run_agent("Can you calculate 15 * 23 + 100?", user_name="Alice", deps=deps)
    print(f"User: Can you calculate 15 * 23 + 100?")
    print(f"Agent: {response}")
    print()
    
    # Example 3: Information search
    print("Example 3: Knowledge Search")
    response = await run_agent("Tell me about Python programming", user_name="Alice", deps=deps)
    print(f"User: Tell me about Python programming")
    print(f"Agent: {response}")
    print()
    
    # Example 4: Save preference
    print("Example 4: Saving Preferences")
    response = await run_agent("Save my favorite color as blue", user_name="Alice", deps=deps)
    print(f"User: Save my favorite color as blue")
    print(f"Agent: {response}")
    print()
    
    # Example 5: Get time
    print("Example 5: Get Current Time")
    response = await run_agent("What time is it?", user_name="Alice", deps=deps)
    print(f"User: What time is it?")
    print(f"Agent: {response}")
    print()


# ============================================================================
# WEB INTERFACE CLASS
# ============================================================================

class AgentWebInterface:
    """
    Web interface for the AI Agent using FastAPI and WebSockets
    Provides a modern chat interface accessible via browser
    """
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        self.host = host
        self.port = port
        self.app = FastAPI(title="AI Agent Chat Interface")
        self.active_connections: dict[str, WebSocket] = {}
        self.user_contexts: dict[str, AgentDeps] = {}
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup FastAPI routes"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def get_chat_page():
            """Serve the main chat interface"""
            return self._get_html_page()
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {"status": "healthy", "active_users": len(self.active_connections)}
        
        @self.app.websocket("/ws/{user_id}")
        async def websocket_endpoint(websocket: WebSocket, user_id: str):
            """WebSocket endpoint for real-time chat"""
            await websocket.accept()
            self.active_connections[user_id] = websocket
            
            # Initialize user context
            if user_id not in self.user_contexts:
                self.user_contexts[user_id] = AgentDeps(user_name=user_id)
            
            try:
                # Send welcome message
                await websocket.send_json({
                    "type": "message",
                    "sender": "agent",
                    "content": f"Hello {user_id}! I'm AIBotic., your AI assistant. I can help with calculations, answer questions, and remember your preferences. How can I help you today?",
                    "timestamp": datetime.now().isoformat()
                })
                
                while True:
                    # Receive message from client
                    data = await websocket.receive_json()
                    message = data.get("message", "")
                    
                    if message.strip():
                        # Send typing indicator
                        await websocket.send_json({
                            "type": "typing",
                            "sender": "agent"
                        })
                        
                        # Process message with agent
                        try:
                            response = await run_agent(
                                message, 
                                user_name=user_id,
                                deps=self.user_contexts[user_id]
                            )
                            
                            # Ensure response is a string and is JSON serializable
                            if not isinstance(response, str):
                                response = str(response)
                            
                            # Send response
                            await websocket.send_json({
                                "type": "message",
                                "sender": "agent",
                                "content": response,
                                "timestamp": datetime.now().isoformat()
                            })
                        except Exception as e:
                            print(f"Error processing message: {e}")
                            import traceback
                            traceback.print_exc()
                            await websocket.send_json({
                                "type": "error",
                                "content": "I apologize, but I encountered an error processing your message. Please try again.",
                                "timestamp": datetime.now().isoformat()
                            })
            
            except WebSocketDisconnect:
                if user_id in self.active_connections:
                    del self.active_connections[user_id]
                print(f"User {user_id} disconnected")
            except Exception as e:
                print(f"WebSocket error for user {user_id}: {e}")
                import traceback
                traceback.print_exc()
                if user_id in self.active_connections:
                    del self.active_connections[user_id]
    
    def _get_html_page(self) -> str:
        """Return the HTML page for the chat interface"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Agent Chat - Pydantic AI</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .chat-container {
            width: 100%;
            max-width: 800px;
            height: 90vh;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .chat-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .chat-header h1 {
            font-size: 24px;
            margin-bottom: 5px;
        }
        
        .chat-header p {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            background: #4ade80;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .messages-container {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f8fafc;
        }
        
        .message {
            display: flex;
            margin-bottom: 16px;
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message-content {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 18px;
            word-wrap: break-word;
            white-space: pre-wrap;
        }
        
        .message.agent .message-content {
            background: white;
            color: #1e293b;
            border: 1px solid #e2e8f0;
            border-bottom-left-radius: 4px;
        }
        
        .message.user .message-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 4px;
        }
        
        .message-sender {
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 4px;
            opacity: 0.7;
        }
        
        .message-time {
            font-size: 11px;
            margin-top: 4px;
            opacity: 0.6;
        }
        
        .typing-indicator {
            display: none;
            padding: 12px 16px;
            background: white;
            border-radius: 18px;
            border: 1px solid #e2e8f0;
            width: fit-content;
        }
        
        .typing-indicator.active {
            display: block;
        }
        
        .typing-indicator span {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #94a3b8;
            border-radius: 50%;
            margin: 0 2px;
            animation: typing 1.4s infinite;
        }
        
        .typing-indicator span:nth-child(2) {
            animation-delay: 0.2s;
        }
        
        .typing-indicator span:nth-child(3) {
            animation-delay: 0.4s;
        }
        
        @keyframes typing {
            0%, 60%, 100% {
                transform: translateY(0);
            }
            30% {
                transform: translateY(-10px);
            }
        }
        
        .input-container {
            padding: 20px;
            background: white;
            border-top: 1px solid #e2e8f0;
            display: flex;
            gap: 10px;
        }
        
        .input-container input {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 24px;
            font-size: 15px;
            outline: none;
            transition: border-color 0.3s;
        }
        
        .input-container input:focus {
            border-color: #667eea;
        }
        
        .input-container button {
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 24px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .input-container button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        .input-container button:active {
            transform: translateY(0);
        }
        
        .input-container button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        .user-name-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        
        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            text-align: center;
            max-width: 400px;
            width: 90%;
        }
        
        .modal-content h2 {
            margin-bottom: 20px;
            color: #1e293b;
        }
        
        .modal-content input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 15px;
            margin-bottom: 20px;
            outline: none;
        }
        
        .modal-content input:focus {
            border-color: #667eea;
        }
        
        .modal-content button {
            width: 100%;
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
        }
        
        .modal-content button:hover {
            opacity: 0.9;
        }
        
        .error-message {
            background: #fee;
            color: #c33;
            padding: 12px;
            border-radius: 8px;
            margin: 10px 20px;
            text-align: center;
        }
        
        .suggestions {
            padding: 10px 20px;
            background: white;
            border-top: 1px solid #e2e8f0;
        }
        
        .suggestions-title {
            font-size: 12px;
            color: #64748b;
            margin-bottom: 8px;
        }
        
        .suggestion-chips {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        
        .suggestion-chip {
            padding: 6px 12px;
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            font-size: 13px;
            color: #475569;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .suggestion-chip:hover {
            background: #e2e8f0;
            transform: translateY(-1px);
        }
    </style>
</head>
<body>
    <div class="user-name-modal" id="userNameModal">
        <div class="modal-content">
            <h2>👋 Welcome!</h2>
            <p style="margin-bottom: 20px; color: #64748b;">Enter your name to start chatting</p>
            <input type="text" id="userNameInput" placeholder="Your name" autofocus>
            <button onclick="startChat()">Start Chat</button>
        </div>
    </div>
    
    <div class="chat-container" style="display: none;" id="chatContainer">
        <div class="chat-header">
            <h1>🤖 AI Agent Chat</h1>
            <p><span class="status-indicator"></span>Powered by Pydantic AI</p>
        </div>
        
        <div class="messages-container" id="messagesContainer">
            <div class="typing-indicator" id="typingIndicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
        
        <div class="suggestions">
            <div class="suggestions-title">Try asking:</div>
            <div class="suggestion-chips">
                <div class="suggestion-chip" onclick="useSuggestion('Calculate 25 * 48')">Calculate 25 × 48</div>
                <div class="suggestion-chip" onclick="useSuggestion('Tell me about Python')">About Python</div>
                <div class="suggestion-chip" onclick="useSuggestion('What time is it?')">Current time</div>
                <div class="suggestion-chip" onclick="useSuggestion('Save my favorite food as pizza')">Save preference</div>
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="messageInput" placeholder="Type your message..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()" id="sendButton">Send</button>
        </div>
    </div>
    
    <script>
        let ws;
        let userName = '';
        
        function startChat() {
            userName = document.getElementById('userNameInput').value.trim();
            if (!userName) {
                alert('Please enter your name');
                return;
            }
            
            document.getElementById('userNameModal').style.display = 'none';
            document.getElementById('chatContainer').style.display = 'flex';
            
            connectWebSocket();
        }
        
        function connectWebSocket() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${protocol}//${window.location.host}/ws/${userName}`);
            
            ws.onopen = function() {
                console.log('Connected to chat');
            };
            
            ws.onmessage = function(event) {
                const data = JSON.parse(event.data);
                
                if (data.type === 'message') {
                    addMessage(data.content, data.sender, data.timestamp);
                    hideTypingIndicator();
                } else if (data.type === 'typing') {
                    showTypingIndicator();
                } else if (data.type === 'error') {
                    showError(data.content);
                    hideTypingIndicator();
                }
            };
            
            ws.onerror = function(error) {
                console.error('WebSocket error:', error);
                showError('Connection error. Please refresh the page.');
            };
            
            ws.onclose = function() {
                console.log('Disconnected from chat');
                showError('Disconnected from server. Please refresh the page.');
            };
        }
        
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Display user message immediately
            addMessage(message, 'user', new Date().toISOString());
            
            // Send to server
            ws.send(JSON.stringify({
                message: message
            }));
            
            // Clear input
            input.value = '';
            input.focus();
        }
        
        function useSuggestion(text) {
            document.getElementById('messageInput').value = text;
            sendMessage();
        }
        
        function addMessage(content, sender, timestamp) {
            const container = document.getElementById('messagesContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            
            const time = new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            
            messageDiv.innerHTML = `
                <div class="message-content">
                    <div class="message-sender">${sender === 'user' ? userName : 'AIBotic.'}</div>
                    ${content}
                    <div class="message-time">${time}</div>
                </div>
            `;
            
            // Insert before typing indicator
            const typingIndicator = document.getElementById('typingIndicator');
            container.insertBefore(messageDiv, typingIndicator);
            
            // Scroll to bottom
            container.scrollTop = container.scrollHeight;
        }
        
        function showTypingIndicator() {
            document.getElementById('typingIndicator').classList.add('active');
            const container = document.getElementById('messagesContainer');
            container.scrollTop = container.scrollHeight;
        }
        
        function hideTypingIndicator() {
            document.getElementById('typingIndicator').classList.remove('active');
        }
        
        function showError(message) {
            const container = document.getElementById('messagesContainer');
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            errorDiv.textContent = message;
            
            const typingIndicator = document.getElementById('typingIndicator');
            container.insertBefore(errorDiv, typingIndicator);
            
            setTimeout(() => {
                errorDiv.remove();
            }, 5000);
        }
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        // Focus on name input when page loads
        window.onload = function() {
            document.getElementById('userNameInput').focus();
        };
    </script>
</body>
</html>
        """
    
    def run(self):
        """Run the web server"""
        import uvicorn
        print(f"🚀 Starting AI Agent Web Interface...")
        print(f"📱 Open your browser and navigate to: http://localhost:{self.port}")
        print(f"🔑 Make sure OPENAI_API_KEY is set in your environment")
        print()
        
        uvicorn.run(self.app, host=self.host, port=self.port)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import sys
    
    # Check if API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        print("⚠️  Please set your OPENAI_API_KEY environment variable")
        sys.exit(1)
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # Run CLI version
        asyncio.run(main())
    else:
        # Run web interface (default)
        web_interface = AgentWebInterface(host="0.0.0.0", port=8000)
        web_interface.run()