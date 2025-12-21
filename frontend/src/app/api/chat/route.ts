import { NextRequest, NextResponse } from 'next/server'
import OpenAI from 'openai'
import { searchJobsTool, getCompanyInfoTool, validateJobPageTool, explainTechnologyTool } from '@/lib/tools-definition'

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
})

const SYSTEM_PROMPT = `You are a helpful career assistant for a job board platform. Your role is to:

1. Help users find relevant job opportunities based on their skills and preferences
2. Provide information about companies and their open positions
3. Explain technologies and tools mentioned in job descriptions
4. Validate that job pages are displaying correctly

You have access to the following tools:
- search_jobs: Search for jobs with filters (location, level, keywords)
- get_company_info: Get detailed information about a specific company
- validate_job_page: Check if a job page is displaying correctly (uses Playwright MCP)
- explain_technology: Get official documentation about a technology (uses Context7 MCP)

Be friendly, professional, and concise. When recommending jobs, explain why they might be a good fit.`

export async function POST(req: NextRequest) {
  try {
    const { messages } = await req.json()
    
    if (!messages || !Array.isArray(messages)) {
      return NextResponse.json(
        { error: 'Invalid request: messages array required' },
        { status: 400 }
      )
    }
    
    // Add system message
    const messagesWithSystem = [
      { role: 'system', content: SYSTEM_PROMPT },
      ...messages,
    ]
    
    // Call OpenAI with tools
    const response = await openai.chat.completions.create({
      model: 'gpt-4-turbo-preview',
      messages: messagesWithSystem as any,
      tools: [
        searchJobsTool,
        getCompanyInfoTool,
        validateJobPageTool,
        explainTechnologyTool,
      ],
      tool_choice: 'auto',
      temperature: 0.7,
      max_tokens: 1000,
    })
    
    const assistantMessage = response.choices[0].message
    
    // Check if tool calls are needed
    if (assistantMessage.tool_calls && assistantMessage.tool_calls.length > 0) {
      // Execute tool calls
      const toolResults = await Promise.all(
        assistantMessage.tool_calls.map(async (toolCall) => {
          const toolName = toolCall.function.name
          const toolArgs = JSON.parse(toolCall.function.arguments)
          
          let result
          
          try {
            // Import and execute the appropriate tool
            if (toolName === 'search_jobs') {
              const { searchJobs } = await import('@/app/api/tools/search-jobs')
              result = await searchJobs(toolArgs)
            } else if (toolName === 'get_company_info') {
              const { getCompanyInfo } = await import('@/app/api/tools/get-company')
              result = await getCompanyInfo(toolArgs)
            } else if (toolName === 'validate_job_page') {
              const { validateJobPage } = await import('@/app/api/tools/validate-job')
              result = await validateJobPage(toolArgs)
            } else if (toolName === 'explain_technology') {
              const { explainTechnology } = await import('@/app/api/tools/explain-tech')
              result = await explainTechnology(toolArgs)
            } else {
              result = { error: `Unknown tool: ${toolName}` }
            }
          } catch (error: any) {
            result = { error: error.message || 'Tool execution failed' }
          }
          
          return {
            tool_call_id: toolCall.id,
            role: 'tool' as const,
            name: toolName,
            content: JSON.stringify(result),
          }
        })
      )
      
      // Call OpenAI again with tool results
      const finalResponse = await openai.chat.completions.create({
        model: 'gpt-4-turbo-preview',
        messages: [
          ...messagesWithSystem,
          assistantMessage,
          ...toolResults,
        ] as any,
        temperature: 0.7,
        max_tokens: 1000,
      })
      
      return NextResponse.json({
        message: finalResponse.choices[0].message.content,
        tool_calls: assistantMessage.tool_calls.map(tc => ({
          name: tc.function.name,
          arguments: JSON.parse(tc.function.arguments),
        })),
      })
    }
    
    // No tool calls, return direct response
    return NextResponse.json({
      message: assistantMessage.content,
    })
    
  } catch (error: any) {
    console.error('Chat API error:', error)
    return NextResponse.json(
      { error: error.message || 'Internal server error' },
      { status: 500 }
    )
  }
}
