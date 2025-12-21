import { fetchJobs } from '@/lib/api'
import { JobFilters, JobLevel } from '@/lib/types'

interface SearchJobsArgs {
  search?: string
  location?: string
  level?: 'junior' | 'middle' | 'senior' | 'lead'
  limit?: number
}

export async function searchJobs(args: SearchJobsArgs) {
  try {
    const filters: JobFilters = {
      search: args.search,
      location: args.location,
      level: args.level as JobLevel | undefined,
      limit: args.limit || 10,
    }
    
    const jobs = await fetchJobs(filters)
    
    // Format results for AI
    const formattedJobs = jobs.map(job => ({
      id: job.id,
      title: job.title,
      company: job.company.name,
      company_id: job.company_id,
      location: job.location,
      level: job.level,
      salary: job.salary,
      description: job.description.substring(0, 200) + '...', // Truncate for context
      url: `http://localhost:3000/jobs/${job.id}`,
    }))
    
    return {
      success: true,
      count: formattedJobs.length,
      jobs: formattedJobs,
      message: formattedJobs.length > 0 
        ? `Found ${formattedJobs.length} matching job(s)`
        : 'No jobs found matching the criteria',
    }
  } catch (error: any) {
    return {
      success: false,
      error: error.message || 'Failed to search jobs',
    }
  }
}
