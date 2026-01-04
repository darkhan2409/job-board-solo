// Centralized API client with automatic auth headers and token refresh

import {
  getAccessToken,
  getRefreshToken,
  setTokens,
  clearTokens,
} from './auth'
import { refreshAccessToken } from './api'

interface ApiClientOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
  body?: any
  headers?: Record<string, string>
  requireAuth?: boolean
  skipRefresh?: boolean
}

/**
 * Centralized API client with automatic authentication and token refresh
 */
class ApiClient {
  private baseUrl: string
  private isRefreshing: boolean = false
  private refreshPromise: Promise<string | null> | null = null

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  /**
   * Make an HTTP request with automatic auth headers and token refresh
   *
   * @param endpoint - API endpoint path (e.g., '/api/jobs')
   * @param options - Request options
   * @returns Parsed JSON response
   * @throws Error if request fails
   */
  async request<T>(
    endpoint: string,
    options: ApiClientOptions = {}
  ): Promise<T> {
    const {
      method = 'GET',
      body,
      headers = {},
      requireAuth = false,
      skipRefresh = false,
    } = options

    // Build request headers
    const requestHeaders: Record<string, string> = {
      'Content-Type': 'application/json',
      ...headers,
    }

    // Add authorization header if token exists
    const token = getAccessToken()
    if (token) {
      requestHeaders['Authorization'] = `Bearer ${token}`
    } else if (requireAuth) {
      // Required auth but no token - redirect to login
      if (typeof window !== 'undefined') {
        window.location.href = '/login'
      }
      throw new Error('Authentication required')
    }

    // Make the request
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method,
        headers: requestHeaders,
        body: body ? JSON.stringify(body) : undefined,
        credentials: 'include', // Include cookies and auth headers for CORS
        cache: method === 'GET' ? 'no-store' : undefined,
      })

      // Handle 401 Unauthorized - try to refresh token
      if (response.status === 401 && !skipRefresh) {
        const newToken = await this.handleTokenRefresh()

        if (newToken) {
          // Retry the original request with new token
          return this.request<T>(endpoint, {
            ...options,
            skipRefresh: true, // Prevent infinite loop
          })
        } else {
          // Refresh failed - clear tokens and redirect
          clearTokens()
          if (typeof window !== 'undefined') {
            window.location.href = '/login'
          }
          throw new Error('Session expired')
        }
      }

      // Handle other errors
      if (!response.ok) {
        const error = await response.json().catch(() => ({
          detail: `Request failed with status ${response.status}`,
        }))
        throw new Error(error.detail || `HTTP ${response.status}`)
      }

      // Handle 204 No Content
      if (response.status === 204) {
        return undefined as T
      }

      // Parse and return JSON
      return response.json()
    } catch (error) {
      // Re-throw if it's already our error
      if (error instanceof Error) {
        throw error
      }
      // Network or other error
      throw new Error('Network request failed')
    }
  }

  /**
   * Handle token refresh with concurrent request protection
   *
   * @returns New access token or null if refresh failed
   */
  private async handleTokenRefresh(): Promise<string | null> {
    // If already refreshing, wait for existing refresh to complete
    if (this.isRefreshing && this.refreshPromise) {
      return this.refreshPromise
    }

    const refreshToken = getRefreshToken()
    if (!refreshToken) {
      return null
    }

    // Mark as refreshing and create promise
    this.isRefreshing = true
    this.refreshPromise = (async () => {
      try {
        const response = await refreshAccessToken(refreshToken)
        setTokens(response.access_token, response.refresh_token)
        return response.access_token
      } catch (error) {
        console.error('Token refresh failed:', error)
        return null
      } finally {
        this.isRefreshing = false
        this.refreshPromise = null
      }
    })()

    return this.refreshPromise
  }

  /**
   * Convenience method for GET requests
   */
  async get<T>(endpoint: string, options?: Omit<ApiClientOptions, 'method'>): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'GET' })
  }

  /**
   * Convenience method for POST requests
   */
  async post<T>(
    endpoint: string,
    body?: any,
    options?: Omit<ApiClientOptions, 'method' | 'body'>
  ): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'POST', body })
  }

  /**
   * Convenience method for PUT requests
   */
  async put<T>(
    endpoint: string,
    body?: any,
    options?: Omit<ApiClientOptions, 'method' | 'body'>
  ): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'PUT', body })
  }

  /**
   * Convenience method for DELETE requests
   */
  async delete<T>(endpoint: string, options?: Omit<ApiClientOptions, 'method'>): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'DELETE' })
  }

  /**
   * Convenience method for PATCH requests
   */
  async patch<T>(
    endpoint: string,
    body?: any,
    options?: Omit<ApiClientOptions, 'method' | 'body'>
  ): Promise<T> {
    return this.request<T>(endpoint, { ...options, method: 'PATCH', body })
  }
}

// Export singleton instance
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
export const apiClient = new ApiClient(API_URL)
