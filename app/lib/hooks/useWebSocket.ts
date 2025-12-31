/**
 * React Hook for WebSocket connections
 * Provides easy-to-use interface for real-time AI chat features
 */

import { useEffect, useState, useCallback, useRef } from 'react';
import { 
  websocketClient, 
  WebSocketMessage, 
  ConversationSession 
} from '../services/websocket-client';

export interface UseWebSocketOptions {
  sessionId: string;
  scenarioType: 'catfish_chat' | 'social_media_simulation';
  userId: string;
  autoConnect?: boolean;
  onMessage?: (message: WebSocketMessage) => void;
  onError?: (error: Error) => void;
}

export interface UseWebSocketReturn {
  // Connection state
  isConnected: boolean;
  connectionStatus: 'connected' | 'disconnected' | 'reconnecting';
  
  // Typing indicator state
  isAgentTyping: boolean;
  
  // Messages
  messages: WebSocketMessage[];
  
  // Actions
  sendMessage: (message: string) => void;
  connect: () => void;
  disconnect: () => void;
  clearMessages: () => void;
  
  // Error state
  error: Error | null;
}

export function useWebSocket(options: UseWebSocketOptions): UseWebSocketReturn {
  const {
    sessionId,
    scenarioType,
    userId,
    autoConnect = true,
    onMessage: externalOnMessage,
    onError: externalOnError,
  } = options;

  const [isConnected, setIsConnected] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected' | 'reconnecting'>('disconnected');
  const [isAgentTyping, setIsAgentTyping] = useState(false);
  const [messages, setMessages] = useState<WebSocketMessage[]>([]);
  const [error, setError] = useState<Error | null>(null);
  
  // Use refs to avoid recreating handlers on every render
  const externalOnMessageRef = useRef(externalOnMessage);
  const externalOnErrorRef = useRef(externalOnError);

  useEffect(() => {
    externalOnMessageRef.current = externalOnMessage;
    externalOnErrorRef.current = externalOnError;
  }, [externalOnMessage, externalOnError]);

  // Message handler
  const handleMessage = useCallback((message: WebSocketMessage) => {
    // Update typing indicator
    if (message.type === 'typing_indicator') {
      setIsAgentTyping(message.is_typing || false);
    }
    
    // Add message to history
    if (message.type === 'agent_message' || message.type === 'user_message') {
      setMessages(prev => [...prev, message]);
    }
    
    // Handle connection status messages
    if (message.type === 'connection_status') {
      setConnectionStatus(message.status || 'disconnected');
    }
    
    // Handle error messages
    if (message.type === 'error') {
      const errorObj = new Error(message.error || 'Unknown WebSocket error');
      setError(errorObj);
      externalOnErrorRef.current?.(errorObj);
    }
    
    // Call external handler
    externalOnMessageRef.current?.(message);
  }, []);

  // Connection status handler
  const handleConnectionStatus = useCallback((status: 'connected' | 'disconnected' | 'reconnecting') => {
    setConnectionStatus(status);
    setIsConnected(status === 'connected');
    
    if (status === 'disconnected') {
      setIsAgentTyping(false);
    }
  }, []);

  // Error handler
  const handleError = useCallback((err: Error) => {
    setError(err);
    externalOnErrorRef.current?.(err);
  }, []);

  // Connect function
  const connect = useCallback(() => {
    try {
      websocketClient.connect(sessionId, scenarioType, userId);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to connect');
      handleError(error);
    }
  }, [sessionId, scenarioType, userId, handleError]);

  // Disconnect function
  const disconnect = useCallback(() => {
    websocketClient.disconnect();
  }, []);

  // Send message function
  const sendMessage = useCallback((message: string) => {
    if (!isConnected) {
      const error = new Error('Cannot send message: WebSocket is not connected');
      handleError(error);
      return;
    }

    try {
      websocketClient.sendMessage(message);
      
      // Add user message to local state immediately for better UX
      const userMessage: WebSocketMessage = {
        type: 'user_message',
        message,
        timestamp: new Date().toISOString(),
      };
      setMessages(prev => [...prev, userMessage]);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to send message');
      handleError(error);
    }
  }, [isConnected, handleError]);

  // Clear messages function
  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  // Set up WebSocket event listeners
  useEffect(() => {
    const unsubscribeMessage = websocketClient.onMessage(handleMessage);
    const unsubscribeStatus = websocketClient.onConnectionStatus(handleConnectionStatus);
    const unsubscribeError = websocketClient.onError(handleError);

    return () => {
      unsubscribeMessage();
      unsubscribeStatus();
      unsubscribeError();
    };
  }, [handleMessage, handleConnectionStatus, handleError]);

  // Auto-connect on mount if enabled
  useEffect(() => {
    if (autoConnect) {
      connect();
    }

    // Cleanup on unmount
    return () => {
      disconnect();
    };
  }, [autoConnect, connect, disconnect]);

  return {
    isConnected,
    connectionStatus,
    isAgentTyping,
    messages,
    sendMessage,
    connect,
    disconnect,
    clearMessages,
    error,
  };
}

/**
 * Hook for managing typing indicators separately
 * Useful for displaying typing status in UI
 */
export function useTypingIndicator() {
  const [typingAgents, setTypingAgents] = useState<Set<string>>(new Set());

  useEffect(() => {
    const unsubscribe = websocketClient.onMessage((message) => {
      if (message.type === 'typing_indicator' && message.agent) {
        setTypingAgents(prev => {
          const next = new Set(prev);
          if (message.is_typing) {
            next.add(message.agent!);
          } else {
            next.delete(message.agent!);
          }
          return next;
        });
      }
    });

    return unsubscribe;
  }, []);

  return {
    typingAgents: Array.from(typingAgents),
    isAnyoneTyping: typingAgents.size > 0,
  };
}
