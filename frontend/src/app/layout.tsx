import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import ChatWidget from '@/components/ChatWidget'
import { AuthProvider } from '@/contexts/AuthContext'
import Header from '@/components/Header'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Job Board - Find Your Dream Tech Job',
  description: 'Browse and apply to the latest tech jobs from top companies',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider>
          <div className="min-h-screen flex flex-col">
            <Header />

            <main className="flex-1">{children}</main>

            <footer className="border-t mt-auto">
              <div className="container mx-auto px-4 py-6 text-center text-sm text-muted-foreground">
                <p>© 2024 JobBoard. Built with Next.js, FastAPI, and AI.</p>
              </div>
            </footer>
          </div>

          {/* AI Chat Widget */}
          <ChatWidget />
        </AuthProvider>
      </body>
    </html>
  )
}
