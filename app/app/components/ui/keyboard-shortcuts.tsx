"use client";

import { useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';

/**
 * Keyboard Shortcuts Hook
 * Provides global keyboard shortcuts for common actions
 * Requirements: 8.1 - Add keyboard shortcuts for common actions
 */

export interface KeyboardShortcut {
  key: string;
  ctrl?: boolean;
  alt?: boolean;
  shift?: boolean;
  description: string;
  action: () => void;
}

export function useKeyboardShortcuts(shortcuts: KeyboardShortcut[], enabled = true) {
  useEffect(() => {
    if (!enabled) return;

    const handleKeyDown = (event: KeyboardEvent) => {
      for (const shortcut of shortcuts) {
        const ctrlMatch = shortcut.ctrl ? event.ctrlKey || event.metaKey : !event.ctrlKey && !event.metaKey;
        const altMatch = shortcut.alt ? event.altKey : !event.altKey;
        const shiftMatch = shortcut.shift ? event.shiftKey : !event.shiftKey;
        
        if (
          event.key.toLowerCase() === shortcut.key.toLowerCase() &&
          ctrlMatch &&
          altMatch &&
          shiftMatch
        ) {
          // Don't prevent default for input fields unless it's a specific shortcut
          const target = event.target as HTMLElement;
          const isInput = target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.isContentEditable;
          
          if (!isInput || shortcut.ctrl || shortcut.alt) {
            event.preventDefault();
            shortcut.action();
          }
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [shortcuts, enabled]);
}

/**
 * Global Keyboard Shortcuts Component
 * Provides application-wide keyboard shortcuts
 */
export function GlobalKeyboardShortcuts() {
  const router = useRouter();

  const shortcuts: KeyboardShortcut[] = [
    {
      key: 'h',
      alt: true,
      description: 'Go to home page',
      action: () => router.push('/'),
    },
    {
      key: 'd',
      alt: true,
      description: 'Go to deepfake detection',
      action: () => router.push('/deepfake-training'),
    },
    {
      key: 's',
      alt: true,
      description: 'Go to social media simulation',
      action: () => router.push('/social-media-sim'),
    },
    {
      key: 'c',
      alt: true,
      description: 'Go to catfish detection',
      action: () => router.push('/catfish-training'),
    },
    {
      key: 'a',
      alt: true,
      description: 'Go to analytics dashboard',
      action: () => router.push('/analytics'),
    },
    {
      key: '/',
      ctrl: true,
      description: 'Show keyboard shortcuts',
      action: () => {
        // This will be handled by the KeyboardShortcutsHelp component
        window.dispatchEvent(new CustomEvent('toggle-shortcuts-help'));
      },
    },
  ];

  useKeyboardShortcuts(shortcuts);

  return null;
}

/**
 * Keyboard Shortcuts Help Dialog
 * Displays available keyboard shortcuts
 */
export function KeyboardShortcutsHelp() {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const handleToggle = () => setIsOpen(prev => !prev);
    window.addEventListener('toggle-shortcuts-help', handleToggle);
    return () => window.removeEventListener('toggle-shortcuts-help', handleToggle);
  }, []);

  if (!isOpen) return null;

  const shortcuts = [
    { keys: ['Alt', 'H'], description: 'Go to home page' },
    { keys: ['Alt', 'D'], description: 'Go to deepfake detection' },
    { keys: ['Alt', 'S'], description: 'Go to social media simulation' },
    { keys: ['Alt', 'C'], description: 'Go to catfish detection' },
    { keys: ['Alt', 'A'], description: 'Go to analytics dashboard' },
    { keys: ['Ctrl', '/'], description: 'Show/hide this help' },
    { keys: ['Tab'], description: 'Navigate between interactive elements' },
    { keys: ['Shift', 'Tab'], description: 'Navigate backwards' },
    { keys: ['Enter'], description: 'Activate focused element' },
    { keys: ['Escape'], description: 'Close dialogs and menus' },
  ];

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4"
      onClick={() => setIsOpen(false)}
      role="dialog"
      aria-modal="true"
      aria-labelledby="shortcuts-title"
    >
      <div
        className="bg-white border-6 border-black shadow-brutal-lg max-w-2xl w-full max-h-[80vh] overflow-y-auto"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-6 border-b-4 border-black bg-brutal-blue text-white">
          <h2 id="shortcuts-title" className="text-2xl font-black uppercase">
            ⌨️ Keyboard Shortcuts
          </h2>
        </div>
        
        <div className="p-6">
          <div className="space-y-3">
            {shortcuts.map((shortcut, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 border-2 border-black bg-brutal-gray-50"
              >
                <span className="font-semibold">{shortcut.description}</span>
                <div className="flex gap-2">
                  {shortcut.keys.map((key, keyIndex) => (
                    <kbd
                      key={keyIndex}
                      className="px-3 py-1 bg-white border-2 border-black font-mono font-bold text-sm"
                    >
                      {key}
                    </kbd>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <button
            onClick={() => setIsOpen(false)}
            className="mt-6 w-full px-6 py-3 bg-brutal-blue text-white border-4 border-black font-black uppercase shadow-brutal-sm hover-press focus:outline-none focus:ring-4 focus:ring-brutal-blue"
          >
            Close (Esc)
          </button>
        </div>
      </div>
    </div>
  );
}

// Import useState
import { useState } from 'react';
