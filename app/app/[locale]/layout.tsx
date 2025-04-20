import { NextIntlClientProvider, AbstractIntlMessages } from 'next-intl'; // Import AbstractIntlMessages
import React from 'react';

// Define supported locales directly in this file
export const locales = ['en', 'pt'] as const;

// Import your components and styles
import '../globals.css';
import { Providers } from '../providers/providers';

type Props = {
  children: React.ReactNode;
  params: { locale: string };
};

export function generateStaticParams() {
  return locales.map((locale) => ({ locale }));
}

// Function to safely load messages with fallback
async function getMessages(locale: string): Promise<AbstractIntlMessages> {
  try {
    return (await import(`../../messages/${locale}.json`)).default;
  } catch (error: unknown) { // Specify type for error
    console.warn(`Could not load messages for locale: ${locale}. Falling back to 'en'. Error: ${error instanceof Error ? error.message : String(error)}`);
    // Fallback to English messages if the requested locale is not found
    return (await import(`../../messages/en.json`)).default;
  }
}

export default async function LocaleLayout({ children, params: { locale } }: Props) {
  // Validate locale?
  const isValidLocale = locales.includes(locale as typeof locales[number]);
  const targetLocale = isValidLocale ? locale : 'en'; // Use 'en' if locale is invalid

  // Load messages using the helper function
  const messages = await getMessages(targetLocale);

  return (
    <html lang={targetLocale}>
      <body>
        <NextIntlClientProvider locale={targetLocale} messages={messages}>
          <Providers>{children}</Providers>
        </NextIntlClientProvider>
      </body>
    </html>
  );
}


