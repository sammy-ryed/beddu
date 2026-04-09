import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Link from 'next/link'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'beedu - Mental Health Companion',
  description: 'Your mental health and financial stress support companion for India',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-neutral-50">
          {/* Simple header - no AI vibes */}
          <header className="border-b border-neutral-200 bg-white">
            <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
              <Link href="/" className="flex items-center gap-2 text-neutral-900 hover:text-neutral-600 transition-colors">
                <span className="text-xl font-medium">beedu</span>
              </Link>
              <nav className="flex items-center gap-6 text-sm">
                <Link href="/" className="text-neutral-600 hover:text-neutral-900 transition-colors">
                  Chat
                </Link>
                <Link href="/history" className="text-neutral-600 hover:text-neutral-900 transition-colors">
                  History
                </Link>
                <Link href="/stats" className="text-neutral-600 hover:text-neutral-900 transition-colors">
                  Progress
                </Link>
              </nav>
            </div>
          </header>
          
          {/* Content */}
          <main>{children}</main>
          
          {/* Subtle footer */}
          <footer className="border-t border-neutral-200 mt-12">
            <div className="max-w-5xl mx-auto px-4 py-6 text-xs text-neutral-500 text-center">
              Not a replacement for professional help. Crisis: KIRAN 1800-599-0019
            </div>
          </footer>
        </div>
      </body>
    </html>
  )
}
