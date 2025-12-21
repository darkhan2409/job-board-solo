import { fetchCompanyById } from '@/lib/api'

interface GetCompanyParams {
  company_id: number
}

export async function getCompanyInfo(params: GetCompanyParams) {
  try {
    const company = await fetchCompanyById(params.company_id)

    // Format company data for AI response
    return {
      success: true,
      company: {
        id: company.id,
        name: company.name,
        description: company.description,
        website: company.website,
        open_positions: company.jobs?.length || 0,
        jobs: company.jobs?.map(job => ({
          id: job.id,
          title: job.title,
          location: job.location,
          level: job.level,
          salary: job.salary,
          url: `/jobs/${job.id}`,
        })),
      },
    }
  } catch (error) {
    console.error('Get company error:', error)
    return {
      success: false,
      error: 'Failed to get company information',
    }
  }
}
