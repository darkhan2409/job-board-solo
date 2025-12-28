'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { resetPassword } from '@/lib/api'
import { validatePassword } from '@/lib/validation'
import { Eye, EyeOff, CheckCircle } from 'lucide-react'

interface ResetPasswordFormProps {
  token: string
}

export default function ResetPasswordForm({ token }: ResetPasswordFormProps) {
  const router = useRouter()

  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isLoading, setIsLoading] = useState(false)
  const [apiError, setApiError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    const passwordError = validatePassword(password)
    if (passwordError) newErrors.password = passwordError

    if (password !== confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setApiError(null)

    if (!validateForm()) return

    setIsLoading(true)

    try {
      await resetPassword(token, password)
      setSuccess(true)
      // Redirect to login after 2 seconds
      setTimeout(() => {
        router.push('/login?message=password_reset_success')
      }, 2000)
    } catch (error) {
      setApiError(
        error instanceof Error
          ? error.message
          : 'Failed to reset password. The link may be invalid or expired.'
      )
    } finally {
      setIsLoading(false)
    }
  }

  const getPasswordStrength = (pwd: string): string => {
    if (pwd.length === 0) return ''
    if (pwd.length < 8) return 'Weak'

    let strength = 0
    if (/[a-z]/.test(pwd)) strength++
    if (/[A-Z]/.test(pwd)) strength++
    if (/[0-9]/.test(pwd)) strength++
    if (/[^a-zA-Z0-9]/.test(pwd)) strength++

    if (strength <= 2) return 'Weak'
    if (strength === 3) return 'Medium'
    return 'Strong'
  }

  const passwordStrength = getPasswordStrength(password)

  const getStrengthColor = (strength: string): string => {
    switch (strength) {
      case 'Weak':
        return 'text-red-600'
      case 'Medium':
        return 'text-yellow-600'
      case 'Strong':
        return 'text-green-600'
      default:
        return 'text-gray-600'
    }
  }

  if (success) {
    return (
      <div className="text-center space-y-4">
        <div className="flex justify-center">
          <CheckCircle className="w-16 h-16 text-green-500" />
        </div>
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Password Reset Successful!
          </h3>
          <p className="text-gray-600">
            Your password has been reset successfully. Redirecting to login...
          </p>
        </div>
      </div>
    )
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {apiError && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {apiError}
        </div>
      )}

      <div>
        <label
          htmlFor="password"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          New Password
        </label>
        <div className="relative">
          <Input
            id="password"
            type={showPassword ? 'text' : 'password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter new password"
            className={errors.password ? 'border-red-500' : ''}
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
          >
            {showPassword ? (
              <EyeOff className="w-4 h-4" />
            ) : (
              <Eye className="w-4 h-4" />
            )}
          </button>
        </div>
        {errors.password && (
          <p className="text-red-600 text-sm mt-1">{errors.password}</p>
        )}
        {password && !errors.password && (
          <p className={`text-sm mt-1 ${getStrengthColor(passwordStrength)}`}>
            Password strength: {passwordStrength}
          </p>
        )}
        <p className="text-xs text-gray-500 mt-1">
          Must be at least 8 characters with uppercase, lowercase, and number
        </p>
      </div>

      <div>
        <label
          htmlFor="confirmPassword"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Confirm New Password
        </label>
        <Input
          id="confirmPassword"
          type={showPassword ? 'text' : 'password'}
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="Confirm new password"
          className={errors.confirmPassword ? 'border-red-500' : ''}
        />
        {errors.confirmPassword && (
          <p className="text-red-600 text-sm mt-1">{errors.confirmPassword}</p>
        )}
      </div>

      <Button type="submit" className="w-full" disabled={isLoading}>
        {isLoading ? 'Resetting Password...' : 'Reset Password'}
      </Button>

      <div className="text-center">
        <Link href="/login" className="text-sm text-primary hover:underline">
          Back to Login
        </Link>
      </div>
    </form>
  )
}
