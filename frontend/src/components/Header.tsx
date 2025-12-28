'use client'

import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'
import { Button } from '@/components/ui/button'
import { LogOut, Briefcase, Building2, Terminal, Bookmark } from 'lucide-react'

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
    <header className="border-b border-muted bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <nav className="flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 group">
            <div className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center group-hover:bg-primary/20 transition-colors">
              <Terminal className="w-5 h-5 text-primary" />
            </div>
            <span className="text-xl font-bold">
              <span className="text-gradient">Career</span>
              <span className="text-muted-foreground">OS</span>
            </span>
          </Link>

          <div className="flex items-center gap-8">
            <Link 
              href="/jobs" 
              className="font-medium text-muted-foreground hover:text-foreground transition-colors flex items-center gap-2"
            >
              <Briefcase className="w-4 h-4" />
              Roles
            </Link>
            <Link 
              href="/companies" 
              className="font-medium text-muted-foreground hover:text-foreground transition-colors flex items-center gap-2"
            >
              <Building2 className="w-4 h-4" />
              Companies
            </Link>
            {isAuthenticated && (
              <Link 
                href="/saved" 
                className="font-medium text-muted-foreground hover:text-foreground transition-colors flex items-center gap-2"
              >
                <Bookmark className="w-4 h-4" />
                Saved
              </Link>
            )}

            {isAuthenticated ? (
              <div className="flex items-center gap-4">
                <div className="px-3 py-1.5 bg-card border border-muted rounded-lg">
                  <span className="text-sm font-medium">
                    {user?.full_name}
                  </span>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleLogout}
                  className="flex items-center gap-2 border-muted hover:border-destructive hover:text-destructive"
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
