'use client'

import { useEffect, useState } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { handleOAuthCallback } from '@/lib/api'
import { setTokens, saveUser } from '@/lib/auth'
import { CheckCircle, XCircle, Loader2 } from 'lucide-react'

export default function OAuthCallbackPage() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>(
    'loading'
  )
  const [message, setMessage] = useState('')

  useEffect(() => {
    const code = searchParams.get('code')
    const state = searchParams.get('state')
    const provider = searchParams.get('provider') as 'google' | 'github' | null

    if (!code || !state || !provider) {
      setStatus('error')
      setMessage('Missing required parameters')
      return
    }

    const processCallback = async () => {
      try {
        const response = await handleOAuthCallback(provider, code, state)

        // Save tokens and user
        setTokens(response.access_token, response.refresh_token)
        saveUser(response.user)

        setStatus('success')
        setMessage('Successfully logged in!')

        // Redirect after short delay
        setTimeout(() => {
          router.push('/jobs')
        }, 1500)
      } catch (error) {
        setStatus('error')
        setMessage(
          error instanceof Error ? error.message : 'OAuth callback failed'
        )
      }
    }

    processCallback()
  }, [searchParams, router])

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-md mx-auto">
        <Card>
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">OAuth Callback</CardTitle>
          </CardHeader>
          <CardContent className="text-center space-y-4">
            {status === 'loading' && (
              <>
                <Loader2 className="w-16 h-16 mx-auto text-primary animate-spin" />
                <p className="text-gray-600">Processing authentication...</p>
              </>
            )}

            {status === 'success' && (
              <>
                <CheckCircle className="w-16 h-16 mx-auto text-green-600" />
                <p className="text-gray-600">{message}</p>
                <p className="text-sm text-gray-500">Redirecting...</p>
              </>
            )}

            {status === 'error' && (
              <>
                <XCircle className="w-16 h-16 mx-auto text-red-600" />
                <p className="text-gray-600">{message}</p>
                <Button
                  onClick={() => router.push('/login')}
                  variant="outline"
                  className="w-full"
                >
                  Back to Login
                </Button>
              </>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
