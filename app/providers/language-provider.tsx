'use client';

import { createContext, useContext, useState, ReactNode } from 'react';
import { useRouter, usePathname } from 'next/navigation';

interface LanguageContextType {
  locale: string;
  setLocale: (locale: string) => void;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

interface LanguageProviderProps {
  children: ReactNode;
  initialLocale?: string;
}

export function LanguageProvider({ children, initialLocale = 'en' }: LanguageProviderProps) {
  const [locale, setLocaleState] = useState(initialLocale);
  const router = useRouter();
  const pathname = usePathname();
  
  // Switch the path to the new locale
  const setLocale = (newLocale: string) => {
    if (newLocale === locale) return;
    
    setLocaleState(newLocale);
    
    // Update the path
    let newPath = pathname || '/';
    
    // Remove current locale from path if it exists
    if (newPath.startsWith('/en')) {
      newPath = newPath.replace(/^\/en/, '');
    } else if (newPath.startsWith('/pt')) {
      newPath = newPath.replace(/^\/pt/, '');
    }
    
    // Ensure we have a slash at the beginning
    if (!newPath.startsWith('/')) {
      newPath = '/' + newPath;
    }
    
    // Add the new locale to the path
    if (newLocale !== 'en') {
      newPath = '/' + newLocale + newPath;
    }
    
    // Navigate to the new path
    router.push(newPath);
  };

  return (
    <LanguageContext.Provider value={{ locale, setLocale }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage(): LanguageContextType {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}
