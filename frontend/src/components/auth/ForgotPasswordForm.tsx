'use client'

import { useState } from 'react'
import Link from 'next/link'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { requestPasswordReset } from '@/lib/api'
import { validateEmail } from '@/lib/validation'
import { CheckCircle } from 'lucide-react'

export default function ForgotPasswordForm() {
  const [email, setEmail] = useState('')
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [isLoading, setIsLoading] = useState(false)
  const [apiError, setApiError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {}

    const emailError = validateEmail(email)
    if (emailError) newErrors.email = emailError

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setApiError(null)

    if (!validateForm()) return

    setIsLoading(true)

    try {
      await requestPasswordReset(email)
      setSuccess(true)
    } catch (error) {
      setApiError(error instanceof Error ? error.message : 'Failed to send reset email')
    } finally {
      setIsLoading(false)
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
            Check your email
          </h3>
          <p className="text-gray-600 mb-4">
            If an account exists with the email <strong>{email}</strong>, you
            will receive a password reset link shortly.
          </p>
          <p className="text-sm text-gray-500">
            Didn't receive the email? Check your spam folder or try again.
          </p>
        </div>
        <div className="space-y-2">
          <Button
            onClick={() => setSuccess(false)}
            variant="outline"
            className="w-full"
          >
            Try another email
          </Button>
          <Link href="/login">
            <Button variant="outline" className="w-full">
              Back to Login
            </Button>
          </Link>
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
          htmlFor="email"
          className="block text-sm font-medium text-gray-700 mb-2"
        >
          Email
        </label>
        <Input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="you@example.com"
          className={errors.email ? 'border-red-500' : ''}
        />
        {errors.email && (
          <p className="text-red-600 text-sm mt-1">{errors.email}</p>
        )}
      </div>

      <Button type="submit" className="w-full" disabled={isLoading}>
        {isLoading ? 'Sending...' : 'Send Reset Link'}
      </Button>

      <div className="text-center">
        <Link
          href="/login"
          className="text-sm text-primary hover:underline"
        >
          Back to Login
        </Link>
      </div>
    </form>
  )
}
