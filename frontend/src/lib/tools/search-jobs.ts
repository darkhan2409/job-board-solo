import { fetchJobs } from '@/lib/api'
import { JobLevel } from '@/lib/types'

interface SearchJobsParams {
  search?: string
  location?: string
  level?: JobLevel
  limit?: number
}

export async function searchJobs(params: SearchJobsParams) {
  try {
    const jobs = await fetchJobs({
      search: params.search,
      location: params.location,
      level: params.level,
      limit: params.limit || 5,
    })

    // Format jobs for AI response
    const formattedJobs = jobs.map(job => ({
      id: job.id,
      title: job.title,
      company: job.company?.name || 'Unknown',
      location: job.location,
      level: job.level,
      salary: job.salary,
      description: job.description.substring(0, 200) + '...',
      url: `/jobs/${job.id}`,
    }))

    return {
      success: true,
      count: formattedJobs.length,
      jobs: formattedJobs,
    }
  } catch (error) {
    console.error('Search jobs error:', error)
    return {
      success: false,
      error: 'Failed to search jobs',
    }
  }
}
