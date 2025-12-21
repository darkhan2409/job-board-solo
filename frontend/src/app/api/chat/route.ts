import { NextRequest, NextResponse } from 'next/server'
import OpenAI from 'openai'

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
})

const SYSTEM_PROMPT = `You are a helpful career assistant for a job board platform. You help users find jobs, learn about companies, and understand technologies.

You have access to the following tools:
1. search_jobs - Search for jobs with filters (location, level, keywords)
2. get_company_info - Get detailed information about a company
3. validate_job_page - Validate that a job page displays correctly (uses Playwright)
4. explain_technology - Explain a technology using official documentation (uses Context7)

Be friendly, concise, and helpful. When recommending jobs, explain why they might be a good fit.`

const tools: OpenAI.Chat.Completions.ChatCompletionTool[] = [
  {
    type: 'function',
    function: {
      name: 'search_jobs',
      description: 'Search for jobs with optional filters. Returns a list of matching jobs.',
      parameters: {
        type: 'object',
        properties: {
          search: {
            type: 'string',
            description: 'Search query for job title or keywords (e.g., "React developer", "Python")',
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
            description: 'Maximum number of results to return (default: 5)',
          },
        },
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'get_company_info',
      description: 'Get detailed information about a specific company, including all open positions.',
      parameters: {
        type: 'object',
        properties: {
          company_id: {
            type: 'number',
            description: 'The ID of the company',
          },
        },
        required: ['company_id'],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'validate_job_page',
      description: 'Validate that a job detail page displays correctly using browser automation. Checks if all required elements are present.',
      parameters: {
        type: 'object',
        properties: {
          job_id: {
            type: 'number',
            description: 'The ID of the job to validate',
          },
        },
        required: ['job_id'],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'explain_technology',
      description: 'Explain a technology or framework using official documentation. Useful when user asks "What is X?" or needs to understand a technology mentioned in a job.',
      parameters: {
        type: 'object',
        properties: {
          technology: {
            type: 'string',
            description: 'The technology to explain (e.g., "React", "Next.js", "FastAPI", "Docker")',
          },
          topic: {
            type: 'string',
            description: 'Optional specific topic to focus on (e.g., "hooks", "routing", "deployment")',
          },
        },
        required: ['technology'],
      },
    },
  },
]

export async function POST(req: NextRequest) {
  try {
    const { messages } = await req.json()

    if (!messages || !Array.isArray(messages)) {
      return NextResponse.json(
        { error: 'Messages array is required' },
        { status: 400 }
      )
    }

    // Create chat completion with streaming
    const response = await openai.chat.completions.create({
      model: 'gpt-4-turbo-preview',
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        ...messages,
      ],
      tools,
      tool_choice: 'auto',
      stream: true,
      temperature: 0.7,
      max_tokens: 1000,
    })

    // Create a readable stream for SSE
    const encoder = new TextEncoder()
    const stream = new ReadableStream({
      async start(controller) {
        try {
          for await (const chunk of response) {
            const delta = chunk.choices[0]?.delta
            
            if (delta?.content) {
              // Send content chunk
              const data = JSON.stringify({
                type: 'content',
                content: delta.content,
              })
              controller.enqueue(encoder.encode(`data: ${data}\n\n`))
            }
            
            if (delta?.tool_calls) {
              // Send tool call chunk
              const data = JSON.stringify({
                type: 'tool_call',
                tool_calls: delta.tool_calls,
              })
              controller.enqueue(encoder.encode(`data: ${data}\n\n`))
            }
            
            if (chunk.choices[0]?.finish_reason === 'tool_calls') {
              // Tool calls complete
              const data = JSON.stringify({
                type: 'tool_calls_complete',
              })
              controller.enqueue(encoder.encode(`data: ${data}\n\n`))
            }
            
            if (chunk.choices[0]?.finish_reason === 'stop') {
              // Completion finished
              const data = JSON.stringify({
                type: 'done',
              })
              controller.enqueue(encoder.encode(`data: ${data}\n\n`))
            }
          }
        } catch (error) {
          console.error('Streaming error:', error)
          const data = JSON.stringify({
            type: 'error',
            error: 'Streaming failed',
          })
          controller.enqueue(encoder.encode(`data: ${data}\n\n`))
        } finally {
          controller.close()
        }
      },
    })

    return new Response(stream, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    })
  } catch (error) {
    console.error('Chat API error:', error)
    return NextResponse.json(
      { error: 'Failed to process chat request' },
      { status: 500 }
    )
  }
}
