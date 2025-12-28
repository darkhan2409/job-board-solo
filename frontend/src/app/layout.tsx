import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import ChatWidget from '@/components/ChatWidget'
import { AuthProvider } from '@/contexts/AuthContext'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

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

            <Footer />
          </div>

          {/* AI Chat Widget */}
          <ChatWidget />
        </AuthProvider>
      </body>
    </html>
  )
}
