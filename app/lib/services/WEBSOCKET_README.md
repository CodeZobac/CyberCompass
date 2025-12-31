# WebSocket Client Implementation

This directory contains the WebSocket client implementation for real-time communication with the AI Backend.

## Overview

The WebSocket client enables real-time features including:
- **Catfish Chat Simulations**: Interactive conversations with AI agents that simulate suspicious online personas
- **Social Media Simulations**: Real-time social media feed generation and interaction tracking
- **Typing Indicators**: Human-like typing delays to make conversations feel natural
- **Connection Recovery**: Automatic reconnection with exponential backoff
- **Error Handling**: Comprehensive error handling with user-friendly messages

## Architecture

### Core Components

1. **WebSocketClient** (`websocket-client.ts`)
   - Low-level WebSocket connection management
   - Message routing and event handling
   - Automatic reconnection with exponential backoff
   - Heartbeat mechanism to keep connections alive

2. **useWebSocket Hook** (`../hooks/useWebSocket.ts`)
   - React hook for easy WebSocket integration
   - State management for connection status and messages
   - Typing indicator state
   - Error handling

3. **UI Components** (`../../app/components/`)
   - `ChatInterface`: Complete chat UI with message display
   - `TypingIndicator`: Animated typing indicator
   - `ConnectionRecovery`: Connection status banner with manual reconnect
   - `CatfishChatSimulation`: Example implementation

## Usage

### Basic WebSocket Connection

```typescript
import { websocketClient } from '@/lib/services/websocket-client';

// Connect to a catfish chat session
websocketClient.connect(
  'session-123',           // Session ID
  'catfish_chat',          // Scenario type
  'user-456'               // User ID
);

// Listen for messages
const unsubscribe = websocketClient.onMessage((message) => {
  console.log('Received:', message);
});

// Send a message
websocketClient.sendMessage('Hello!');

// Disconnect when done
websocketClient.disconnect();

// Clean up listener
unsubscribe();
```

### Using the React Hook

```typescript
import { useWebSocket } from '@/lib/hooks/useWebSocket';

function MyChatComponent() {
  const {
    isConnected,
    connectionStatus,
    isAgentTyping,
    messages,
    sendMessage,
    error,
  } = useWebSocket({
    sessionId: 'session-123',
    scenarioType: 'catfish_chat',
    userId: 'user-456',
    autoConnect: true,
  });

  return (
    <div>
      <p>Status: {connectionStatus}</p>
      {isAgentTyping && <p>Agent is typing...</p>}
      
      {messages.map((msg, i) => (
        <div key={i}>{msg.message}</div>
      ))}
      
      <button onClick={() => sendMessage('Hello!')}>
        Send
      </button>
    </div>
  );
}
```

### Using the Complete Chat Interface

```typescript
import { ChatInterface } from '@/app/components/ChatInterface';

function MyPage() {
  return (
    <div className="h-screen">
      <ChatInterface
        sessionId="session-123"
        scenarioType="catfish_chat"
        userId="user-456"
        locale="en"
        onError={(error) => console.error(error)}
      />
    </div>
  );
}
```

## Message Types

### Incoming Messages

```typescript
interface WebSocketMessage {
  type: 'agent_message' | 'typing_indicator' | 'connection_status' | 'error';
  agent?: string;              // Agent name (e.g., 'catfish_character')
  message?: string;            // Message content
  timestamp?: string;          // ISO timestamp
  is_typing?: boolean;         // Typing indicator state
  status?: 'connected' | 'disconnected' | 'reconnecting';
  error?: string;              // Error message
}
```

### Outgoing Messages

```typescript
// User message
{
  type: 'user_message',
  message: 'Hello!',
  timestamp: '2024-01-15T10:30:00Z',
  session_id: 'session-123'
}

// Heartbeat (automatic)
{
  type: 'ping'
}
```

## Connection Management

### Automatic Reconnection

The client automatically attempts to reconnect when the connection is lost:
- **Exponential Backoff**: Retry intervals increase with each attempt (3s, 6s, 9s, 12s, 15s)
- **Max Attempts**: 5 reconnection attempts before giving up
- **Status Updates**: Connection status is broadcast to all listeners

### Manual Reconnection

Users can manually trigger reconnection through the UI:

```typescript
const { connect } = useWebSocket({ ... });

// Trigger manual reconnection
connect();
```

### Heartbeat

A heartbeat mechanism keeps the connection alive:
- Sends ping every 30 seconds
- Detects stale connections
- Triggers reconnection if needed

## Error Handling

### Error Types

