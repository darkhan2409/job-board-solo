'use client'

import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'
import { Button } from '@/components/ui/button'
import { LogOut } from 'lucide-react'

export default function Header() {
  const { user, isAuthenticated, logout } = useAuth()

  const handleLogout = async () => {
    try {
      await logout()
    } catch (error) {
      console.error('Logout failed:', error)
    }
  }

  return (
    <header className="border-b">
      <div className="container mx-auto px-4 py-4">
        <nav className="flex items-center justify-between">
          <Link href="/" className="text-2xl font-bold text-primary">
            JobBoard
          </Link>

          <div className="flex items-center gap-6">
            <Link href="/jobs" className="hover:text-primary transition-colors">
              Jobs
            </Link>
            <Link href="/companies" className="hover:text-primary transition-colors">
              Companies
            </Link>

            {isAuthenticated ? (
              <div className="flex items-center gap-4">
                <span className="text-sm text-muted-foreground">
                  {user?.full_name}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleLogout}
                  className="flex items-center gap-2"
                >
                  <LogOut className="w-4 h-4" />
                  Logout
                </Button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link href="/login">
                  <Button variant="ghost" size="sm">
                    Login
                  </Button>
                </Link>
                <Link href="/register">
                  <Button size="sm">Sign Up</Button>
                </Link>
              </div>
            )}
          </div>
        </nav>
      </div>
    </header>
  )
}
