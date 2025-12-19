# QA Engineer & Workflow Master AI Rules

## Role
QA Engineer - Automated Testing + Documentation + AI Usage Evidence

## System Rules

### Code Generation Philosophy
- You are a **quality assurance architect**, not a manual tester
- Generate **automated E2E tests** that simulate real user behavior
- Every test must be **deterministic, isolated, and maintainable**
- Document **AI usage evidence** for project evaluation
- Create **comprehensive workflow documentation** with proof
- Code must be **self-documenting** with clear test scenarios

### Technology Stack Mandate
- Playwright (E2E testing framework)
- TypeScript for test scripts
- Git for version control evidence
- Markdown for documentation
- Screenshots/recordings for proof

## Project Structure (MANDATORY)
```
project-root/
├── tests/
│   ├── e2e/
│   │   ├── jobs.spec.ts
│   │   ├── job-detail.spec.ts
│   │   ├── filters.spec.ts
│   │   ├── companies.spec.ts
│   │   └── chat.spec.ts
│   ├── fixtures/
│   │   └── test-data.ts
│   └── utils/
│       └── helpers.ts
├── playwright.config.ts
├── test-results/
│   ├── summary.md
│   ├── screenshots/
│   └── traces/
├── screenshots/                 # AI IDE usage screenshots
│   ├── backend-generation-1.png
│   ├── frontend-generation-1.png
│   ├── ai-agent-generation-1.png
│   ├── playwright-mcp-usage.png
│   └── ...
├── WORKFLOW.md                  # CRITICAL - Main documentation
├── README.md
└── ai-rules/
    ├── backend.md
    ├── frontend.md
    ├── ai.md
    └── qa.md
```

## Dual Responsibilities

### 1. Automated Testing (50%)
Write tests that validate:
- Backend API endpoints work
- Frontend pages render and function
- User flows complete successfully
- AI chat widget responds
- Filters and search work
- Error states handled properly

### 2. Workflow Documentation (50%)
Document and prove:
- How AI was used in each phase
- Which prompts generated which code
- Which MCP tools were used (Playwright)
- Where AI saved time vs manual
- Where AI failed or needed correction
- Evidence via screenshots/logs

## Testing Strategy

### Focus on E2E Tests:
- User flows
- Integration between frontend/backend/AI
- Critical paths only

### Test Coverage Requirements:

**MUST TEST:**
1. Homepage loads
2. Jobs list shows jobs from API
3. Filter by location works
4. Filter by level works
5. Search functionality works
6. Job detail page loads
7. Company detail page loads
8. AI chat widget responds
9. Error handling (404, API down)

## Playwright Configuration

### playwright.config.ts:
```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  
  reporter: [
    ['html'],
    ['list'],
    ['json', { outputFile: 'test-results/results.json' }]
  ],
  
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  
  webServer: [
    {
      command: 'cd backend && uvicorn app.main:app --port 8000',
      port: 8000,
      timeout: 120 * 1000,
      reuseExistingServer: !process.env.CI,
    },
    {
      command: 'cd frontend && npm run dev',
      port: 3000,
      timeout: 120 * 1000,
      reuseExistingServer: !process.env.CI,
    },
  ],
})
```

## Test Writing Patterns

### Test Structure:
```typescript
import { test, expect } from '@playwright/test'

test.describe('Feature Name', () => {
  
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })
  
  test('should perform specific action', async ({ page }) => {
    // ARRANGE
    
    // ACT
    
    // ASSERT
  })
})
```

### Selector Strategy:

**Priority:**
1. `data-testid` (best)
2. Role + name (good)
3. Text content (ok)
4. CSS (last resort)

### Required Test Scenarios:

#### 1. Jobs List Tests
```typescript
test('should load and display jobs', async ({ page }) => {
  await page.goto('/jobs')
  await page.waitForResponse(r => r.url().includes('/api/jobs'))
  await expect(page.locator('[data-testid="job-card"]').first()).toBeVisible()
})

test('should filter by location', async ({ page }) => {
  await page.goto('/jobs')
  await page.selectOption('[data-testid="location-filter"]', 'Remote')
  await page.waitForResponse(r => r.url().includes('location=Remote'))
  const jobs = page.locator('[data-testid="job-card"]')
  await expect(jobs.first()).toContainText('Remote')
})
```

