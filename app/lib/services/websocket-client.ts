/**
 * WebSocket Client - Real-time communication with AI Backend
 * Handles catfish chat simulations, social media interactions, and typing indicators
 */

// Types for WebSocket messages
export interface WebSocketMessage {
  type: 'agent_message' | 'typing_indicator' | 'connection_status' | 'error' | 'user_message';
  agent?: string;
  message?: string;
  timestamp?: string;
  is_typing?: boolean;
  status?: 'connected' | 'disconnected' | 'reconnecting';
  error?: string;
  session_id?: string;
}

export interface ConversationSession {
  session_id: string;
  scenario_type: 'catfish_chat' | 'social_media_simulation';
  user_id: string;
  locale: string;
  character_profile?: Record<string, any>;
  conversation_history: Array<{
    role: 'user' | 'agent';
    content: string;
    timestamp: string;
    agent_type?: string;
  }>;
}

export interface WebSocketConfig {
  url?: string;
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  heartbeatInterval?: number;
}

export type MessageHandler = (message: WebSocketMessage) => void;
export type ConnectionStatusHandler = (status: 'connected' | 'disconnected' | 'reconnecting') => void;
export type ErrorHandler = (error: Error) => void;

class WebSocketClient {
  private ws: WebSocket | null = null;
  private baseUrl: string;
  private reconnectInterval: number;
  private maxReconnectAttempts: number;
  private heartbeatInterval: number;
  private reconnectAttempts: number = 0;
  private reconnectTimer: NodeJS.Timeout | null = null;
  private heartbeatTimer: NodeJS.Timeout | null = null;
  private messageHandlers: Set<MessageHandler> = new Set();
  private connectionStatusHandlers: Set<ConnectionStatusHandler> = new Set();
  private errorHandlers: Set<ErrorHandler> = new Set();
  private isIntentionallyClosed: boolean = false;
  private currentSessionId: string | null = null;

  constructor(config: WebSocketConfig = {}) {
    // Use environment variable or default to localhost for development
    const httpUrl = process.env.NEXT_PUBLIC_AI_BACKEND_URL || 'http://localhost:8000';
    // Convert HTTP URL to WebSocket URL
    this.baseUrl = httpUrl.replace(/^http/, 'ws');
    
    this.reconnectInterval = config.reconnectInterval || 3000; // 3 seconds
    this.maxReconnectAttempts = config.maxReconnectAttempts || 5;
    this.heartbeatInterval = config.heartbeatInterval || 30000; // 30 seconds
  }

