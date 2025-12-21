import { fetchCompanyById } from '@/lib/api'

interface GetCompanyInfoArgs {
  company_id: number
}

export async function getCompanyInfo(args: GetCompanyInfoArgs) {
  try {
    const company = await fetchCompanyById(args.company_id)
    
    // Format results for AI
    const formattedCompany = {
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
        url: `http://localhost:3000/jobs/${job.id}`,
      })) || [],
    }
    
    return {
      success: true,
      company: formattedCompany,
      message: `Found company: ${company.name} with ${formattedCompany.open_positions} open position(s)`,
    }
  } catch (error: any) {
    return {
      success: false,
      error: error.message || 'Failed to get company info',
    }
  }
}
