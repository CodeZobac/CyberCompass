'use client';

import React from 'react';
import { cn } from '@lib/utils';
import { useNetworkStatus, useOfflineSync } from '@lib/services/offline-sync';

interface ProgressCircleProps {
  progress: number;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'brutal';
  showPercentage?: boolean;
  className?: string;
}

export function ProgressCircle({ 
  progress, 
  size = 'md', 
  variant = 'brutal',
  showPercentage = true,
  className 
}: ProgressCircleProps) {
  const circumference = 2 * Math.PI * 45; // radius = 45
  const strokeDasharray = circumference;
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  const sizeClasses = {
    sm: 'w-12 h-12',
    md: 'w-16 h-16',
    lg: 'w-24 h-24',
  };

  const textSizes = {
    sm: 'text-xs',
    md: 'text-sm',
    lg: 'text-base',
  };

  return (
    <div className={cn('relative inline-flex items-center justify-center', sizeClasses[size], className)}>
      <svg 
        className="transform -rotate-90" 
        width="100%" 
        height="100%" 
        viewBox="0 0 100 100"
      >
        {/* Background circle */}
        <circle
          cx="50"
          cy="50"
          r="45"
          stroke={variant === 'brutal' ? '#000' : '#e5e7eb'}
          strokeWidth={variant === 'brutal' ? '4' : '3'}
          fill="transparent"
          className={variant === 'brutal' ? 'drop-shadow-[2px_2px_0_#000]' : ''}
        />
        {/* Progress circle */}
        <circle
          cx="50"
          cy="50"
          r="45"
          stroke={variant === 'brutal' ? '#3b82f6' : '#3b82f6'}
          strokeWidth={variant === 'brutal' ? '4' : '3'}
          fill="transparent"
          strokeDasharray={strokeDasharray}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          className={cn(
            'transition-all duration-500 ease-out',
            variant === 'brutal' && 'drop-shadow-[2px_2px_0_#1e40af]'
          )}
        />
      </svg>
      {showPercentage && (
        <div className={cn(
          'absolute inset-0 flex items-center justify-center font-bold',
          textSizes[size],
          variant === 'brutal' && 'text-black drop-shadow-[1px_1px_0_#fff]'
        )}>
          {Math.round(progress)}%
        </div>
      )}
    </div>
  );
}

interface StatusIndicatorProps {
  status: 'online' | 'offline' | 'syncing' | 'conflict';
  size?: 'sm' | 'md';
  showText?: boolean;
  className?: string;
}

export function StatusIndicator({ 
  status, 
  size = 'sm', 
  showText = false,
  className 
}: StatusIndicatorProps) {
  const statusConfig = {
    online: {
      color: 'bg-green-500',
      borderColor: 'border-green-700',
      text: 'Online',
      icon: '●',
    },
    offline: {
      color: 'bg-red-500',
      borderColor: 'border-red-700',
      text: 'Offline',
      icon: '●',
    },
    syncing: {
      color: 'bg-yellow-500',
      borderColor: 'border-yellow-700',
      text: 'Syncing',
      icon: '↻',
    },
    conflict: {
      color: 'bg-orange-500',
      borderColor: 'border-orange-700',
      text: 'Conflict',
      icon: '⚠',
    },
  };

  const config = statusConfig[status];
  
  const sizeClasses = {
    sm: 'w-3 h-3',
    md: 'w-4 h-4',
  };

  return (
    <div className={cn('flex items-center gap-2', className)}>
      <div className={cn(
        'rounded-full border-2 flex items-center justify-center font-bold text-white text-xs',
        sizeClasses[size],
        config.color,
        config.borderColor,
        'shadow-[2px_2px_0_0_#000]',
        status === 'syncing' && 'animate-pulse'
      )}>
        {size === 'md' && (
          <span className="text-[10px]">{config.icon}</span>
        )}
      </div>
      {showText && (
        <span className="text-sm font-bold uppercase tracking-wider">
          {config.text}
        </span>
      )}
    </div>
  );
}

interface ProgressIndicatorProps {
  challengeId?: string;
  userId?: string;
  progress?: number;
  className?: string;
}

