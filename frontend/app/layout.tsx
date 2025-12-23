import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Providers from '@/components/providers';
import Navbar from '@/components/navbar';
import { Toaster } from '@/components/ui/toaster';
import { KeyboardShortcutsProvider } from '@/components/keyboard-shortcuts-provider';
import { MobileProvider } from '@/components/mobile/MobileProvider';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A full-stack todo application',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          <KeyboardShortcutsProvider>
            <div className="min-h-screen flex flex-col overflow-x-hidden">
              <Navbar />
              <div className="flex-1 overflow-x-hidden">
                {children}
              </div>
            </div>
            <MobileProvider />
            <Toaster />
          </KeyboardShortcutsProvider>
        </Providers>
      </body>
    </html>
  );
}