import { searchJobs } from '@/app/api/tools/search-jobs'
import { getCompanyInfo } from '@/app/api/tools/get-company'

export async function executeToolCall(toolName: string, args: any) {
  console.log(`Executing tool: ${toolName}`, args)

  try {
    switch (toolName) {
      case 'search_jobs':
        return await searchJobs(args)
      
      case 'get_company_info':
        return await getCompanyInfo(args)
      
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
