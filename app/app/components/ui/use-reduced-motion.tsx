"use client";

import { useEffect, useState } from 'react';

/**
 * Hook to detect user's motion preference
 * Requirements: 8.4 - Implement prefers-reduced-motion media query
 * 
 * @returns boolean - true if user prefers reduced motion
 */
export function useReducedMotion(): boolean {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    // Check if window is available (client-side)
    if (typeof window === 'undefined') return;

    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    
    // Set initial value
    setPrefersReducedMotion(mediaQuery.matches);

    // Listen for changes
    const handleChange = (event: MediaQueryListEvent) => {
      setPrefersReducedMotion(event.matches);
    };

    // Modern browsers
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handleChange);
      return () => mediaQuery.removeEventListener('change', handleChange);
    } 
    // Fallback for older browsers
    else {
      mediaQuery.addListener(handleChange);
      return () => mediaQuery.removeListener(handleChange);
    }
  }, []);

  return prefersReducedMotion;
}

/**
 * Hook to get animation duration based on motion preference
 * Returns 0 if user prefers reduced motion, otherwise returns the specified duration
 * 
 * @param duration - Animation duration in milliseconds
 * @returns number - Adjusted duration based on user preference
 */
export function useAnimationDuration(duration: number): number {
  const prefersReducedMotion = useReducedMotion();
  return prefersReducedMotion ? 0 : duration;
}

/**
 * Hook to conditionally apply animations
 * Returns empty string if user prefers reduced motion, otherwise returns the animation class
 * 
 * @param animationClass - CSS animation class name
 * @returns string - Animation class or empty string
 */
export function useConditionalAnimation(animationClass: string): string {
  const prefersReducedMotion = useReducedMotion();
  return prefersReducedMotion ? '' : animationClass;
}

/**
 * Component wrapper that respects motion preferences
 * Disables animations for children if user prefers reduced motion
 */
export function MotionWrapper({ 
  children, 
  className = '' 
}: { 
  children: React.ReactNode;
  className?: string;
}) {
  const prefersReducedMotion = useReducedMotion();
  
  return (
    <div 
      className={className}
      data-reduced-motion={prefersReducedMotion}
      style={prefersReducedMotion ? {
        animation: 'none',
        transition: 'none',
      } : undefined}
    >
      {children}
    </div>
  );
}

/**
 * Safe animation component that respects motion preferences
 * Automatically disables animations if user prefers reduced motion
 */
export function SafeAnimation({
  children,
  animationClass,
  duration = 300,
  delay = 0,
}: {
  children: React.ReactNode;
  animationClass: string;
  duration?: number;
  delay?: number;
}) {
  const prefersReducedMotion = useReducedMotion();
  
  if (prefersReducedMotion) {
    return <>{children}</>;
  }
  
  return (
    <div
      className={animationClass}
      style={{
        animationDuration: `${duration}ms`,
        animationDelay: `${delay}ms`,
      }}
    >
      {children}
    </div>
  );
}
