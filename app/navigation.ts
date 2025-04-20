// Temporarily simplified to allow build. Language switching needs reimplementation.

export const locales = ['en', 'pt'] as const;
export const localePrefix = 'as-needed';

// NOTE: next-intl navigation helpers (Link, redirect, usePathname, useRouter)
// were removed due to build errors with next-intl v4.0.2.
// Language switching logic needs to be implemented manually using next/navigation.

// Force the file to be treated as a module
export {};
