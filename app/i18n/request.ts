// filepath: /home/caboz/dev/CyberCompass/app/i18n/request.ts
import {getRequestConfig} from 'next-intl/server';
import {locales} from '../navigation';
import {AbstractIntlMessages} from 'next-intl';

// Define a type for the locales
type Locale = typeof locales[number];

export default getRequestConfig(async ({locale}) => {
  // Validate that the incoming `locale` parameter is valid
  const validatedLocale = locales.includes(locale as Locale) ? locale as Locale : 'en'; // Fallback to 'en' if invalid
  if (!locales.includes(locale as Locale)) {
    console.warn(`Invalid locale "${locale}" requested in request.ts. Falling back to 'en'.`);
  }

  let messages: AbstractIntlMessages;
  try {
    messages = (await import(`../messages/${validatedLocale}.json`)).default;
  } catch (error) {
    console.error(`Could not load messages for locale: ${validatedLocale} in request.ts`, error);
    // Attempt to load default English messages as a last resort
    try {
      messages = (await import(`../messages/en.json`)).default;
    } catch (fallbackError) {
      console.error(`Could not load fallback messages for locale: en in request.ts`, fallbackError);
      messages = {}; // Return empty messages if fallback fails
    }
  }

  return {
    locale: validatedLocale,
    messages
  };
});
