# AI Engineer AI Rules

## Role
AI Engineer - Conversational Agent Architect using OpenAI API + Tool Calling + Playwright MCP

## System Rules

### Code Generation Philosophy
- You are an **agentic AI architect**, not a chatbot builder
- Build **intelligent agents with tools**, not simple completion endpoints
- Every agent must **call external tools/functions**, not just generate text
- Use **streaming responses** for better UX
- Design **multi-turn conversations** with memory/context
- Implement **structured outputs** for reliable parsing
- Code must be **production-ready** with error handling

### Technology Stack Mandate
- OpenAI API (GPT-4 or GPT-4 Turbo)
- Playwright MCP (already installed - just call it)
- Next.js API Routes (for backend integration)
- Server-Sent Events (SSE) for streaming
- TypeScript for type safety
- Zod for schema validation

## Project Structure (MANDATORY)
```
frontend/src/app/api/
├── chat/
│   └── route.ts              # Main chat endpoint (POST)
├── tools/
│   ├── search-jobs.ts        # Job search tool logic
│   ├── get-company.ts        # Company info tool logic
│   └── validate-job.ts       # Playwright MCP integration

frontend/src/lib/
├── openai.ts                 # OpenAI API client wrapper
├── tools-definition.ts       # Tool schemas for OpenAI
└── playwright-mcp.ts         # Playwright MCP client

frontend/src/components/
├── ChatWidget.tsx            # Chat UI (Client Component)
├── ChatMessage.tsx           # Message bubble component
└── ChatInput.tsx             # Input with send button
```

## Agent Architecture
```
User Input
    ↓
Intent Classification (OpenAI)
    ↓
Tool Selection (OpenAI decides which tools to call)
    ↓
Tool Execution (Your code executes tools)
    ↓
Tool Results → OpenAI
    ↓
Response Generation (OpenAI synthesizes answer)
    ↓
Stream to User
```

## Tool Calling Requirements

### OpenAI Tool Definition Pattern (MANDATORY)

Every tool must have:
1. **type** - Always "function"
2. **function.name** - Function identifier (snake_case)
3. **function.description** - Clear explanation
4. **function.parameters** - JSON Schema

### Required Tools:

#### 1. search_jobs (REQUIRED)
**Purpose:** Search and filter jobs

**OpenAI Schema:**
```typescript
{
  type: "function",
  function: {
    name: "search_jobs",
    description: "Search for jobs based on skills, location, and seniority level. Returns matching job listings with company details.",
    parameters: {
      type: "object",
      properties: {
        skills: {
          type: "array",
          items: { type: "string" },
          description: "Technical skills or technologies (e.g., ['React', 'Python'])"
        },
        location: {
          type: "string",
          description: "Job location (e.g., 'Remote', 'San Francisco')"
        },
        level: {
          type: "string",
          enum: ["junior", "middle", "senior", "lead"],
          description: "Seniority level"
        }
      },
      required: ["skills"]
    }
  }
}
```

#### 2. get_company_info (REQUIRED)
**Purpose:** Get company details

**OpenAI Schema:**
```typescript
{
  type: "function",
  function: {
    name: "get_company_info",
    description: "Retrieve detailed company information including all jobs.",
    parameters: {
      type: "object",
      properties: {
        company_id: {
          type: "number",
          description: "Unique company identifier"
        }
      },
      required: ["company_id"]
    }
  }
}
```

#### 3. validate_job_page (REQUIRED - PLAYWRIGHT MCP)
**Purpose:** Validate job page using Playwright

**OpenAI Schema:**
```typescript
{
  type: "function",
  function: {
    name: "validate_job_page",
    description: "Use Playwright to verify a job page displays correctly. Returns validation results.",
    parameters: {
      type: "object",
      properties: {
        job_id: {
          type: "number",
          description: "Job ID to validate"
        },
        checks: {
          type: "array",
          items: {
            type: "string",
            enum: ["title", "company", "description", "apply_button"]
          },
          description: "Which elements to validate"
        }
      },
      required: ["job_id"]
    }
  }
}
```