export function ProgressIndicator({ 
  challengeId, 
  userId, 
  progress = 0,
  className 
}: ProgressIndicatorProps) {
  const { isOnline } = useNetworkStatus();
  const { syncInProgress, pendingItems } = useOfflineSync();

  // Determine status
  let status: 'online' | 'offline' | 'syncing' | 'conflict' = 'online';
  if (!isOnline) {
    status = 'offline';
  } else if (syncInProgress) {
    status = 'syncing';
  } else if (pendingItems > 0) {
    status = 'conflict';
  }

  return (
    <div className={cn(
      'flex items-center gap-3 p-3 bg-white border-4 border-black rounded-sm shadow-[4px_4px_0_0_#000]',
      className
    )}>
      <ProgressCircle progress={progress} size="md" />
      <div className="flex-1">
        <div className="flex items-center justify-between">
          <span className="font-bold text-sm uppercase tracking-wider">
            Progress
          </span>
          <StatusIndicator status={status} showText />
        </div>
        {pendingItems > 0 && (
          <div className="text-xs text-gray-600 mt-1">
            {pendingItems} pending sync{pendingItems !== 1 ? 's' : ''}
          </div>
        )}
      </div>
    </div>
  );
}

interface OfflineIndicatorProps {
  className?: string;
}

export function OfflineIndicator({ className }: OfflineIndicatorProps) {
  return (
    <div className={cn(
      'inline-flex items-center gap-2 px-3 py-1 bg-red-500 text-white font-bold text-xs uppercase tracking-wider',
      'border-2 border-red-700 rounded-sm shadow-[2px_2px_0_0_#000]',
      className
    )}>
      <span className="animate-pulse">●</span>
      Offline
    </div>
  );
}

interface SyncSpinnerProps {
  className?: string;
}

export function SyncSpinner({ className }: SyncSpinnerProps) {
  return (
    <div className={cn(
      'inline-flex items-center gap-2 px-3 py-1 bg-yellow-500 text-black font-bold text-xs uppercase tracking-wider',
      'border-2 border-yellow-700 rounded-sm shadow-[2px_2px_0_0_#000]',
      className
    )}>
      <span className="animate-spin">↻</span>
      Syncing
    </div>
  );
}

interface ConflictWarningProps {
  onResolve?: () => void;
  className?: string;
}

export function ConflictWarning({ onResolve, className }: ConflictWarningProps) {
  return (
    <div className={cn(
      'inline-flex items-center gap-2 px-3 py-1 bg-orange-500 text-white font-bold text-xs uppercase tracking-wider',
      'border-2 border-orange-700 rounded-sm shadow-[2px_2px_0_0_#000]',
      className
    )}>
      <span>⚠</span>
      Sync Conflict
      {onResolve && (
        <button
          onClick={onResolve}
          className="ml-2 px-2 py-1 bg-white text-orange-700 border border-orange-700 rounded-sm hover:bg-orange-50 transition-colors"
        >
          Resolve
        </button>
      )}
    </div>
  );
}

// Real-time collaboration indicator
interface CollaborationIndicatorProps {
  activeUsers?: Array<{
    id: string;
    name?: string;
    image?: string;
  }>;
  className?: string;
}

export function CollaborationIndicator({ activeUsers = [], className }: CollaborationIndicatorProps) {
  if (activeUsers.length === 0) return null;

  return (
    <div className={cn(
      'flex items-center gap-2 px-3 py-2 bg-blue-500 text-white border-2 border-blue-700 rounded-sm shadow-[2px_2px_0_0_#000]',
      className
    )}>
      <div className="flex -space-x-1">
        {activeUsers.slice(0, 3).map((user, index) => (
          <div
            key={user.id}
            className="w-6 h-6 rounded-full bg-white border-2 border-blue-700 flex items-center justify-center text-xs font-bold text-blue-700"
            title={user.name || `User ${index + 1}`}
          >
            {user.name ? user.name.charAt(0).toUpperCase() : '?'}
          </div>
        ))}
        {activeUsers.length > 3 && (
          <div className="w-6 h-6 rounded-full bg-gray-500 border-2 border-gray-700 flex items-center justify-center text-xs font-bold text-white">
            +{activeUsers.length - 3}
          </div>
        )}
      </div>
      <span className="text-xs font-bold uppercase tracking-wider">
        {activeUsers.length === 1 ? '1 User Active' : `${activeUsers.length} Users Active`}
      </span>
    </div>
  );
}
