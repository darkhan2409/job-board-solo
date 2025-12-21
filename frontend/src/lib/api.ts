// API client for backend communication

import { Job, JobFilters, Company, CompanyWithJobs } from './types'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function fetchJobs(filters?: JobFilters): Promise<Job[]> {
  const params = new URLSearchParams()
  
  if (filters?.location) params.append('location', filters.location)
  if (filters?.level) params.append('level', filters.level)
  if (filters?.search) params.append('search', filters.search)
  if (filters?.skip !== undefined) params.append('skip', filters.skip.toString())
  if (filters?.limit !== undefined) params.append('limit', filters.limit.toString())
  
  const url = `${API_URL}/api/jobs${params.toString() ? `?${params.toString()}` : ''}`
  
  const res = await fetch(url, {
    cache: 'no-store',
  })
  
  if (!res.ok) {
    throw new Error(`Failed to fetch jobs: ${res.status}`)
  }
  
  return res.json()
}

export async function fetchJobById(id: number): Promise<Job> {
  const res = await fetch(`${API_URL}/api/jobs/${id}`, {
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
    cache: 'no-store',
  })
  
  if (!res.ok) {
    throw new Error(`Failed to fetch companies: ${res.status}`)
  }
  
  return res.json()
}

export async function fetchCompanyById(id: number): Promise<CompanyWithJobs> {
  const res = await fetch(`${API_URL}/api/companies/${id}`, {
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