## System Prompt (MANDATORY)
```
You are an AI career assistant helping users find jobs that match their skills and interests.

CAPABILITIES:
- Search jobs by skills, location, and level
- Provide detailed company information
- Validate job listings using automated browser tests (Playwright)
- Match user skills against job requirements

TOOLS AVAILABLE:
1. search_jobs - Find jobs matching criteria
2. get_company_info - Get company details
3. validate_job_page - Use Playwright to check if job page works correctly

BEHAVIOR RULES:
- ALWAYS use tools to get real data (don't make up job listings)
- When user mentions skills, call search_jobs
- When user asks about a company, call get_company_info
- When user reports a bug or asks "does this work?", use validate_job_page
- Provide 3-5 job recommendations maximum per response
- Explain WHY each job is a good match
- Ask follow-up questions to refine search

PLAYWRIGHT MCP USAGE:
- Use validate_job_page when user questions if a job page works
- Report test results in user-friendly language (not raw logs)
- Suggest fixes if tests fail

RESPONSE FORMAT:
- Start with conversational acknowledgment
- Present findings with clear structure
- End with follow-up question or next step suggestion

EXAMPLE:
User: "I know React and Node.js, looking for remote senior roles"
You: [Call search_jobs with skills=["React", "Node.js"], location="Remote", level="senior"]
You: "I found 4 remote senior positions that match your React and Node.js experience:

1. **Senior Full-Stack Engineer at TechCorp**
   - Why it matches: Heavy React frontend + Node.js microservices
   - Salary: $150-180k
   - [View Details]

Would you like me to verify any of these job pages are displaying correctly?"
```

## OpenAI API Integration

### API Route Pattern:
```typescript
// app/api/chat/route.ts

import OpenAI from 'openai'

export async function POST(req: Request) {
  const { messages } = await req.json()
  
  const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
  })
  
  const tools = [
    searchJobsTool,
    getCompanyInfoTool,
    validateJobPageTool
  ]
  
  const stream = await openai.chat.completions.create({
    model: 'gpt-4-turbo-preview',
    messages: messages,
    tools: tools,
    tool_choice: 'auto',
    stream: true
  })
  
  // Handle streaming + tool calls
  // Return SSE to client
}
```

### OpenAI Response Format:

**Tool call:**
```typescript
{
  role: "assistant",
  content: null,
  tool_calls: [{
    id: "call_abc123",
    type: "function",
    function: {
      name: "search_jobs",
      arguments: '{"skills": ["React"]}'
    }
  }]
}
```

**Tool result:**
```typescript
{
  role: "tool",
  tool_call_id: "call_abc123",
  content: JSON.stringify(result)
}
```

## Playwright MCP Integration (CRITICAL)

### Playwright MCP is Already Installed

Your job: **Call it from code**.

### How to Call Playwright MCP:
```typescript
// lib/playwright-mcp.ts

import { Client } from '@modelcontextprotocol/sdk/client/index.js'
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js'

export async function validateJobPage(jobId: number) {
  // Create transport
  const transport = new StdioClientTransport({
    command: 'npx',
    args: ['-y', '@playwright/test']
  })
  
  // Create client
  const client = new Client({
    name: "job-board-agent",
    version: "1.0.0"
  }, {
    capabilities: {}
  })
  
  // Connect
  await client.connect(transport)
  
  // Navigate to page
  await client.callTool({
    name: 'playwright_navigate',
    arguments: {
      url: `http://localhost:3000/jobs/${jobId}`
    }
  })
  
  // Check title exists
  const titleCheck = await client.callTool({
    name: 'playwright_querySelector',
    arguments: {
      selector: 'h1[data-testid="job-title"]'
    }
  })
  
  // Take screenshot
  const screenshot = await client.callTool({
    name: 'playwright_screenshot',
    arguments: {
      path: `./test-results/job-${jobId}.png`
    }
  })
  
  // Close
  await client.close()
  
  return {
    success: titleCheck.isSuccessful,
    screenshot: screenshot.path
  }
}
```

### Tool Implementation:
```typescript
// app/api/tools/validate-job.ts

import { validateJobPage } from '@/lib/playwright-mcp'

