import React from 'react';
import { cn } from '@lib/utils';

export interface LoadingSpinnerProps extends React.HTMLAttributes<HTMLDivElement> {
  size?: 'sm' | 'md' | 'lg';
  text?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  className,
  size = 'md',
  text = 'LOADING...',
  ...props
}) => {
  const sizeStyles = {
    sm: 'w-8 h-8 border-2',
    md: 'w-12 h-12 border-4',
    lg: 'w-16 h-16 border-4',
  };

  const textSizeStyles = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
  };

  return (
    <div
      className={cn('flex flex-col items-center justify-center gap-4', className)}
      {...props}
    >
      <div
        className={cn(
          'rounded-full border-black border-t-transparent animate-spin',
          sizeStyles[size]
        )}
        role="status"
        aria-label="Loading"
      />
      {text && (
        <p className={cn('font-bold uppercase', textSizeStyles[size])}>
          {text}
        </p>
      )}
    </div>
  );
};

LoadingSpinner.displayName = 'LoadingSpinner';
