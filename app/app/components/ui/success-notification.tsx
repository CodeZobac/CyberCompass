import React, { useEffect, useState } from 'react';
import { cn } from '@lib/utils';

export interface SuccessNotificationProps {
  message: string;
  duration?: number;
  onClose?: () => void;
  show?: boolean;
}

export const SuccessNotification: React.FC<SuccessNotificationProps> = ({
  message,
  duration = 3000,
  onClose,
  show = true,
}) => {
  const [isVisible, setIsVisible] = useState(show);
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    if (show) {
      setIsVisible(true);
      setIsAnimating(true);

      const timer = setTimeout(() => {
        setIsAnimating(false);
        setTimeout(() => {
          setIsVisible(false);
          onClose?.();
        }, 300);
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [show, duration, onClose]);

  if (!isVisible) return null;

  return (
    <div
      className={cn(
        'fixed top-4 right-4 z-50 transition-all duration-300',
        isAnimating ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'
      )}
      role="alert"
      aria-live="polite"
    >
      <div className="bg-[var(--brutal-green)] text-white font-bold border-4 border-black px-6 py-4 shadow-brutal-md flex items-center gap-3 min-w-[300px]">
        <span className="text-2xl" aria-hidden="true">✓</span>
        <div>
          <p className="text-sm uppercase">SUCCESS!</p>
          <p className="text-base">{message}</p>
        </div>
      </div>
    </div>
  );
};

SuccessNotification.displayName = 'SuccessNotification';

export const useSuccessNotification = () => {
  const [notification, setNotification] = useState<{
    show: boolean;
    message: string;
  }>({
    show: false,
    message: '',
  });

  const showSuccess = (message: string) => {
    setNotification({ show: true, message });
  };

  const hideSuccess = () => {
    setNotification({ show: false, message: '' });
  };

  return {
    notification,
    showSuccess,
    hideSuccess,
  };
};