export async function validate_job_page(job_id: number) {
  try {
    const result = await validateJobPage(job_id)
    return {
      status: "success",
      message: `Job page #${job_id} validated successfully`,
      checks: {
        title_visible: true,
        company_visible: true,
        apply_button: true
      },
      screenshot: result.screenshot
    }
  } catch (error) {
    return {
      status: "error",
      message: `Failed to validate: ${error.message}`
    }
  }
}
```

### When to Call Playwright MCP:

1. User asks "Does this job page work?"
2. User reports bug
3. After recommending jobs (optional validation)
4. User asks "Is the site working?"

## Context7 MCP Integration (DOCUMENTATION)

### Purpose
Load official documentation for technologies mentioned in jobs and questions.

### When to Use Context7:
1. **During development** - Load docs for FastAPI, Next.js, OpenAI API
2. **When user asks about tech** - "What is React hooks?"
3. **When job mentions tech stack** - Load docs to explain requirements
4. **When suggesting learning** - Provide official resources

### How to Call Context7 MCP:
````typescript
// lib/context7-mcp.ts

import { Client } from '@modelcontextprotocol/sdk/client/index.js'
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js'

export async function loadTechDocs(techName: string, topic?: string) {
  const transport = new StdioClientTransport({
    command: 'npx',
    args: ['-y', '@context7/mcp-server']
  })
  
  const client = new Client({
    name: "job-board-agent",
    version: "1.0.0"
  }, {
    capabilities: {}
  })
  
  await client.connect(transport)
  
  // Map tech names to Context7 library IDs
  const libraryMap: Record<string, string> = {
    'React': '/facebook/react',
    'Next.js': '/vercel/next.js',
    'FastAPI': '/tiangolo/fastapi',
    'Python': '/python/cpython',
    'TypeScript': '/microsoft/typescript',
    'Tailwind': '/tailwindlabs/tailwindcss',
    'Playwright': '/microsoft/playwright',
    'OpenAI': '/openai/openai-node',
    'SQLAlchemy': '/sqlalchemy/sqlalchemy',
    'PostgreSQL': '/postgres/postgres',
    'Node.js': '/nodejs/node'
  }
  
  const libraryId = libraryMap[techName]
  
  if (!libraryId) {
    await client.close()
    throw new Error(`Unknown tech: ${techName}`)
  }
  
  // Load documentation
  const result = await client.callTool({
    name: 'get-library-docs',
    arguments: {
      context7CompatibleLibraryID: libraryId,
      topic: topic,
      tokens: 3000
    }
  })
  
  await client.close()
  
  return result.content
}
````

### Required Tools - Add 4th Tool:

#### 4. explain_technology (REQUIRED - CONTEXT7 MCP)
**Purpose:** Explain technology concepts using official documentation

**OpenAI Schema:**
````typescript
{
  type: "function",
  function: {
    name: "explain_technology",
    description: "Load official documentation to explain a technology or concept. Use when user asks 'What is X?' or when job mentions unfamiliar tech.",
    parameters: {
      type: "object",
      properties: {
        technology: {
          type: "string",
          description: "Technology name (e.g., 'React', 'FastAPI', 'Next.js')"
        },
        topic: {
          type: "string",
          description: "Specific topic within the tech (e.g., 'hooks', 'async', 'routing')"
        }
      },
      required: ["technology"]
    }
  }
}
````

**Implementation:**
````typescript
// app/api/tools/explain-tech.ts

import { loadTechDocs } from '@/lib/context7-mcp'

export async function explain_technology(technology: string, topic?: string) {
  try {
    const docs = await loadTechDocs(technology, topic)
    
    return {
      status: "success",
      technology: technology,
      topic: topic,
      documentation: docs,
      source: "Official documentation via Context7 MCP"
    }
  } catch (error) {
    return {
      status: "error",
      message: `Could not load documentation for ${technology}`,
      suggestion: "Try searching online or ask for a different technology"
    }
  }
}
````

### When to Call Context7:

**Scenario 1: User asks about technology**
````
User: "What is React Server Components?"
AI: [calls explain_technology("React", "Server Components")]
AI: "React Server Components are a new feature that..."
    [explains using Context7 docs]
````

**Scenario 2: Job mentions unfamiliar tech**
````
User: "Show me jobs with GraphQL"
AI: [calls search_jobs(skills=["GraphQL"])]
AI: "I found 3 GraphQL positions. Would you like me to explain what GraphQL is?"
User: "Yes"
AI: [calls explain_technology("GraphQL")]
AI: "GraphQL is a query language for APIs..."
````

**Scenario 3: Suggesting learning path**
````
User: "I know Python, what should I learn for this job?"
AI: [analyzes job requirements]
AI: "This job requires FastAPI. Let me explain it:"
    [calls explain_technology("FastAPI")]
AI: "FastAPI is a modern Python web framework..."
````

### Integration in System Prompt:

Update system prompt to include:
````
TOOLS AVAILABLE:
1. search_jobs - Find jobs matching criteria
2. get_company_info - Get company details
3. validate_job_page - Use Playwright to check if job page works correctly
4. explain_technology - Load official documentation to explain tech concepts

CONTEXT7 MCP USAGE:
- Use explain_technology when user asks "What is X?"
- Use when job mentions unfamiliar technology
- Reference official docs when explaining requirements
- Provide learning resources from documentation
````

### MCP Evidence Required:

**For WORKFLOW.md:**
1. Screenshot of Context7 loading docs
2. Console logs showing MCP connection
3. Example where AI explains tech using Context7
4. List of technologies documented via Context7

Example entry:
````markdown
## Context7 MCP Usage

### Loading FastAPI Documentation
User asked about async endpoints in FastAPI.

Code calling Context7:
![Context7 Code](./screenshots/context7-code.png)

Console showing MCP loading docs:
![Context7 Logs](./screenshots/context7-logs.png)

AI response using loaded documentation:
![AI Explanation](./screenshots/ai-explanation-fastapi.png)

### Technologies Loaded via Context7:
1. FastAPI - for async patterns
2. Next.js - for App Router data fetching
3. OpenAI API - for tool calling format
4. React - for Server Components explanation
5. Playwright - for testing best practices
````

### Completion Checklist Update:

- [ ] Context7 MCP client created
- [ ] explain_technology tool implemented
- [ ] AI agent can load docs for 5+ technologies
- [ ] System prompt includes Context7 usage
- [ ] WORKFLOW.md documents Context7 usage
- [ ] 3+ screenshots showing Context7 in action
- [ ] Logs show Context7 MCP communication

## Response Formatting

### Job Recommendation Format:
```
I found [N] jobs that match your [criteria]:

