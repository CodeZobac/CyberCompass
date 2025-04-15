'use client'

import { ThemeProvider } from './theme-provider'
import { useRouter } from 'next/navigation'
import { RouterProvider } from 'react-aria-components'
import { SessionProvider } from 'next-auth/react'

declare module 'react-aria-components' {
  interface RouterConfig {
    routerOptions: NonNullable<Parameters<ReturnType<typeof useRouter>['push']>[1]>
  }
}

export function Providers({ children }: { children: React.ReactNode }) {
  const router = useRouter()

  return (
    <SessionProvider>
      <RouterProvider navigate={router.push}>
        <ThemeProvider enableSystem attribute="class">{children}</ThemeProvider>
      </RouterProvider>
    </SessionProvider>
  )
}