  /**
   * Connect to WebSocket endpoint for a specific scenario
   */
  connect(sessionId: string, scenarioType: 'catfish_chat' | 'social_media_simulation', userId: string): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      console.warn('WebSocket already connected');
      return;
    }

    this.isIntentionallyClosed = false;
    this.currentSessionId = sessionId;

    const endpoint = scenarioType === 'catfish_chat' 
      ? `/ws/catfish/${sessionId}?user_id=${userId}`
      : `/ws/social-media/${sessionId}?user_id=${userId}`;

    const wsUrl = `${this.baseUrl}${endpoint}`;

    try {
      this.ws = new WebSocket(wsUrl);
      this.setupEventHandlers();
    } catch (error) {
      this.handleError(new Error(`Failed to create WebSocket connection: ${error}`));
    }
  }

  /**
   * Set up WebSocket event handlers
   */
  private setupEventHandlers(): void {
    if (!this.ws) return;

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
      this.notifyConnectionStatus('connected');
      this.startHeartbeat();
    };

    this.ws.onmessage = (event) => {
      try {
        const message: WebSocketMessage = JSON.parse(event.data);
        this.handleMessage(message);
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error);
      }
    };

    this.ws.onerror = (event) => {
      console.error('WebSocket error:', event);
      this.handleError(new Error('WebSocket connection error'));
    };

    this.ws.onclose = (event) => {
      console.log('WebSocket closed:', event.code, event.reason);
      this.stopHeartbeat();
      this.notifyConnectionStatus('disconnected');

      // Attempt reconnection if not intentionally closed
      if (!this.isIntentionallyClosed && this.reconnectAttempts < this.maxReconnectAttempts) {
        this.scheduleReconnect();
      }
    };
  }

  /**
   * Send a message through WebSocket
   */
  sendMessage(message: string): void {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      this.handleError(new Error('WebSocket is not connected'));
      return;
    }

    const payload: WebSocketMessage = {
      type: 'user_message',
      message,
      timestamp: new Date().toISOString(),
      session_id: this.currentSessionId || undefined,
    };

    try {
      this.ws.send(JSON.stringify(payload));
    } catch (error) {
      this.handleError(new Error(`Failed to send message: ${error}`));
    }
  }

  /**
   * Handle incoming WebSocket messages
   */
  private handleMessage(message: WebSocketMessage): void {
    this.messageHandlers.forEach(handler => {
      try {
        handler(message);
      } catch (error) {
        console.error('Error in message handler:', error);
      }
    });
  }

  /**
   * Handle errors
   */
  private handleError(error: Error): void {
    this.errorHandlers.forEach(handler => {
      try {
        handler(error);
      } catch (err) {
        console.error('Error in error handler:', err);
      }
    });
  }

  /**
   * Notify connection status change
   */
  private notifyConnectionStatus(status: 'connected' | 'disconnected' | 'reconnecting'): void {
    this.connectionStatusHandlers.forEach(handler => {
      try {
        handler(status);
      } catch (error) {
        console.error('Error in connection status handler:', error);
      }
    });
  }

  /**
   * Schedule reconnection attempt
   */
  private scheduleReconnect(): void {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
    }

    this.reconnectAttempts++;
    this.notifyConnectionStatus('reconnecting');

    console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);

    this.reconnectTimer = setTimeout(() => {
      if (this.currentSessionId && !this.isIntentionallyClosed) {
        // Reconnect with the same session ID
        // Note: We need to store scenario type and user ID for reconnection
        this.handleError(new Error('Reconnection requires session context - please reinitialize connection'));
      }
    }, this.reconnectInterval * this.reconnectAttempts); // Exponential backoff
  }

  /**
   * Start heartbeat to keep connection alive
   */
  private startHeartbeat(): void {
    this.stopHeartbeat();
    
    this.heartbeatTimer = setInterval(() => {
      if (this.ws && this.ws.readyState === WebSocket.OPEN) {
        try {
          this.ws.send(JSON.stringify({ type: 'ping' }));
        } catch (error) {
          console.error('Failed to send heartbeat:', error);
        }
      }
    }, this.heartbeatInterval);
  }

  /**
   * Stop heartbeat
   */
  private stopHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
  }

  /**
   * Register a message handler
   */
  onMessage(handler: MessageHandler): () => void {
    this.messageHandlers.add(handler);
    // Return unsubscribe function
    return () => {
      this.messageHandlers.delete(handler);
    };
  }

  /**
   * Register a connection status handler
   */
  onConnectionStatus(handler: ConnectionStatusHandler): () => void {
    this.connectionStatusHandlers.add(handler);
    return () => {
      this.connectionStatusHandlers.delete(handler);
    };
  }

  /**
   * Register an error handler
   */
  onError(handler: ErrorHandler): () => void {
    this.errorHandlers.add(handler);
    return () => {
      this.errorHandlers.delete(handler);
    };
  }

  /**
   * Disconnect WebSocket
   */
  disconnect(): void {
    this.isIntentionallyClosed = true;
    this.stopHeartbeat();
    
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    if (this.ws) {
      this.ws.close(1000, 'Client disconnecting');
      this.ws = null;
    }

    this.currentSessionId = null;
    this.reconnectAttempts = 0;
  }

  /**
   * Get current connection state
   */
  getConnectionState(): 'connecting' | 'open' | 'closing' | 'closed' {
    if (!this.ws) return 'closed';
    
    switch (this.ws.readyState) {
      case WebSocket.CONNECTING:
        return 'connecting';
      case WebSocket.OPEN:
        return 'open';
      case WebSocket.CLOSING:
        return 'closing';
      case WebSocket.CLOSED:
        return 'closed';
      default:
        return 'closed';
    }
  }

  /**
   * Check if WebSocket is connected
   */
  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN;
  }
}

// Export singleton instance
export const websocketClient = new WebSocketClient();

// Export class for creating multiple instances if needed
export { WebSocketClient };
