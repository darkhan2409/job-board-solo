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
