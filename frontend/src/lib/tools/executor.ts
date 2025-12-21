import { searchJobs } from './search-jobs'
import { getCompanyInfo } from './get-company'
import { validateJobPage } from './validate-job'
import { explainTechnology } from './explain-tech'

export async function executeToolCall(toolName: string, args: any) {
  console.log(`Executing tool: ${toolName}`, args)

  try {
    switch (toolName) {
      case 'search_jobs':
        return await searchJobs(args)
      
      case 'get_company_info':
        return await getCompanyInfo(args)
      
      case 'validate_job_page':
        return await validateJobPage(args)
      
      case 'explain_technology':
        return await explainTechnology(args)
      
      default:
        return {
          success: false,
          error: `Unknown tool: ${toolName}`,
        }
    }
  } catch (error) {
    console.error(`Tool execution error (${toolName}):`, error)
    return {
      success: false,
      error: `Failed to execute ${toolName}`,
    }
  }
}
