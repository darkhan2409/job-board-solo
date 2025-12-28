// TypeScript types matching backend schemas

export type JobLevel = "junior" | "middle" | "senior" | "lead"

export interface Company {
  id: number
  name: string
  description?: string
  logo?: string
  website?: string
  job_count?: number
}

export interface Job {
  id: number
  title: string
  description: string
  location: string
  salary?: string
  level: JobLevel
  company_id: number
  created_at: string
  company?: Company
}

export interface JobFilters {
  location?: string
  level?: JobLevel
  search?: string
  skip?: number
  limit?: number
}

export interface CompanyWithJobs extends Company {
  jobs: Job[]
}

// Authentication types
export enum UserRole {
  REGULAR_USER = "REGULAR_USER",
  EMPLOYER = "EMPLOYER",
  ADMIN = "ADMIN",
}

export interface User {
  id: number
  email: string
  full_name: string
  role: UserRole
  is_active: boolean
  is_verified: boolean
  oauth_provider?: string | null
  created_at: string
}

export interface LoginRequest {
  email: string
  password: string
  remember_me?: boolean
}

export interface RegisterRequest {
  email: string
  password: string
  full_name: string
  role?: UserRole
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

export interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

export interface OAuthUrlResponse {
  authorization_url: string
  state: string
}

// Password reset types
export interface PasswordResetRequest {
  email: string
}

export interface PasswordReset {
  token: string
  new_password: string
}

// Saved jobs types
export interface SavedJob {
  user_id: number
  job_id: number
  saved_at: string
  job: Job
}
