/**
 * ConnectionRecovery Component
 * Displays connection status and provides manual reconnection option
 */

'use client';

import { useEffect, useState } from 'react';

export interface ConnectionRecoveryProps {
  connectionStatus: 'connected' | 'disconnected' | 'reconnecting';
  onReconnect: () => void;
  locale?: string;
  className?: string;
}

export function ConnectionRecovery({
  connectionStatus,
  onReconnect,
  locale = 'en',
  className = '',
}: ConnectionRecoveryProps) {
  const [showBanner, setShowBanner] = useState(false);

  useEffect(() => {
    // Show banner when disconnected or reconnecting
    setShowBanner(connectionStatus !== 'connected');
  }, [connectionStatus]);

  if (!showBanner) {
    return null;
  }

  const messages = {
    en: {
      reconnecting: 'Reconnecting to server...',
      disconnected: 'Connection lost. Your messages will be sent when reconnected.',
      reconnectButton: 'Reconnect Now',
    },
    pt: {
      reconnecting: 'Reconectando ao servidor...',
      disconnected: 'Conexão perdida. Suas mensagens serão enviadas quando reconectado.',
      reconnectButton: 'Reconectar Agora',
    },
  };

  const localeMessages = messages[locale as keyof typeof messages] || messages.en;

  const getBannerStyle = () => {
    switch (connectionStatus) {
      case 'reconnecting':
        return 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800';
      case 'disconnected':
        return 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800';
      default:
        return '';
    }
  };

  const getTextStyle = () => {
    switch (connectionStatus) {
      case 'reconnecting':
        return 'text-yellow-800 dark:text-yellow-200';
      case 'disconnected':
        return 'text-red-800 dark:text-red-200';
      default:
        return '';
    }
  };

  const getMessage = () => {
    switch (connectionStatus) {
      case 'reconnecting':
        return localeMessages.reconnecting;
      case 'disconnected':
        return localeMessages.disconnected;
      default:
        return '';
    }
  };

  return (
    <div className={`${getBannerStyle()} border-b px-4 py-3 ${className}`}>
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          {connectionStatus === 'reconnecting' && (
            <svg
              className="animate-spin h-4 w-4 text-yellow-600 dark:text-yellow-400"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
          )}
          {connectionStatus === 'disconnected' && (
            <svg
              className="h-4 w-4 text-red-600 dark:text-red-400"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
          )}
          <p className={`text-sm font-medium ${getTextStyle()}`}>
            {getMessage()}
          </p>
        </div>

        {connectionStatus === 'disconnected' && (
          <button
            onClick={onReconnect}
            className="px-3 py-1 text-sm font-medium text-red-700 dark:text-red-300 bg-red-100 dark:bg-red-900/40 rounded hover:bg-red-200 dark:hover:bg-red-900/60 transition-colors"
          >
            {localeMessages.reconnectButton}
          </button>
        )}
      </div>
    </div>
  );
}
