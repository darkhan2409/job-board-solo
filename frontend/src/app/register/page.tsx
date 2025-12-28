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
    <div className="min-h-screen bg-background flex items-center justify-center px-4 py-12">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-secondary/10 border border-secondary/20 rounded-2xl mb-4">
            <UserPlus className="w-8 h-8 text-secondary" />
          </div>
          <h1 className="text-3xl font-bold text-white mb-2 font-heading">Join CareerOS</h1>
          <p className="text-gray-400 font-mono text-sm">$ create --new-account</p>
        </div>
        
        <Card className="card-dark border border-border/50">
          <CardHeader className="text-center pb-4">
            <CardTitle className="text-2xl text-white font-heading">Create Your Account</CardTitle>
            <CardDescription className="text-gray-400">
              Sign up to access thousands of job opportunities
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <RegisterForm />

            <OAuthButtons />

            <div className="mt-6 text-center text-sm text-gray-500 pt-4 border-t border-border/50">
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
