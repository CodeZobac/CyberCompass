/**
 * TypingIndicator Component
 * Animated typing indicator for real-time chat
 */

'use client';

export function TypingIndicator() {
  return (
    <div className="inline-flex items-center gap-1 px-4 py-3 bg-gray-100 dark:bg-gray-800 rounded-lg">
      <div className="flex gap-1">
        <span className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce [animation-delay:-0.3s]" />
        <span className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce [animation-delay:-0.15s]" />
        <span className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" />
      </div>
    </div>
  );
}
