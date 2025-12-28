import Link from 'next/link'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import RegisterForm from '@/components/auth/RegisterForm'
import OAuthButtons from '@/components/auth/OAuthButtons'

export default function RegisterPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-md mx-auto">
        <Card>
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">Create Account</CardTitle>
            <CardDescription>
              Join JobBoard to find your next opportunity
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <RegisterForm />

            <OAuthButtons />

            <div className="mt-6 text-center text-sm text-gray-600">
              Already have an account?{' '}
              <Link
                href="/login"
                className="text-primary hover:underline font-semibold"
              >
                Login
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