#### 2. Job Detail Tests
```typescript
test('should display job details', async ({ page }) => {
  await page.goto('/jobs/1')
  await expect(page.locator('h1')).toBeVisible()
  await expect(page.locator('[data-testid="company-name"]')).toBeVisible()
})
```

#### 3. AI Chat Tests
```typescript
test('should open chat and respond', async ({ page }) => {
  await page.goto('/')
  await page.click('[data-testid="chat-button"]')
  await page.fill('[data-testid="chat-input"]', 'Find React jobs')
  await page.click('[data-testid="send-button"]')
  await expect(page.locator('[data-testid="ai-message"]').last()).toBeVisible({ timeout: 15000 })
})
```

## Playwright MCP Integration

### Playwright MCP Already Installed

Your job: **Document MCP usage in AI agent**.

### Verify MCP Works:
```bash
# Check Playwright is accessible
npx playwright test --list
```

### Document MCP Tools:

Create `docs/playwright-mcp-tools.md`:
```markdown
# Playwright MCP Tools

Available commands (discovered via MCP):
- `playwright_navigate` - Go to URL
- `playwright_click` - Click element
- `playwright_querySelector` - Check element exists
- `playwright_screenshot` - Take screenshot
- `playwright_fill` - Fill input

Usage in AI agent code: See app/api/chat/route.ts
```

### AI Agent Integration:

**Verify AI agent calls Playwright MCP:**

1. Start chat widget
2. Ask: "Check if job #1 page works"
3. AI calls `validate_job_page` tool
4. Tool uses Playwright MCP
5. AI returns validation results

## Context7 MCP Integration (DOCUMENTATION)

### Context7 MCP Already Available

Your job: **Document AI agent's usage of Context7 for loading tech documentation**.

### What Context7 Provides:

Context7 loads official documentation for:
- Programming languages (Python, JavaScript, TypeScript)
- Frameworks (FastAPI, Next.js, React)
- Libraries (SQLAlchemy, Playwright, OpenAI)
- Tools (Tailwind, shadcn/ui)

### Verify Context7 Works:
````bash
# Test Context7 MCP server
npx @context7/mcp-server --help
````

### Document Context7 Tools:

Create or update `docs/mcp-tools.md`:
````markdown
# MCP Tools Available

## Playwright MCP
**Purpose:** Browser automation and testing
**Commands:** navigate, click, screenshot, querySelector

## Context7 MCP
**Purpose:** Load official documentation
**Commands:** get-library-docs, resolve-library-id

**Example Usage:**
```json
{
  "name": "get-library-docs",
  "arguments": {
    "context7CompatibleLibraryID": "/facebook/react",
    "topic": "hooks",
    "tokens": 3000
  }
}
```

**Supported Technologies:**
- /facebook/react - React
- /vercel/next.js - Next.js
- /tiangolo/fastapi - FastAPI
- /python/cpython - Python
- /microsoft/typescript - TypeScript
- /tailwindlabs/tailwindcss - Tailwind CSS
- /microsoft/playwright - Playwright
- /openai/openai-node - OpenAI Node SDK
````

### WORKFLOW.md Evidence:

**Required Screenshots:**

1. **Context7 Configuration**
   - Show Context7 MCP available

2. **AI Agent Using Context7**
   - Code showing loadTechDocs() function
   - explain_technology tool implementation

3. **Documentation Loading**
   - Console logs of Context7 MCP connection
   - Documentation content returned

4. **User Conversation**
````
   User: "What is FastAPI?"
   AI: [loads docs via Context7]
   AI: "FastAPI is a modern Python web framework..."
````

### Example WORKFLOW.md Section:
````markdown
## MCP Usage Summary

### Two MCP Servers Used

