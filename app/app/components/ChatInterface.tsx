/**
 * ChatInterface Component
 * Real-time chat interface for AI agent conversations with typing indicators
 */

'use client';

import { useState, useRef, useEffect } from 'react';
import { useWebSocket } from '@lib/hooks/useWebSocket';
import { WebSocketMessage } from '@lib/services/websocket-client';
import { TypingIndicator } from './TypingIndicator';
import { ConnectionRecovery } from './ConnectionRecovery';

export interface ChatInterfaceProps {
  sessionId: string;
  scenarioType: 'catfish_chat' | 'social_media_simulation';
  userId: string;
  locale?: string;
  onError?: (error: Error) => void;
  onMessageSent?: () => void;
  className?: string;
}

export function ChatInterface({
  sessionId,
  scenarioType,
  userId,
  locale = 'en',
  onError,
  onMessageSent,
  className = '',
}: ChatInterfaceProps) {
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const {
    isConnected,
    connectionStatus,
    isAgentTyping,
    messages,
    sendMessage,
    connect,
    error,
  } = useWebSocket({
    sessionId,
    scenarioType,
    userId,
    autoConnect: true,
    onError,
  });

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isAgentTyping]);

  // Focus input when connected
  useEffect(() => {
    if (isConnected) {
      inputRef.current?.focus();
    }
  }, [isConnected]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!inputMessage.trim() || !isConnected) {
      return;
    }

    sendMessage(inputMessage);
    setInputMessage('');
    
    // Call the callback if provided
    if (onMessageSent) {
      onMessageSent();
    }
  };

  const getConnectionStatusText = () => {
    switch (connectionStatus) {
      case 'connected':
        return locale === 'pt' ? 'Conectado' : 'Connected';
      case 'reconnecting':
        return locale === 'pt' ? 'Reconectando...' : 'Reconnecting...';
      case 'disconnected':
        return locale === 'pt' ? 'Desconectado' : 'Disconnected';
    }
  };

  const getConnectionStatusColor = () => {
    switch (connectionStatus) {
      case 'connected':
        return 'bg-green-500';
      case 'reconnecting':
        return 'bg-yellow-500';
      case 'disconnected':
        return 'bg-red-500';
    }
  };

  return (
    <div className={`flex flex-col h-full ${className}`}>
      {/* Connection Recovery Banner */}
      <ConnectionRecovery
        connectionStatus={connectionStatus}
        onReconnect={connect}
        locale={locale}
      />

      {/* Error Display */}
      {error && (
        <div className="px-4 py-2 bg-red-50 dark:bg-red-900/20 border-b border-red-200 dark:border-red-800">
          <p className="text-sm text-red-600 dark:text-red-400">
            {locale === 'pt' ? 'Erro: ' : 'Error: '}
            {error.message}
          </p>
        </div>
      )}

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 dark:text-gray-400 mt-8">
            {locale === 'pt' 
              ? 'Comece a conversa enviando uma mensagem...' 
              : 'Start the conversation by sending a message...'}
          </div>
        )}

        {messages.map((message, index) => (
          <ChatMessage
            key={`${message.timestamp}-${index}`}
            message={message}
            locale={locale}
          />
        ))}

        {/* Typing Indicator */}
        {isAgentTyping && (
          <div className="flex items-start gap-2">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-medium">
              AI
            </div>
            <div className="flex-1">
              <TypingIndicator />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="p-4 border-t bg-white dark:bg-gray-900">
        <div className="flex gap-2">
          <input
            ref={inputRef}
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            disabled={!isConnected}
            placeholder={
              locale === 'pt' 
                ? 'Digite sua mensagem...' 
                : 'Type your message...'
            }
            className="flex-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed dark:bg-gray-800 dark:border-gray-700 dark:text-white"
          />
          <button
            type="submit"
            disabled={!isConnected || !inputMessage.trim()}
            className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            {locale === 'pt' ? 'Enviar' : 'Send'}
          </button>
        </div>
      </form>
    </div>
  );
}

interface ChatMessageProps {
  message: WebSocketMessage;
  locale: string;
}

function ChatMessage({ message, locale }: ChatMessageProps) {
  const isUserMessage = message.type === 'user_message';
  const isAgentMessage = message.type === 'agent_message';

  if (!isUserMessage && !isAgentMessage) {
    return null;
  }

  const formatTime = (timestamp?: string) => {
    if (!timestamp) return '';
    const date = new Date(timestamp);
    return date.toLocaleTimeString(locale === 'pt' ? 'pt-BR' : 'en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className={`flex items-start gap-2 ${isUserMessage ? 'flex-row-reverse' : ''}`}>
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-medium ${
          isUserMessage ? 'bg-gray-500' : 'bg-blue-500'
        }`}
      >
        {isUserMessage ? 'U' : 'AI'}
      </div>

      {/* Message Content */}
      <div className={`flex-1 max-w-[70%] ${isUserMessage ? 'items-end' : 'items-start'}`}>
        <div
          className={`px-4 py-2 rounded-lg ${
            isUserMessage
              ? 'bg-gray-500 text-white'
              : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white'
          }`}
        >
          {message.agent && (
            <div className="text-xs font-medium mb-1 opacity-75">
              {message.agent}
            </div>
          )}
          <p className="text-sm whitespace-pre-wrap break-words">{message.message}</p>
        </div>
        <div className="text-xs text-gray-500 dark:text-gray-400 mt-1 px-1">
          {formatTime(message.timestamp)}
        </div>
      </div>
    </div>
  );
}
