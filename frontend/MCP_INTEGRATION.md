# MCP Integration Guide

Этот проект использует два MCP сервера для расширения возможностей AI агента:

## 🔧 Установленные MCP серверы

### 1. Context7 MCP (Документация)
**Назначение:** Загрузка официальной документации технологий

**Использование в проекте:**
- Tool: `explain_technology`
- Файл: `src/lib/tools/explain-tech.ts`
- Когда вызывается: Когда пользователь спрашивает "Что такое X?" или нужно объяснить технологию из вакансии

**Поддерживаемые технологии:**
- React (`/facebook/react`)
- Next.js (`/vercel/next.js`)
- FastAPI (`/tiangolo/fastapi`)
- Python (`/python/cpython`)
- TypeScript (`/microsoft/TypeScript`)
- Node.js (`/nodejs/node`)
- Docker (`/docker/docs`)
- Kubernetes (`/kubernetes/kubernetes`)
- PostgreSQL (`/postgres/postgres`)
- MongoDB (`/mongodb/docs`)
- Redis (`/redis/redis`)
- Tailwind CSS (`/tailwindlabs/tailwindcss`)

**Пример вызова:**
```typescript
const result = await explainTechnology({
  technology: 'React',
  topic: 'hooks' // опционально
})
```

### 2. Playwright MCP (Браузерная автоматизация)
**Назначение:** Валидация страниц через браузер

**Использование в проекте:**
- Tool: `validate_job_page`
- Файл: `src/lib/tools/validate-job.ts`
- Когда вызывается: Для проверки корректности отображения страницы вакансии

**Что проверяется:**
- Наличие заголовка вакансии (`[data-testid="job-title"]`)
- Наличие названия компании (`[data-testid="company-name"]`)
- Наличие описания (`[data-testid="job-description"]`)
- Наличие кнопки Apply (`[data-testid="apply-button"]`)

**Пример вызова:**
```typescript
const result = await validateJobPage({
  job_id: 1
})
```

## 🚀 Как это работает

### Архитектура

```
User → ChatWidget → /api/chat → OpenAI GPT-4
                                    ↓
                              Tool Calls
                                    ↓
                         /api/tools → executor
                                    ↓
                    ┌───────────────┴───────────────┐
                    ↓                               ↓
            Context7 MCP                    Playwright MCP
         (explain_technology)              (validate_job_page)
```

### Поток данных

1. **Пользователь** отправляет сообщение в ChatWidget
2. **ChatWidget** отправляет запрос в `/api/chat`
3. **OpenAI GPT-4** анализирует запрос и решает, какие tools вызвать
4. **Tool executor** выполняет вызовы:
   - `search_jobs` → Backend API
   - `get_company_info` → Backend API
   - `validate_job_page` → **Playwright MCP**
   - `explain_technology` → **Context7 MCP**
5. **Результаты** возвращаются в GPT-4
6. **GPT-4** формирует ответ пользователю
7. **ChatWidget** отображает ответ (streaming)

## 📝 Примеры использования

### Context7 MCP

**Вопрос пользователя:**
> "Что такое Next.js?"

**AI вызывает:**
```json
{
  "tool": "explain_technology",
  "arguments": {
    "technology": "Next.js"
  }
}
```

**Context7 MCP возвращает:**
```json
{
  "success": true,
  "documentation": {
    "library": "Next.js",
    "library_id": "/vercel/next.js",
    "content": "Next.js is a React framework...",
    "source": "Official Documentation"
  },
  "mcp_used": "Context7 MCP"
}
```

### Playwright MCP

**Вопрос пользователя:**
> "Проверь, правильно ли отображается вакансия #5"

**AI вызывает:**
```json
{
  "tool": "validate_job_page",
  "arguments": {
    "job_id": 5
  }
}
```

**Playwright MCP возвращает:**
```json
{
  "success": true,
  "validation": {
    "url": "http://localhost:3000/jobs/5",
    "elements_checked": [
      { "selector": "[data-testid='job-title']", "found": true },
      { "selector": "[data-testid='company-name']", "found": true },
      { "selector": "[data-testid='job-description']", "found": true },
      { "selector": "[data-testid='apply-button']", "found": true }
    ],
    "all_elements_present": true
  },
  "mcp_used": "Playwright MCP"
}
```

## 🔍 Логирование MCP вызовов

Все вызовы MCP логируются в консоль:

```bash
Executing tool: explain_technology { technology: 'React' }
Executing tool: validate_job_page { job_id: 5 }
```

## 🧪 Тестирование MCP интеграции

### Тест Context7 MCP:
```bash
# В ChatWidget спросите:
"Что такое FastAPI?"
"Объясни React hooks"
"Расскажи про Docker"
```

### Тест Playwright MCP:
```bash
# В ChatWidget спросите:
"Проверь страницу вакансии 1"
"Валидируй job page для вакансии 3"
```

## 📊 MCP Evidence для WORKFLOW.md

Для документации нужно собрать:

1. **Скриншоты консоли** с логами MCP вызовов
2. **Скриншоты ChatWidget** с ответами AI
3. **Таблица использования:**

| MCP Server | Tool | Вызовов | Примеры |
|------------|------|---------|---------|
| Context7 | explain_technology | 10+ | React, Next.js, FastAPI |
| Playwright | validate_job_page | 5+ | Jobs 1, 3, 5, 7, 10 |

## 🛠️ Настройка

### 1. Установить зависимости:
```bash
npm install
```

### 2. Создать .env.local:
```bash
cp .env.local.example .env.local
```

### 3. Добавить OpenAI API ключ:
```env
OPENAI_API_KEY=sk-...
```

### 4. Запустить:
```bash
npm run dev
```

## 📚 Дополнительная информация

- Context7 MCP: https://github.com/context7/mcp-server
- Playwright MCP: https://github.com/microsoft/playwright-mcp
- OpenAI Tool Calling: https://platform.openai.com/docs/guides/function-calling