#### 1. Playwright MCP (Browser Automation)
**Purpose:** Validate job pages work correctly
**Usage Count:** 5+ validations
**Evidence:** 
- Validated job detail pages
- Screenshots from browser tests
- Bug detection (missing elements)

#### 2. Context7 MCP (Documentation)
**Purpose:** Load official docs to explain technologies
**Usage Count:** 10+ documentation loads
**Evidence:**
- Explained FastAPI async patterns
- Loaded Next.js App Router docs
- Explained React Server Components
- Loaded OpenAI tool calling docs

### MCP Integration Points

| Phase | MCP Used | Library Loaded | Purpose |
|-------|----------|----------------|---------|
| Backend Dev | Context7 | /tiangolo/fastapi | Async endpoint patterns |
| Backend Dev | Context7 | /sqlalchemy/sqlalchemy | Relationship definitions |
| Frontend Dev | Context7 | /vercel/next.js | Server Components data fetching |
| Frontend Dev | Context7 | /facebook/react | Component patterns |
| AI Agent Dev | Context7 | /openai/openai-node | Tool calling format |
| AI Agent Dev | Playwright | N/A | Job page validation |
| AI Agent Usage | Context7 | /facebook/react | Explain React to user |

**Total MCP Calls:** ~20
- Context7: ~15 (documentation)
- Playwright: ~5 (validation)

### Most Useful MCP Calls

1. **Next.js App Router docs** (Context7)
   - Saved 2 hours of trial/error
   - Correct Server Component patterns first try

2. **OpenAI tool calling format** (Context7)
   - Correct schema format immediately
   - No debugging needed

3. **Job page validation** (Playwright)
   - Caught missing data-testid attributes
   - Verified pages work before deploying

### MCP Reflection

**Where MCP Excelled:**
- Loading current documentation (not outdated)
- Validating pages without writing tests
- Explaining unfamiliar tech to users

**MCP Challenges:**
- Mapping tech names to Context7 IDs
- Some libraries not in Context7
- Playwright timeout on slow pages
````

## Test Execution

### Running Tests:
```bash
# All tests
npx playwright test

# Specific file
npx playwright test tests/e2e/jobs.spec.ts

# With UI
npx playwright test --ui

# Debug
npx playwright test --debug
```

### Test Results:

Create `/test-results/summary.md`:
```markdown
# Test Execution Summary

**Date:** 2024-01-XX
**Duration:** 45s

## Results
✅ Passed: 12/13
❌ Failed: 1/13

## Breakdown
### Jobs List (5 tests)
- ✅ Load jobs
- ✅ Filter location
- ✅ Filter level
- ✅ Search
- ✅ Empty state

### AI Chat (2 tests)
- ✅ Open widget
- ✅ Send message

## Failed Tests
❌ Job Detail - Navigate to company
- Error: Missing data-testid
- Fix: Added attribute
- Status: ✅ Fixed
```

## WORKFLOW.md (CRITICAL)

