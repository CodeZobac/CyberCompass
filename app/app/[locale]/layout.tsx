import { NextIntlClientProvider, AbstractIntlMessages } from 'next-intl';
import React from 'react';

// Import locales from the central i18n configuration
import { locales } from '../../i18n';

// Import your components and styles
import '../globals.css';
import { Providers } from '../providers/providers';

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

// Adjust props type to handle params as a Promise (Next.js 15 requirement)
export default async function LocaleLayout({
    children,
    params // In Next.js 15, params is a Promise
}: {
    children: React.ReactNode;
    params: Promise<{ locale: string }>; // Updated to reflect Promise type
}) {
    // Await the params to get locale
    const { locale } = await params;

    // Validate locale
    const isValidLocale = locales.includes(locale as typeof locales[number]);
    const targetLocale = isValidLocale ? locale : 'en'; // Use 'en' if locale is invalid

    // Load messages using the helper function
    const messages = await getMessages(targetLocale);

    return (
        <NextIntlClientProvider locale={targetLocale} messages={messages}>
            <Providers>{children}</Providers>
        </NextIntlClientProvider>
    );
}


