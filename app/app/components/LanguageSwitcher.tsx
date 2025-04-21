'use client';

import * as React from 'react';
import { usePathname, useRouter } from 'next/navigation';
import { useLocale } from 'next-intl';
import { Button } from './ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from './ui/retrodropdown';

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
    } else if (pathname === `/${locale}`) { // Handle root path for the locale
        newPath = `/${newLocale}`;
    } else if (locale === 'en' && pathname === '/') { // Handle switching from root default locale
        newPath = `/${newLocale}`;
    } else if (locale === 'en') {
      // If we're on default locale (en) and not prefixed root
      newPath = `/${newLocale}${pathname}`;
    } else if (newLocale === 'en' && pathname === `/${locale}`) { // Handle switching to root default locale
        newPath = '/';
    } else if (newLocale === 'en') {
      // If we're switching to default locale (en)
      newPath = pathname.replace(`/${locale}`, '');
    } else {
        // Fallback or other cases if necessary - ensure leading slash
        const basePath = pathname.startsWith('/') ? pathname : `/${pathname}`;
        // Ensure we don't double-prefix if the basePath already includes the old locale
        const pathWithoutOldLocale = basePath.startsWith(`/${locale}`) ? basePath.substring(locale.length + 1) : basePath;
        newPath = `/${newLocale}${pathWithoutOldLocale}`;
    }


    router.push(newPath);
  };

  return (
    <div className="ml-4"> {/* Removed flex and gap as it's now a single element */}
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          {/* Using ghost variant and sm size */}
          <Button size="sm">
            {locale.toUpperCase()}
          </Button>
        </DropdownMenuTrigger>
        {/* Added bg-background for opacity */}
        <DropdownMenuContent className="w-20 bg-background"> 
          <DropdownMenuLabel>Select your language</DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuRadioGroup value={locale} onValueChange={switchLocale}>
            <DropdownMenuRadioItem value="en">EN</DropdownMenuRadioItem>
            <DropdownMenuSeparator />
            <DropdownMenuRadioItem value="pt">PT</DropdownMenuRadioItem>
          </DropdownMenuRadioGroup>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
}
