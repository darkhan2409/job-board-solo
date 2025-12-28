'use client'

import { useEffect } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { UserRole } from '@/lib/types'
import { Loader2 } from 'lucide-react'

interface ProtectedRouteProps {
  children: React.ReactNode
  fallback?: React.ReactNode
  requiredRoles?: UserRole[]
}

export default function ProtectedRoute({
  children,
  fallback,
  requiredRoles,
}: ProtectedRouteProps) {
  const router = useRouter()
  const pathname = usePathname()
  const { user, isAuthenticated, isLoading } = useAuth()

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      // Redirect to login with return URL
      const returnUrl = encodeURIComponent(pathname)
      router.push(`/login?returnUrl=${returnUrl}`)
    }
  }, [isLoading, isAuthenticated, pathname, router])

  // Show loading state while checking authentication
  if (isLoading) {
    if (fallback) {
      return <>{fallback}</>
    }

    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin mx-auto text-primary" />
          <p className="mt-4 text-sm text-gray-600">Loading...</p>
        </div>
      </div>
    )
  }

  // Not authenticated - will redirect via useEffect
  if (!isAuthenticated) {
    return null
  }

  // Check required roles if specified
  if (requiredRoles && requiredRoles.length > 0) {
    if (!user || !requiredRoles.includes(user.role)) {
      return (
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Access Denied
            </h2>
            <p className="text-gray-600">
              You don't have permission to access this page.
            </p>
          </div>
        </div>
      )
    }
  }

  // Authenticated and authorized - render children
  return <>{children}</>
}
