'use client';

import { NextIntlClientProvider, AbstractIntlMessages } from 'next-intl'; // Import AbstractIntlMessages
import { ReactNode } from 'react';

type Props = {
  locale: string;
  children: ReactNode;
  messages: AbstractIntlMessages; // Use AbstractIntlMessages type
};

export function IntlClientProvider({ locale, messages, children }: Props) {
  return (
    <NextIntlClientProvider locale={locale} messages={messages}>
      {children}
    </NextIntlClientProvider>
  );
}