1. **Connection Errors**
   - Failed to establish connection
   - Network unavailable
   - Backend service down

2. **Message Errors**
   - Invalid message format
   - Failed to send message
   - Message parsing errors

3. **Timeout Errors**
   - Connection timeout
   - Message send timeout

### Error Recovery

```typescript
const { error } = useWebSocket({
  sessionId: 'session-123',
  scenarioType: 'catfish_chat',
  userId: 'user-456',
  onError: (error) => {
    // Custom error handling
    console.error('WebSocket error:', error);
    
    // Show user-friendly message
    toast.error(error.message);
  },
});
```

## Configuration

### Environment Variables

```env
# AI Backend URL (automatically converted to WebSocket URL)
NEXT_PUBLIC_AI_BACKEND_URL=http://localhost:8000
```

### Custom Configuration

```typescript
import { WebSocketClient } from '@/lib/services/websocket-client';

const customClient = new WebSocketClient({
  url: 'ws://custom-backend:8000',
  reconnectInterval: 5000,        // 5 seconds
  maxReconnectAttempts: 10,
  heartbeatInterval: 60000,       // 60 seconds
});
```

## Backend Integration

### Expected Backend Endpoints

The WebSocket client expects the following backend endpoints:

1. **Catfish Chat**: `ws://backend/ws/catfish/{session_id}?user_id={user_id}`
2. **Social Media**: `ws://backend/ws/social-media/{session_id}?user_id={user_id}`

### Backend Message Format

The backend should send messages in the following format:

```json
{
  "type": "agent_message",
  "agent": "catfish_character",
  "message": "Hey! How are you?",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Typing Indicators

The backend should send typing indicators before sending messages:

```json
// Start typing
{
  "type": "typing_indicator",
  "agent": "catfish_character",
  "is_typing": true
}

// Stop typing (send with actual message)
{
  "type": "typing_indicator",
  "agent": "catfish_character",
  "is_typing": false
}
```

## Testing

### Manual Testing

1. Start the AI backend service
2. Open the application in a browser
3. Navigate to a chat simulation page
4. Verify connection status indicator shows "Connected"
5. Send messages and verify they appear in the chat
6. Verify typing indicators appear before agent responses
7. Disconnect the backend and verify reconnection attempts
8. Verify error messages are displayed appropriately

### Automated Testing

```typescript
// Example test
import { WebSocketClient } from '@/lib/services/websocket-client';

describe('WebSocketClient', () => {
  it('should connect and send messages', async () => {
    const client = new WebSocketClient();
    
    client.connect('test-session', 'catfish_chat', 'test-user');
    
    await waitForConnection(client);
    
    client.sendMessage('Test message');
    
    // Verify message was sent
    expect(mockWebSocket.send).toHaveBeenCalled();
  });
});
```

## Performance Considerations

### Message Batching

For high-frequency updates, consider batching messages:

```typescript
// Backend should batch typing indicators
// Instead of sending every keystroke, send every 500ms
```

### Memory Management

The client automatically cleans up resources:
- Removes event listeners on disconnect
- Clears timers and intervals
- Releases WebSocket connection

### Scalability

For production deployments:
- Use WebSocket load balancers
- Implement session affinity (sticky sessions)
- Monitor connection counts and message rates
- Set up connection limits per user

## Troubleshooting

### Connection Issues

**Problem**: WebSocket fails to connect

**Solutions**:
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check CORS configuration on backend
3. Verify WebSocket URL is correct
4. Check browser console for errors

### Message Not Received

**Problem**: Messages sent but not received

**Solutions**:
1. Verify connection is open: `client.isConnected()`
2. Check message format matches expected schema
3. Verify message handlers are registered
4. Check backend logs for errors

### Reconnection Loops

**Problem**: Client keeps reconnecting

**Solutions**:
1. Check backend health and stability
2. Verify session ID is valid
3. Check for authentication issues
4. Review backend logs for rejection reasons

## Future Enhancements

- [ ] Message queuing for offline support
- [ ] Message delivery confirmation (ACK)
- [ ] Binary message support for media
- [ ] Compression for large messages
- [ ] End-to-end encryption
- [ ] Multi-tab synchronization
- [ ] Presence indicators (online/offline)
- [ ] Read receipts
- [ ] Message editing and deletion
- [ ] File upload through WebSocket

## References

- [WebSocket API Documentation](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
- [FastAPI WebSocket Documentation](https://fastapi.tiangolo.com/advanced/websockets/)
- [React Hooks Best Practices](https://react.dev/reference/react)
