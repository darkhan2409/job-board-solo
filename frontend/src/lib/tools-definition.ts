// OpenAI tool definitions for function calling

export const searchJobsTool = {
  type: 'function' as const,
  function: {
    name: 'search_jobs',
    description: 'Search for job opportunities with optional filters. Returns a list of matching jobs with company information.',
    parameters: {
      type: 'object',
      properties: {
        search: {
          type: 'string',
          description: 'Search query for job title or keywords (e.g., "React developer", "Python engineer")',
        },
        location: {
          type: 'string',
          description: 'Filter by location (e.g., "Remote", "San Francisco, CA", "New York, NY")',
        },
        level: {
          type: 'string',
          enum: ['junior', 'middle', 'senior', 'lead'],
          description: 'Filter by seniority level',
        },
        limit: {
          type: 'number',
          description: 'Maximum number of results to return (default: 10)',
        },
      },
    },
  },
}

export const getCompanyInfoTool = {
  type: 'function' as const,
  function: {
    name: 'get_company_info',
    description: 'Get detailed information about a specific company, including all their open job positions.',
    parameters: {
      type: 'object',
      properties: {
        company_id: {
          type: 'number',
          description: 'The unique ID of the company',
        },
      },
      required: ['company_id'],
    },
  },
}

export const validateJobPageTool = {
  type: 'function' as const,
  function: {
    name: 'validate_job_page',
    description: 'Validate that a job detail page is displaying correctly using browser automation (Playwright MCP). Checks for required elements like title, company name, description, and apply button.',
    parameters: {
      type: 'object',
      properties: {
        job_id: {
          type: 'number',
          description: 'The unique ID of the job to validate',
        },
      },
      required: ['job_id'],
    },
  },
}

export const explainTechnologyTool = {
  type: 'function' as const,
  function: {
    name: 'explain_technology',
    description: 'Get official documentation and explanation about a technology, framework, or tool using Context7 MCP. Useful when users ask "What is X?" or need to understand technologies mentioned in job descriptions.',
    parameters: {
      type: 'object',
      properties: {
        technology: {
          type: 'string',
          description: 'The name of the technology to explain (e.g., "React", "FastAPI", "Docker", "Kubernetes")',
        },
        topic: {
          type: 'string',
          description: 'Optional specific topic within the technology (e.g., "hooks" for React, "routing" for Next.js)',
        },
      },
      required: ['technology'],
    },
  },
}
