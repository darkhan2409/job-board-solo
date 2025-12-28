import Link from 'next/link'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import ResetPasswordForm from '@/components/auth/ResetPasswordForm'
import { XCircle } from 'lucide-react'

interface ResetPasswordPageProps {
  searchParams: {
    token?: string
  }
}

export default function ResetPasswordPage({
  searchParams,
}: ResetPasswordPageProps) {
  // Check if token is present
  if (!searchParams.token) {
    return (
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-md mx-auto">
          <Card>
            <CardContent className="pt-6">
              <div className="text-center space-y-4">
                <div className="flex justify-center">
                  <XCircle className="w-16 h-16 text-red-500" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Invalid Reset Link
                  </h3>
                  <p className="text-gray-600 mb-4">
                    This password reset link is invalid or incomplete. Please
                    request a new password reset link.
                  </p>
                </div>
                <div className="space-y-2">
                  <Link href="/forgot-password">
                    <Button className="w-full">Request New Link</Button>
                  </Link>
                  <Link href="/login">
                    <Button variant="outline" className="w-full">
                      Back to Login
                    </Button>
                  </Link>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-md mx-auto">
        <Card>
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">Reset Your Password</CardTitle>
            <CardDescription>
              Enter your new password below
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResetPasswordForm token={searchParams.token} />
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
