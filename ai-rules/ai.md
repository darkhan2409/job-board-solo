# AI Engineer AI Rules

## Role
AI Engineer - Conversational Agent Architect using OpenAI API + Tool Calling

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
│   └── get-company.ts        # Company info tool logic

frontend/src/lib/
└── openai.ts                 # OpenAI API client wrapper

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

## Completion Checklist

- [ ] OpenAI API integrated with streaming
- [ ] 2 tools defined and working (search_jobs, get_company_info)
- [ ] System prompt configured
- [ ] Multi-turn conversations work
- [ ] Tool execution successful
- [ ] Error handling implemented
- [ ] Frontend chat widget working
- [ ] Job recommendations relevant
- [ ] README documents architecture
