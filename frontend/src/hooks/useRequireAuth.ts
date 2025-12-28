import { useEffect } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { useAuth } from './useAuth'
import { User, UserRole } from '@/lib/types'

interface UseRequireAuthOptions {
  redirectTo?: string
  requiredRoles?: UserRole[]
}

/**
 * Hook that ensures user is authenticated before rendering component.
 * Alternative to ProtectedRoute component for more flexible usage.
 *
 * @param options - Configuration options
 * @param options.redirectTo - Custom redirect path (default: /login)
 * @param options.requiredRoles - Array of roles user must have
 * @returns User object if authenticated and authorized, null otherwise
 *
 * @example
 * function DashboardPage() {
 *   const user = useRequireAuth()
 *   if (!user) return null
 *   return <div>Welcome {user.full_name}</div>
 * }
 *
 * @example
 * function AdminPage() {
 *   const user = useRequireAuth({ requiredRoles: [UserRole.ADMIN] })
 *   if (!user) return null
 *   return <div>Admin Panel</div>
 * }
 */
export function useRequireAuth(
  options: UseRequireAuthOptions = {}
): User | null {
  const { redirectTo = '/login', requiredRoles } = options
  const router = useRouter()
  const pathname = usePathname()
  const { user, isAuthenticated, isLoading } = useAuth()

  useEffect(() => {
    if (!isLoading) {
      // Not authenticated - redirect to login
      if (!isAuthenticated) {
        const returnUrl = encodeURIComponent(pathname)
        router.push(`${redirectTo}?returnUrl=${returnUrl}`)
        return
      }

      // Check role requirements
      if (requiredRoles && requiredRoles.length > 0) {
        if (!user || !requiredRoles.includes(user.role)) {
          // Not authorized - redirect to homepage
          router.push('/')
        }
      }
    }
  }, [
    isLoading,
    isAuthenticated,
    user,
    requiredRoles,
    pathname,
    router,
    redirectTo,
  ])

  // Return user if authenticated and authorized
  if (isLoading || !isAuthenticated) {
    return null
  }

  if (requiredRoles && requiredRoles.length > 0) {
    if (!user || !requiredRoles.includes(user.role)) {
      return null
    }
  }

  return user
}
