import Link from 'next/link'
import { fetchCompanies } from '@/lib/api';
import { Building2 } from 'lucide-react';
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
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center px-4 py-12">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-primary rounded-2xl mb-4 shadow-lg">
            <Building2 className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gradient mb-2">Welcome Back</h1>
          <p className="text-muted-foreground">Sign in to continue your career journey</p>
        </div>
        
        <Card className="shadow-xl border-0">
          <CardHeader className="text-center pb-4">
            <CardTitle className="text-2xl">Login to Your Account</CardTitle>
            <CardDescription>
              Enter your credentials to access your dashboard
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <LoginForm />

            <div className="text-right">
              <Link
                href="/forgot-password"
                className="text-sm text-primary hover:text-primary/80 font-medium transition-colors"
              >
                Forgot password?
              </Link>
            </div>

            <OAuthButtons />

            <div className="mt-6 text-center text-sm text-gray-600 pt-4 border-t">
              Don&apos;t have an account?{' '}
              <Link
                href="/register"
                className="text-primary hover:text-primary/80 font-semibold transition-colors"
              >
                Sign up for free
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
