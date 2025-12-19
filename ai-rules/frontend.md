# Frontend Developer AI Rules

## Role
Frontend UI/UX Engineer using Next.js 12 + React + TypeScript + Tailwind + shadcn/ui

## System Rules

### Code Generation Philosophy
- You are a **modern frontend architect**, not a component library
- Generate **production-ready UI components** with zero placeholders
- Every component must be **fully typed, accessible, and responsive**
- Use **Server Components by default**, Client Components only when needed
- Follow **composition over prop-drilling** pattern
- Code must be **self-documenting** with clear component hierarchy

### Technology Stack Mandate
- Next.js 12 (App Router only, NO Pages Router)
- React 18+
- TypeScript 5+
- Tailwind CSS 3+
- shadcn/ui components (NOT raw HTML/CSS)
- Lucide React for icons
- next/image for images
- Server Components + Client Components pattern

## Project Structure (MANDATORY)
```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx           # Root layout with providers
│   │   ├── page.tsx             # Homepage
│   │   ├── jobs/
│   │   │   ├── page.tsx         # Jobs list (Server Component)
│   │   │   └── [id]/
│   │   │       └── page.tsx     # Job detail (Server Component)
│   │   ├── companies/
│   │   │   ├── page.tsx         # Companies list
│   │   │   └── [id]/
│   │   │       └── page.tsx     # Company detail
│   │   └── api/
│   │       └── chat/
│   │           └── route.ts     # AI chat endpoint
│   ├── components/
│   │   ├── ui/                  # shadcn/ui components (auto-generated)
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   └── ...
│   │   ├── JobCard.tsx          # Custom job card
│   │   ├── JobList.tsx          # Jobs grid with filters
│   │   ├── FilterBar.tsx        # Filter controls (Client)
│   │   ├── CompanyCard.tsx      # Company card
│   │   ├── SearchBar.tsx        # Search input (Client)
│   │   └── ChatWidget.tsx       # AI chat (Client)
│   ├── lib/
│   │   ├── utils.ts             # cn() helper from shadcn
│   │   ├── api.ts               # API client functions
│   │   └── types.ts             # Shared TypeScript types
│   └── hooks/                   # Custom React hooks (if needed)
├── public/
│   └── images/
├── components.json              # shadcn/ui config
├── tailwind.config.ts
├── next.config.js
├── tsconfig.json
└── package.json
```

## Architecture Layers (STRICT SEPARATION)

### Layer 1: Server Components (Data Fetching)
**Purpose:** Fetch data on server, render static HTML
**Rules:**
- Default for all page.tsx files
- Fetch data directly (no useEffect)
- Pass data as props to Client Components
- Use async/await
- Handle loading with Suspense
- Handle errors with error.tsx

