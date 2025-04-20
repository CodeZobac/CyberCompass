// import {notFound} from 'next/navigation'; // Removed unused import
import {getRequestConfig} from 'next-intl/server';
import {AbstractIntlMessages} from 'next-intl'; // Import from 'next-intl'

// Define locales directly here
export const locales = ['en', 'pt'] as const;

// Define a type for the locales
type Locale = typeof locales[number];

export default getRequestConfig(async ({locale}) => {
  // Validate that the incoming `locale` parameter is valid
  const validatedLocale = locales.includes(locale as Locale) ? locale as Locale : 'en'; // Fallback to 'en' if invalid
  if (!locales.includes(locale as Locale)) {
    console.warn(`Invalid locale "${locale}" requested. Falling back to 'en'.`);
    // notFound(); // Or redirect, or just use fallback
  }

  let messages: AbstractIntlMessages;
  try {
    messages = (await import(`./messages/${validatedLocale}.json`)).default;
  } catch (error) {
    console.error(`Could not load messages for locale: ${validatedLocale}`, error);
    // Attempt to load default English messages as a last resort
    try {
      messages = (await import(`./messages/en.json`)).default;
    } catch (fallbackError) {
      console.error(`Could not load fallback messages for locale: en`, fallbackError);
      // If even fallback fails, return empty messages or throw
      messages = {}; // Or throw new Error('Failed to load any messages');
    }
  }

  return {
    locale: validatedLocale, // Return the validated locale
    messages
  };
});
