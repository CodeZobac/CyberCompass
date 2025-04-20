import createMiddleware from 'next-intl/middleware';
 
export default createMiddleware({
  // A list of all locales that are supported
  locales: ['en', 'pt'],
  
  // Used when no locale matches
  defaultLocale: 'en',
  
  // This is the default path
  localePrefix: 'as-needed'
});
 
export const config = {
  // Match all pathnames except for
  // - api routes
  // - static files
  // - _next paths (Next.js internals)
  matcher: ['/((?!api|_next|.*\\..*).*)']
};