1. **[Job Title] at [Company Name]**
   💰 Salary: [range]
   📍 Location: [location]
   📊 Level: [level]
   ✨ Why it matches: [explanation]
   🔗 [View Details]
   ✅ Verified: Page loads correctly

2. **[Next job]**
   ...

💡 Next steps: [suggestion]
❓ Questions: [follow-up]
```

### Test Result Format:
```
🧪 Test Results: Job Detail Page

✅ Job title visible
✅ Company logo loaded
✅ Description complete
❌ Apply button not clickable (bug detected)

📸 Screenshot: [path]

Recommendation: Apply button needs fixing.
```

## Error Handling

### Tool Execution Errors:
```typescript
try {
  const jobs = await searchJobs(input)
} catch (error) {
  return {
    role: "tool",
    tool_call_id: toolCallId,
    content: JSON.stringify({
      error: "Failed to search jobs",
      suggestion: "Try again or rephrase"
    })
  }
}
```

### Playwright MCP Errors:
```typescript
try {
  const result = await validateJobPage(jobId)
} catch (error) {
  return {
    status: "error",
    message: "Cannot run browser tests right now"
  }
}
```

## Frontend Integration

### Chat Widget:

**Component Structure:**
```
ChatWidget (Client Component)
├── ChatMessages
│   └── ChatMessage
├── ChatInput
└── TypingIndicator
```

**API Communication:**
```typescript
async function sendMessage(content: string) {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      messages: [...previousMessages, { role: 'user', content }]
    })
  })
  
  // Handle SSE stream
  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    
    const chunk = decoder.decode(value)
    // Parse and update UI
  }
}
```

## Anti-Patterns (NEVER DO)

### ❌ Forbidden:
- Simple GPT completion without tools
- Hallucinating job listings
- Ignoring tool results
- Not using Playwright MCP
- Sync API calls
- Exposing API keys in frontend
- Missing error handling
- No streaming
- Untyped tool schemas
- Forgetting conversation context

### ✅ Always Do:
- Use OpenAI tools for data
- Integrate Playwright MCP
- Stream responses
- Handle errors gracefully
- Type all schemas
- Test tool execution
- Limit recommendations (3-5)
- Validate job pages with Playwright
- Maintain context
- Log MCP usage

## Environment Variables
```
OPENAI_API_KEY=sk-...
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Output Format

### When Generating Code:

1. Show file path
2. Mark as Server-side (API route)
3. Generate complete code with types
4. Include tool definitions
5. Include system prompt
6. Explain behavior (2-3 sentences)
7. Show example flow
8. Demonstrate Playwright MCP usage

## Commit Message Format
```
feat(ai): AI-generated [component]

[What was created]
Tools: search_jobs, get_company_info, validate_job_page
MCP: Playwright for browser automation
API: OpenAI GPT-4 with streaming
Generated by: [Cursor/Windsurf/Claude]
```

## Completion Checklist

- [ ] OpenAI API integrated with streaming
- [ ] 3 tools defined and working
- [ ] Playwright MCP integrated
- [ ] System prompt configured
- [ ] Multi-turn conversations work
- [ ] Tool execution successful
- [ ] Error handling implemented
- [ ] Frontend chat widget working
- [ ] Job recommendations relevant
- [ ] Job pages validated via Playwright
- [ ] Logs show Playwright MCP usage
- [ ] README documents architecture