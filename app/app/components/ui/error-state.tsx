import React from 'react';
import { cn } from '@lib/utils';
import { BrutalButton } from './brutal-button';

export interface ErrorStateProps extends React.HTMLAttributes<HTMLDivElement> {
  title?: string;
  message?: string;
  onRetry?: () => void;
  onGoBack?: () => void;
  showRetry?: boolean;
  showGoBack?: boolean;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  className,
  title = 'OOPS! SOMETHING WENT WRONG',
  message = "We couldn't load this content. Please try again.",
  onRetry,
  onGoBack,
  showRetry = true,
  showGoBack = false,
  ...props
}) => {
  return (
    <div
      className={cn(
        'flex flex-col items-center justify-center p-8 bg-red-100 border-4 border-[var(--brutal-red)] text-center',
        className
      )}
      role="alert"
      {...props}
    >
      <div className="text-6xl mb-4" aria-hidden="true">
        ⚠️
      </div>
      <h2 className="text-2xl font-bold uppercase mb-4 text-[var(--brutal-red)]">
        {title}
      </h2>
      <p className="text-base mb-6 max-w-md">
        {message}
      </p>
      <div className="flex gap-4 flex-wrap justify-center">
        {showRetry && onRetry && (
          <BrutalButton
            variant="danger"
            onClick={onRetry}
            aria-label="Try again"
          >
            TRY AGAIN
          </BrutalButton>
        )}
        {showGoBack && onGoBack && (
          <BrutalButton
            variant="outline"
            onClick={onGoBack}
            aria-label="Go back"
          >
            GO BACK
          </BrutalButton>
        )}
      </div>
    </div>
  );
};

ErrorState.displayName = 'ErrorState';
