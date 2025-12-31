import React from 'react';
import { cn } from '@lib/utils';

export interface BrutalCardProps extends React.HTMLAttributes<HTMLDivElement> {
  hover?: boolean;
  shadow?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export const BrutalCard = React.forwardRef<HTMLDivElement, BrutalCardProps>(
  ({ className, hover = false, shadow = 'md', children, ...props }, ref) => {
    const baseStyles = 'bg-white border-4 border-black';
    
    const shadowStyles = {
      sm: 'shadow-brutal-sm',
      md: 'shadow-brutal-md',
      lg: 'shadow-brutal-lg',
    };

    const hoverStyles = hover
      ? 'transition-all duration-200 hover:-translate-x-[2px] hover:-translate-y-[2px] hover:shadow-brutal-lg'
      : '';

    return (
      <div
        ref={ref}
        className={cn(
          baseStyles,
          shadowStyles[shadow],
          hoverStyles,
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);

BrutalCard.displayName = 'BrutalCard';
