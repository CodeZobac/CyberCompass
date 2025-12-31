import React from 'react';
import { cn } from '@lib/utils';

export interface BrutalButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'success' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export const BrutalButton = React.forwardRef<HTMLButtonElement, BrutalButtonProps>(
  ({ className, variant = 'primary', size = 'md', children, disabled, ...props }, ref) => {
    const baseStyles = 'font-bold uppercase border-4 border-black transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed';
    
    const variantStyles = {
      primary: 'bg-[var(--brutal-blue)] text-white hover:translate-x-[2px] hover:translate-y-[2px] shadow-brutal-sm hover:shadow-[2px_2px_0_0_#000]',
      secondary: 'bg-white text-black hover:translate-x-[2px] hover:translate-y-[2px] shadow-brutal-sm hover:shadow-[2px_2px_0_0_#000]',
      danger: 'bg-[var(--brutal-red)] text-white hover:translate-x-[2px] hover:translate-y-[2px] shadow-brutal-sm hover:shadow-[2px_2px_0_0_#000]',
      success: 'bg-[var(--brutal-green)] text-white hover:translate-x-[2px] hover:translate-y-[2px] shadow-brutal-sm hover:shadow-[2px_2px_0_0_#000]',
      outline: 'bg-white text-black border-4 border-black hover:bg-[var(--brutal-gray-50)] hover:translate-x-[2px] hover:translate-y-[2px] shadow-brutal-sm hover:shadow-[2px_2px_0_0_#000]',
    };

    const sizeStyles = {
      sm: 'px-4 py-2 text-sm',
      md: 'px-6 py-3 text-base',
      lg: 'px-8 py-4 text-lg',
    };

    return (
      <button
        ref={ref}
        className={cn(
          baseStyles,
          variantStyles[variant],
          sizeStyles[size],
          disabled && 'hover:translate-x-0 hover:translate-y-0',
          className
        )}
        disabled={disabled}
        {...props}
      >
        {children}
      </button>
    );
  }
);

BrutalButton.displayName = 'BrutalButton';
