"use client";

import { useEffect } from 'react';

/**
 * Keyboard Navigation Detector
 * Detects when user is navigating with keyboard and adds appropriate class to body
 * This helps show focus indicators only for keyboard users
 * Requirements: 8.1 - Implement focus indicators on all interactive elements
 */
export function KeyboardNavigationDetector() {
  useEffect(() => {
    let isUsingKeyboard = false;

    const handleKeyDown = (e: KeyboardEvent) => {
      // Tab key indicates keyboard navigation
      if (e.key === 'Tab') {
        isUsingKeyboard = true;
        document.body.classList.add('using-keyboard');
      }
    };

    const handleMouseDown = () => {
      // Mouse usage indicates not using keyboard
      isUsingKeyboard = false;
      document.body.classList.remove('using-keyboard');
    };

    const handleFocus = (e: FocusEvent) => {
      // If focus happens without keyboard, it's likely programmatic
      if (!isUsingKeyboard) {
        document.body.classList.remove('using-keyboard');
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('mousedown', handleMouseDown);
    window.addEventListener('focus', handleFocus, true);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('mousedown', handleMouseDown);
      window.removeEventListener('focus', handleFocus, true);
    };
  }, []);

  return null;
}