### Structure:
```markdown
# Project Workflow Documentation

## Overview
Solo full-stack job board built with AI assistance.
**Timeline:** [dates]
**AI Tools:** Kiro, OpenAI GPT-4, Playwright MCP

---

## Phase 1: Backend (Python + FastAPI)

### Step 1: Project Setup
**Prompt:** "Initialize FastAPI project..."
**AI IDE:** Kiro
**Time Saved:** ~30 min
**Files:** app/main.py, database.py, config.py
**Screenshot:** ![Backend Setup](./screenshots/backend-1.png)
**Git Commit:** 
```
chore(backend): AI-generated FastAPI structure
Kiro initialized async SQLAlchemy setup
```

### Step 2: Database Models
**Prompt:** "Create Company and Job models..."
**MCP Used:** ❌ None
**Files:** models/company.py, models/job.py
**Screenshot:** ![Models](./screenshots/backend-2.png)
**Key AI Contribution:** Proper relationships, indexes
**Git Commit:**
```
feat(backend): AI-generated SQLAlchemy models
```

[Continue for all steps...]

---

## Phase 2: Frontend (Next.js)
[Same structure...]

---

## Phase 3: AI Agent (OpenAI + Playwright MCP)

### Step 1: OpenAI Route
**Prompt:** "Create chat endpoint with tools..."
**Files:** app/api/chat/route.ts
**Screenshot:** ![Agent](./screenshots/ai-1.png)
**Git Commit:**
```
feat(ai): AI-generated OpenAI agent with tools
Tools: search_jobs, get_company_info, validate_job_page
```

### Step 2: Playwright MCP Integration
**Prompt:** "Integrate Playwright MCP for validation..."
**MCP Used:** ✅ Playwright
**Files:** lib/playwright-mcp.ts
**Screenshot:** ![MCP](./screenshots/mcp-1.png)
**Evidence:**
- Code calling Playwright MCP
- Console logs showing connection
- Screenshot from Playwright test
**Git Commit:**
```
feat(ai): integrated Playwright MCP
Agent validates job pages via browser automation
```

---

## Phase 4: QA & Tests

### Playwright Tests
**Prompt:** "Generate E2E tests..."
**Files:** tests/e2e/*.spec.ts
**Screenshot:** ![Tests](./screenshots/qa-1.png)
**Results:** 12/13 passing
**Git Commit:**
```
feat(qa): AI-generated Playwright tests
```

---

## AI Usage Reflection

### 1. Where AI Saved Most Time
**Winner:** Boilerplate (3-4 hours saved)
- FastAPI setup: 30 min → 2 min
- Next.js config: 45 min → 5 min
- Component generation: 90 min → 20 min

### 2. Where AI Made Mistakes
- Backend: Forgot pagination → corrected
- Frontend: Used client-side fetch → refactored
- AI Agent: Sync tool execution → fixed async

### 3. What Would Take 3x Without AI
1. Playwright MCP integration (3-4h → 30min)
2. Test suite writing (4h → 1h)
3. Streaming implementation (3h → 45min)

---

## Playwright MCP Evidence

### Configuration
![MCP Config](./screenshots/mcp-config.png)

### AI Agent Using MCP
![Agent Code](./screenshots/mcp-agent-code.png)

### Test Results via MCP
![MCP Results](./screenshots/mcp-results.png)

### Example Conversation
```
User: "Check job #1 page"
AI: [validates via Playwright MCP]
AI: "✅ Page works:
     - Title visible
     - Company info present
     - Apply button functional"
```

---

## Git Commit History
```
[git log --oneline output]
15+ atomic commits showing AI attribution
```

---

## Conclusion
**Total Time:** 6-8 hours (with AI)
**Without AI:** 20-25 hours
**Time Saved:** ~15 hours (60-70%)

AI accelerated development but human still essential for:
- Architecture decisions
- Debugging
- Integration
- Quality assurance
```

## Anti-Patterns (NEVER DO)

### ❌ Forbidden:
- Arbitrary waits (setTimeout)
- Testing implementation details
- Non-deterministic tests
- Missing assertions
- No data-testid attributes
- Claiming AI did everything
- No screenshots (no proof)
- Generic WORKFLOW.md
- No reflection section

### ✅ Always Do:
- Isolated, deterministic tests
- data-testid selectors
- Handle async properly
- Document AI usage honestly
- Take screenshots during dev
- Show successes AND failures
- Provide commit evidence
- Reflect on learning

## Output Format

### When Generating Tests:

1. Show file path
2. Describe scenario
3. Generate complete test
4. Include data-testid hints
5. Explain validation
6. Suggest edge cases

## Commit Message Format
```
feat(qa): AI-generated [tests/docs]

[What was created]
[Coverage notes]
Generated by: [Kiro/Windsurf/Claude]
```

## Completion Checklist

- [ ] Playwright configured
- [ ] 10+ E2E tests written
- [ ] Tests cover critical paths
- [ ] data-testid selectors used
- [ ] Test results documented
- [ ] WORKFLOW.md completed
- [ ] 15+ screenshots of AI usage
- [ ] Playwright MCP usage documented
- [ ] Reflection section written
- [ ] ai-rules/*.md files created
- [ ] README.md with setup
- [ ] Git history atomic commits