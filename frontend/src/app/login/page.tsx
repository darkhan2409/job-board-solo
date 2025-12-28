import Link from 'next/link'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import LoginForm from '@/components/auth/LoginForm'
import OAuthButtons from '@/components/auth/OAuthButtons'

export default function LoginPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-md mx-auto">
        <Card>
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">Welcome Back</CardTitle>
            <CardDescription>
              Login to your account to continue
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <LoginForm />

            <div className="text-right">
              <Link
                href="/forgot-password"
                className="text-sm text-primary hover:underline"
              >
                Forgot password?
              </Link>
            </div>

            <OAuthButtons />

            <div className="mt-6 text-center text-sm text-gray-600">
              Don&apos;t have an account?{' '}
              <Link
                href="/register"
                className="text-primary hover:underline font-semibold"
              >
                Sign up
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
