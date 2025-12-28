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
import { UserPlus } from 'lucide-react'

export default function RegisterPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center px-4 py-12">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-primary rounded-2xl mb-4 shadow-lg">
            <UserPlus className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gradient mb-2">Join JobBoard</h1>
          <p className="text-muted-foreground">Start your journey to your dream career</p>
        </div>
        
        <Card className="shadow-xl border-0">
          <CardHeader className="text-center pb-4">
            <CardTitle className="text-2xl">Create Your Account</CardTitle>
            <CardDescription>
              Sign up to access thousands of job opportunities
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <RegisterForm />

            <OAuthButtons />

            <div className="mt-6 text-center text-sm text-gray-600 pt-4 border-t">
              Already have an account?{' '}
              <Link
                href="/login"
                className="text-primary hover:text-primary/80 font-semibold transition-colors"
              >
                Login here
              </Link>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
