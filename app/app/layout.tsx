import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from "./providers/providers";
import { GlobalSyncStatus } from "./components/GlobalSyncStatus";
import { KeyboardNavigationDetector } from "./components/ui/keyboard-navigation-detector";
import { GlobalKeyboardShortcuts, KeyboardShortcutsHelp } from "./components/ui/keyboard-shortcuts";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: 'swap',
});

export const metadata: Metadata = {
  title: "CyberCompass",
  description: "Your AI-powered cyber ethics mentor",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <meta name="color-scheme" content="light only" />
      </head>
      <body
        className={`${inter.variable} antialiased font-sans`}
      >
        <Providers >
          <KeyboardNavigationDetector />
          <GlobalKeyboardShortcuts />
          {children}
          <GlobalSyncStatus />
          <KeyboardShortcutsHelp />
        </Providers>
      </body>
    </html>
  );
}
