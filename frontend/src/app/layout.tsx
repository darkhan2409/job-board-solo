import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

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
        <div className="min-h-screen flex flex-col">
          <header className="border-b">
            <div className="container mx-auto px-4 py-4">
              <nav className="flex items-center justify-between">
                <a href="/" className="text-2xl font-bold text-primary">
                  JobBoard
                </a>
                <div className="flex gap-6">
                  <a href="/jobs" className="hover:text-primary transition-colors">
                    Jobs
                  </a>
                  <a href="/companies" className="hover:text-primary transition-colors">
                    Companies
                  </a>
                </div>
              </nav>
            </div>
          </header>
          
          <main className="flex-1">
            {children}
          </main>
          
          <footer className="border-t mt-auto">
            <div className="container mx-auto px-4 py-6 text-center text-sm text-muted-foreground">
              <p>© 2024 JobBoard. Built with Next.js, FastAPI, and AI.</p>
            </div>
          </footer>
        </div>
      </body>
    </html>
  )
}
