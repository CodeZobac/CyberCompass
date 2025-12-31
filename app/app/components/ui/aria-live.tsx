"use client";

import { useEffect, useRef } from 'react';

/**
 * ARIA Live Region Component
 * Announces dynamic content changes to screen readers
 * Requirements: 8.2 - Implement aria-live regions for dynamic content
 */

interface AriaLiveProps {
  message: string;
  politeness?: 'polite' | 'assertive' | 'off';
  clearOnUnmount?: boolean;
  atomic?: boolean;
  relevant?: 'additions' | 'removals' | 'text' | 'all';
}

export function AriaLive({
  message,
  politeness = 'polite',
  clearOnUnmount = true,
  atomic = true,
  relevant = 'additions text',
}: AriaLiveProps) {
  const regionRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    return () => {
      if (clearOnUnmount && regionRef.current) {
        regionRef.current.textContent = '';
      }
    };
  }, [clearOnUnmount]);

  if (!message) return null;

  return (
    <div
      ref={regionRef}
      role="status"
      aria-live={politeness}
      aria-atomic={atomic}
      aria-relevant={relevant}
      className="sr-only"
    >
      {message}
    </div>
  );
}

/**
 * Visually Hidden Component
 * Hides content visually but keeps it accessible to screen readers
 * Requirements: 8.2 - Use semantic HTML elements
 */
export function VisuallyHidden({ children }: { children: React.ReactNode }) {
  return <span className="sr-only">{children}</span>;
}

/**
 * Screen Reader Only Text
 * Provides additional context for screen reader users
 */
export function SROnly({ children }: { children: React.ReactNode }) {
  return <span className="sr-only">{children}</span>;
}
