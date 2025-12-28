'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useAuth } from '@/hooks/useAuth'
import {
  validateEmail,
  validatePassword,
  validateFullName,
} from '@/lib/validation'
import { Eye, EyeOff } from 'lucide-react'

export default function RegisterForm() {
  const router = useRouter()
  const { register } = useAuth()

  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    full_name: '',
  })
  const [showPassword, setShowPassword] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isLoading, setIsLoading] = useState(false)
  const [apiError, setApiError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    const emailError = validateEmail(formData.email)
    if (emailError) newErrors.email = emailError

    const passwordError = validatePassword(formData.password)
    if (passwordError) newErrors.password = passwordError

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match'
    }

    const nameError = validateFullName(formData.full_name)
    if (nameError) newErrors.full_name = nameError

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setApiError(null)

    if (!validateForm()) return

    setIsLoading(true)

    try {
      await register({
        email: formData.email,
        password: formData.password,
        full_name: formData.full_name,
      })
      setSuccess(true)
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Registration failed')
    } finally {
      setIsLoading(false)
    }
  }

  if (success) {
    return (
      <div className="text-center space-y-4">
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
          <p className="font-semibold">Registration successful!</p>
          <p className="text-sm mt-1">
            Please check your email to verify your account before logging in.
          </p>
        </div>
        <Button onClick={() => router.push('/login')} className="w-full">
          Go to Login
        </Button>
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
          htmlFor="full_name"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Full Name
        </label>
        <Input
          id="full_name"
          type="text"
          value={formData.full_name}
          onChange={(e) =>
            setFormData({ ...formData, full_name: e.target.value })
          }
          placeholder="John Doe"
          className={errors.full_name ? 'border-red-500' : ''}
        />
        {errors.full_name && (
          <p className="text-red-600 text-sm mt-1">{errors.full_name}</p>
        )}
      </div>

      <div>
        <label
          htmlFor="email"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Email
        </label>
        <Input
          id="email"
          type="email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          placeholder="you@example.com"
          className={errors.email ? 'border-red-500' : ''}
        />
        {errors.email && (
          <p className="text-red-600 text-sm mt-1">{errors.email}</p>
        )}
      </div>

      <div>
        <label
          htmlFor="password"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Password
        </label>
        <div className="relative">
          <Input
            id="password"
            type={showPassword ? 'text' : 'password'}
            value={formData.password}
            onChange={(e) =>
              setFormData({ ...formData, password: e.target.value })
            }
            placeholder="Min. 8 characters"
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
        <p className="text-xs text-gray-500 mt-1">
          Must contain uppercase, lowercase, and digit
        </p>
      </div>

      <div>
        <label
          htmlFor="confirmPassword"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Confirm Password
        </label>
        <Input
          id="confirmPassword"
          type={showPassword ? 'text' : 'password'}
          value={formData.confirmPassword}
          onChange={(e) =>
            setFormData({ ...formData, confirmPassword: e.target.value })
          }
          placeholder="Re-enter password"
          className={errors.confirmPassword ? 'border-red-500' : ''}
        />
        {errors.confirmPassword && (
          <p className="text-red-600 text-sm mt-1">{errors.confirmPassword}</p>
        )}
      </div>

      <Button type="submit" className="w-full" disabled={isLoading}>
        {isLoading ? 'Creating account...' : 'Create Account'}
      </Button>
    </form>
  )
}
