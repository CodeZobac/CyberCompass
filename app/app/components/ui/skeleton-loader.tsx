import React from 'react';
import { cn } from '@lib/utils';

export interface SkeletonLoaderProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'text' | 'card' | 'circle' | 'button';
  width?: string;
  height?: string;
}

export const SkeletonLoader: React.FC<SkeletonLoaderProps> = ({
  className,
  variant = 'text',
  width,
  height,
  ...props
}) => {
  const baseStyles = 'animate-shimmer border-4 border-black';

  const variantStyles = {
    text: 'h-4 w-full',
    card: 'h-48 w-full',
    circle: 'h-12 w-12 rounded-full',
    button: 'h-12 w-32',
  };

  const style: React.CSSProperties = {};
  if (width) style.width = width;
  if (height) style.height = height;

  return (
    <div
      className={cn(
        baseStyles,
        variantStyles[variant],
        className
      )}
      style={style}
      role="status"
      aria-label="Loading content"
      {...props}
    />
  );
};

SkeletonLoader.displayName = 'SkeletonLoader';

export interface SkeletonGroupProps {
  count?: number;
  variant?: SkeletonLoaderProps['variant'];
  className?: string;
}

export const SkeletonGroup: React.FC<SkeletonGroupProps> = ({
  count = 3,
  variant = 'text',
  className,
}) => {
  return (
    <div className={cn('space-y-4', className)}>
      {Array.from({ length: count }).map((_, index) => (
        <SkeletonLoader key={index} variant={variant} />
      ))}
    </div>
  );
};

SkeletonGroup.displayName = 'SkeletonGroup';