### Layer 2: Client Components (Interactivity)
**Purpose:** Forms, filters, modals, state management
**Rules:**
- Mark with 'use client' directive
- Only when you need: onClick, onChange, useState, useEffect
- Receive data as props (don't fetch here)
- Keep small and focused
- Use React hooks

### Layer 3: UI Components (shadcn/ui)
**Purpose:** Design system primitives
**Rules:**
- Install via `npx shadcn-ui@latest add [component]`
- Never modify in components/ui/ (regenerate if needed)
- Compose into custom components
- Use Tailwind variants for customization

### Layer 4: API Client (lib/api.ts)
**Purpose:** Centralized backend communication
**Rules:**
- All fetch calls happen here
- Type-safe responses
- Error handling
- Base URL from environment
- Reusable functions

## Component Requirements

### TypeScript Types (MANDATORY)

Every component must have:
```typescript
interface ComponentNameProps {
  // All props with types
  // Use specific types, NOT any
  // Mark optional with ?
}

export default function ComponentName({ ...props }: ComponentNameProps) {
  // Implementation
}
```

### Accessibility Requirements:
- Semantic HTML (nav, main, article, aside, header, footer)
- ARIA labels where needed
- Keyboard navigation support
- Focus management
- Alt text for images
- Color contrast compliance

## Data Fetching Patterns

### Server Component Fetching:
```typescript
// app/jobs/page.tsx
async function getJobs(filters: JobFilters) {
  const res = await fetch(`${API_URL}/api/jobs?${params}`, {
    cache: 'no-store' // or 'force-cache' or revalidate
  })
  
  if (!res.ok) throw new Error('Failed to fetch jobs')
  return res.json()
}

export default async function JobsPage({ searchParams }) {
  const jobs = await getJobs(searchParams)
  
  return <JobList jobs={jobs} />
}
```

### API Client Pattern (lib/api.ts):
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function fetchJobs(params: JobFilters): Promise<Job[]> {
  const query = new URLSearchParams(params as any).toString()
  const res = await fetch(`${API_URL}/api/jobs?${query}`)
  
  if (!res.ok) {
    throw new Error(`API Error: ${res.status}`)
  }
  
  return res.json()
}
```

### Error Handling:
- Use error.tsx for error boundaries
- Use loading.tsx for loading states
- Handle API errors gracefully
- Show user-friendly messages
- Provide retry mechanisms

## Required Pages

### 1. Homepage (app/page.tsx)
- Hero section with search
- Featured jobs preview (3-6 cards)
- Call-to-action buttons
- Quick filters chips
- Link to full jobs page

### 2. Jobs List (app/jobs/page.tsx)
- Server Component that fetches jobs
- Grid layout (1 col mobile, 2 tablet, 3 desktop)
- FilterBar component (location, level, search)
- JobCard for each job
- Pagination or Load More
- Empty state ("No jobs found")
- Loading skeleton

### 3. Job Detail (app/jobs/[id]/page.tsx)
- Full job description
- Company info card (logo, name, description)
- Requirements list
- Salary and location
- Apply button
- Related jobs section (same company)
- Breadcrumb navigation

### 4. Companies List (app/companies/page.tsx)
- Grid of company cards
- Company logo, name, job count
- Link to company detail page
- Search/filter capability

### 5. Company Detail (app/companies/[id]/page.tsx)
- Company header (logo, name, website)
- About section
- All jobs from this company
- Company stats

## Required Components

### JobCard Component
**Must Display:**
- Company logo (next/image)
- Job title (heading)
- Company name (link)
- Location with icon
- Salary (if available)
- Level badge (color-coded)
- Created date (relative: "2 days ago")

**Design:**
- shadcn Card component
- Hover effect (shadow, scale)
- Click navigates to detail page
- Responsive sizing

### FilterBar Component
**Type:** Client Component ('use client')

**Must Include:**
- Location Select dropdown
- Level multi-select (checkboxes)
- Search Input (debounced)
- Clear filters button
- Active filters count badge

**Behavior:**
- Updates URL search params
- Debounce search input (500ms)
- Show loading state during filter
- Persist filters in URL

### ChatWidget Component
**Type:** Client Component
**Integration:** Communicates with /api/chat (OpenAI backend)

**Must Include:**
- Floating action button
- Dialog/Modal with chat interface
- Message bubbles (user + AI)
- Input with send button
- Typing indicator during streaming
- Job recommendation cards inline

## Styling Requirements

### Tailwind Usage (STRICT):
- Use utility classes ONLY
- No custom CSS files (except globals.css for resets)
- Use Tailwind config for theme
- Responsive prefixes: sm:, md:, lg:, xl:
- Dark mode support: dark:
- Group hover: group-hover:

### shadcn/ui Integration:
- Install components: `npx shadcn-ui@latest add button card input select badge`
- Use components/ui/* components
- Customize via Tailwind (not CSS)
- Use cn() helper for conditional classes

### Responsive Design (MANDATORY):
- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Grid layouts: 1 col → 2 col → 3 col
- Touch-friendly targets (min 44x44px)
- Readable font sizes (min 16px)

## TypeScript Types (lib/types.ts)

### Required Types (Match Backend):
```typescript
export enum JobLevel {
  JUNIOR = "junior",
  MIDDLE = "middle", 
  SENIOR = "senior",
  LEAD = "lead"
}

export interface Company {
  id: number
  name: string
  description?: string
  logo?: string
  website?: string
}

export interface Job {
  id: number
  title: string
  description: string
  location: string
  salary?: string
  level: JobLevel
  company_id: number
  created_at: string
  company: Company
}

export interface JobFilters {
  location?: string
  level?: JobLevel
  search?: string
  skip?: number
  limit?: number
}
```

## API Integration Pattern

### Backend API Contract:
```
GET http://localhost:8000/api/jobs
  Query params: location, level, search, skip, limit
  Response: Job[]

GET http://localhost:8000/api/jobs/:id
  Response: Job (with nested company)

GET http://localhost:8000/api/companies
  Response: Company[]

GET http://localhost:8000/api/companies/:id
  Response: Company (with nested jobs[])
```

## Anti-Patterns (NEVER DO)

### ❌ Forbidden:
- useEffect for data fetching in Server Components
- Fetching in Client Components (use props)
- Inline styles (style={{ }})
- Custom CSS files for components
- Raw HTML (div/span soup)
- Client Component by default
- Untyped props (any type)
- Missing error boundaries
- Non-responsive layouts
- Inaccessible components
- console.log in production
- Hardcoded API URLs
- Missing loading states

### ✅ Always Do:
- Server Components for pages
- Client Components only when needed
- Tailwind utilities for styling
- shadcn/ui for base components
- TypeScript strict mode
- Error handling everywhere
- Loading states for async
- Responsive design
- Semantic HTML
- Accessibility attributes

## Environment Variables

### Required in .env.local:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Output Format

### When Generating Components:
1. Show file path as comment
2. Indicate if Server or Client Component
3. Generate complete code with types
4. Include imports
5. Explain component purpose (1-2 sentences)
6. Suggest where to use it
7. Provide next step

### Example:
```
# src/components/JobCard.tsx

'use client' // if needed

[complete component code with types]

Component purpose: Displays job summary in card format with company info.
Usage: Import in app/jobs/page.tsx, map over jobs array.
Next step: "Create FilterBar client component for job filtering"
```

## Commit Message Format
```
feat(frontend): AI-generated [component/page]

[What was created]
[Key features]
Generated by: [Cursor/Windsurf/Claude]
```

## Completion Checklist

Frontend is complete when:
- [ ] All pages render (home, jobs, job detail, companies, company detail)
- [ ] All custom components working
- [ ] shadcn/ui components installed
- [ ] Filters work (location, level, search)
- [ ] Routing works (Link, navigation)
- [ ] API integration successful
- [ ] Responsive on all breakpoints
- [ ] Loading states implemented
- [ ] Error boundaries working
- [ ] TypeScript types defined
- [ ] Accessible (keyboard nav, ARIA)
- [ ] README with setup instructions