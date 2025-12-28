'use client'

import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'
import { Button } from '@/components/ui/button'
import { LogOut, Briefcase, Building2 } from 'lucide-react'

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
    <header className="border-b bg-white shadow-sm sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <nav className="flex items-center justify-between">
          <Link href="/" className="text-2xl font-bold text-gradient flex items-center gap-2">
            <Briefcase className="w-7 h-7 text-primary" />
            JobBoard
          </Link>

          <div className="flex items-center gap-8">
            <Link 
              href="/jobs" 
              className="font-medium hover:text-primary transition-colors flex items-center gap-2"
            >
              <Briefcase className="w-4 h-4" />
              Jobs
            </Link>
            <Link 
              href="/companies" 
              className="font-medium hover:text-primary transition-colors flex items-center gap-2"
            >
              <Building2 className="w-4 h-4" />
              Companies
            </Link>

            {isAuthenticated ? (
              <div className="flex items-center gap-4">
                <div className="px-3 py-1 bg-primary/10 rounded-full">
                  <span className="text-sm font-medium text-primary">
                    {user?.full_name}
                  </span>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleLogout}
                  className="flex items-center gap-2 hover:bg-destructive/10 hover:text-destructive hover:border-destructive"
                >
                  <LogOut className="w-4 h-4" />
                  Logout
                </Button>
              </div>
            ) : (
              <div className="flex items-center gap-3">
                <Link href="/login">
                  <Button variant="ghost" size="sm" className="font-medium">
                    Login
                  </Button>
                </Link>
                <Link href="/register">
                  <Button size="sm" className="btn-primary font-medium">
                    Sign Up
                  </Button>
                </Link>
              </div>
            )}
          </div>
        </nav>
      </div>
    </header>
  )
}
