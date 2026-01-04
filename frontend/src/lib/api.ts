// API client for backend communication

import {
  Job,
  JobFilters,
  Company,
  CompanyWithJobs,
  LoginRequest,
  RegisterRequest,
  TokenResponse,
  User,
  OAuthUrlResponse,
  PasswordResetRequest,
  PasswordReset,
  SavedJob
} from './types'
import { getAuthHeaders, getRefreshToken } from './auth'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

/**
 * Default fetch options for CORS support
 * Includes credentials to allow cookies and auth headers
 */
const defaultFetchOptions: RequestInit = {
  credentials: 'include', // Include cookies and auth headers for CORS
}

export async function fetchJobs(filters?: JobFilters): Promise<Job[]> {
  const params = new URLSearchParams()
  
  if (filters?.location) params.append('location', filters.location)
  if (filters?.level) params.append('level', filters.level)
  if (filters?.search) params.append('search', filters.search)
  if (filters?.skip !== undefined) params.append('skip', filters.skip.toString())
  if (filters?.limit !== undefined) params.append('limit', filters.limit.toString())
  
  const url = `${API_URL}/api/jobs${params.toString() ? `?${params.toString()}` : ''}`
  
  const res = await fetch(url, {
    ...defaultFetchOptions,
    cache: 'no-store',
  })
  
  if (!res.ok) {
    throw new Error(`Failed to fetch jobs: ${res.status}`)
  }
  
  return res.json()
}

export async function fetchJobById(id: number): Promise<Job> {
  const res = await fetch(`${API_URL}/api/jobs/${id}`, {
    ...defaultFetchOptions,
    cache: 'no-store',
  })
  
  if (!res.ok) {
    if (res.status === 404) {
      throw new Error('Job not found')
    }
    throw new Error(`Failed to fetch job: ${res.status}`)
  }
  
  return res.json()
}

export async function fetchCompanies(): Promise<Company[]> {
  const res = await fetch(`${API_URL}/api/companies`, {
    ...defaultFetchOptions,
    cache: 'no-store',
  })
  
  if (!res.ok) {
    throw new Error(`Failed to fetch companies: ${res.status}`)
  }
  
  return res.json()
}

export async function fetchCompanyById(id: number): Promise<CompanyWithJobs> {
  const res = await fetch(`${API_URL}/api/companies/${id}`, {
    ...defaultFetchOptions,
    cache: 'no-store',
  })

  if (!res.ok) {
    if (res.status === 404) {
      throw new Error('Company not found')
    }
    throw new Error(`Failed to fetch company: ${res.status}`)
  }

  return res.json()
}

// Authentication API

export async function loginUser(data: LoginRequest): Promise<TokenResponse> {
  const res = await fetch(`${API_URL}/api/auth/login`, {
    ...defaultFetchOptions,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Login failed' }))
    throw new Error(error.detail || 'Login failed')
  }

  return res.json()
}

export async function registerUser(data: RegisterRequest): Promise<User> {
  const res = await fetch(`${API_URL}/api/auth/register`, {
    ...defaultFetchOptions,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Registration failed' }))
    throw new Error(error.detail || 'Registration failed')
  }

  return res.json()
}

export async function logoutUser(refreshToken: string): Promise<void> {
  const res = await fetch(`${API_URL}/api/auth/logout`, {
    ...defaultFetchOptions,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify({ refresh_token: refreshToken }),
  })

  if (!res.ok) {
    throw new Error('Logout failed')
  }
}

export async function refreshAccessToken(refreshToken: string): Promise<TokenResponse> {
  const res = await fetch(`${API_URL}/api/auth/refresh`, {
    ...defaultFetchOptions,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh_token: refreshToken }),
  })

  if (!res.ok) {
    throw new Error('Token refresh failed')
  }

  return res.json()
}

// OAuth API

export async function getOAuthUrl(provider: 'google' | 'github'): Promise<OAuthUrlResponse> {
  const res = await fetch(`${API_URL}/api/auth/${provider}`, {
    ...defaultFetchOptions,
    method: 'GET',
  })

  if (!res.ok) {
    throw new Error(`Failed to get ${provider} OAuth URL`)
  }

  return res.json()
}

export async function handleOAuthCallback(
  provider: 'google' | 'github',
  code: string,
  state: string
): Promise<TokenResponse> {
  const res = await fetch(`${API_URL}/api/auth/${provider}/callback`, {
    ...defaultFetchOptions,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ code, state }),
  })

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'OAuth callback failed' }))
    throw new Error(error.detail || 'OAuth callback failed')
  }

  return res.json()
}

// Password Reset API

export async function requestPasswordReset(email: string): Promise<void> {
  const res = await fetch(`${API_URL}/api/auth/request-password-reset`, {
    ...defaultFetchOptions,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email }),
  })

  // Backend always returns 204 for security (don't reveal if email exists)
  if (!res.ok && res.status !== 204) {
    const error = await res.json().catch(() => ({ detail: 'Failed to request password reset' }))
    throw new Error(error.detail || 'Failed to request password reset')
  }
}

export async function resetPassword(token: string, newPassword: string): Promise<User> {
  const res = await fetch(`${API_URL}/api/auth/reset-password`, {
    ...defaultFetchOptions,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ token, new_password: newPassword }),
  })

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Failed to reset password' }))
    throw new Error(error.detail || 'Failed to reset password')
  }

  return res.json()
}

// Saved Jobs API

export async function getSavedJobs(): Promise<SavedJob[]> {
  const res = await fetch(`${API_URL}/api/saved-jobs`, {
    ...defaultFetchOptions,
    headers: getAuthHeaders(),
    cache: 'no-store',
  })

  if (!res.ok) {
    throw new Error('Failed to fetch saved jobs')
  }

  return res.json()
}

export async function checkJobSaved(jobId: number): Promise<boolean> {
  const res = await fetch(`${API_URL}/api/saved-jobs/${jobId}/check`, {
    ...defaultFetchOptions,
    headers: getAuthHeaders(),
    cache: 'no-store',
  })

  if (!res.ok) {
    return false
  }

  const data = await res.json()
  return data.is_saved
}

export async function saveJob(jobId: number): Promise<SavedJob> {
  const res = await fetch(`${API_URL}/api/saved-jobs`, {
    ...defaultFetchOptions,
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeaders(),
    },
    body: JSON.stringify({ job_id: jobId }),
  })

  if (!res.ok) {
    if (res.status === 401) {
      throw new Error('Unauthorized: Please login to save jobs')
    }
    const error = await res.json().catch(() => ({ detail: 'Failed to save job' }))
    throw new Error(error.detail || 'Failed to save job')
  }

  return res.json()
}

export async function unsaveJob(jobId: number): Promise<void> {
  const res = await fetch(`${API_URL}/api/saved-jobs/${jobId}`, {
    ...defaultFetchOptions,
    method: 'DELETE',
    headers: getAuthHeaders(),
  })

  if (!res.ok) {
    throw new Error('Failed to unsave job')
  }
}
