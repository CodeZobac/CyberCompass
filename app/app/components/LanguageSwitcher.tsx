'use client';

import { usePathname, useRouter } from 'next/navigation';
import { useLocale } from 'next-intl';
import { Button } from './ui/button';

export default function LanguageSwitcher() {
  const locale = useLocale();
  const router = useRouter();
  const pathname = usePathname();

  const switchLocale = (newLocale: string) => {
    // Handle path switching logic
    if (locale === newLocale) return;
    
    let newPath = pathname || '/';
    
    // Rewrite path for the new locale
    if (pathname.startsWith(`/${locale}/`)) {
      newPath = pathname.replace(`/${locale}/`, `/${newLocale}/`);
    } else if (pathname.startsWith(`/${locale}`)) {
      newPath = pathname.replace(`/${locale}`, `/${newLocale}`);
    } else if (locale === 'en') {
      // If we're on default locale (en) and not prefixed
      newPath = `/${newLocale}${pathname}`;
    } else if (newLocale === 'en') {
      // If we're switching to default locale (en)
      newPath = pathname.replace(`/${locale}`, '');
    }
    
    router.push(newPath);
  };

  return (
    <div className="flex items-center gap-2 ml-4">
      <Button
        variant="ghost"
        size="sm"
        className={locale === 'en' ? 'bg-accent/20' : ''}
        onClick={() => switchLocale('en')}
      >
        EN
      </Button>
      <Button
        variant="ghost"
        size="sm"
        className={locale === 'pt' ? 'bg-accent/20' : ''}
        onClick={() => switchLocale('pt')}
      >
        PT
      </Button>
    </div>
  );
}
