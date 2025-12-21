# 🚀 Job Board Solo - Full-Stack приложение с AI

> Full-stack job board с AI агентом, интеграцией MCP серверов и E2E тестами

[![GitHub](https://img.shields.io/badge/GitHub-darkhan2409-blue)](https://github.com/darkhan2409/job-board-solo)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-12-black)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue)](https://www.typescriptlang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-teal)](https://fastapi.tiangolo.com/)

## 📋 Описание

Job Board Solo - это современное приложение для поиска работы с интеграцией AI ассистента. Проект демонстрирует:

- ✅ **Full-stack разработку** (FastAPI + Next.js)
- ✅ **AI интеграцию** (OpenAI GPT-4 Turbo)
- ✅ **MCP серверы** (Context7 + Playwright)
- ✅ **E2E тестирование** (Playwright)
- ✅ **Type-safe код** (TypeScript + Pydantic)
- ✅ **Современный UI** (Tailwind CSS + shadcn/ui)

## 🎯 Основные возможности

### Для пользователей
- 🔍 Поиск вакансий с фильтрами (локация, уровень, ключевые слова)
- 🏢 Просмотр компаний и их вакансий
- 🤖 AI ассистент для помощи в поиске работы
- 📚 Объяснение технологий через официальную документацию
- ✅ Валидация страниц через браузерную автоматизацию

### Технические
- 🚀 Server-Side Rendering (Next.js App Router)
- ⚡ Async API (FastAPI + SQLAlchemy)
- 🎨 Responsive дизайн (Mobile-first)
- 🧪 33 E2E теста (Playwright)
- 📝 Type-safe везде (TypeScript + Pydantic V2)

## 🛠️ Технологический стек

### Backend
```
FastAPI 0.104.1      - Web framework
SQLAlchemy 2.0.23    - ORM (async)
Pydantic V2          - Validation
SQLite               - Database
Uvicorn              - ASGI server
```

### Frontend
```
Next.js 12.3.4       - React framework
React 18.2.0         - UI library
TypeScript 5.3.3     - Type safety
Tailwind CSS 3.3.6   - Styling
shadcn/ui            - UI components
Lucide React         - Icons
```

### AI & MCP
```
OpenAI GPT-4 Turbo   - AI model
Context7 MCP         - Documentation
Playwright MCP       - Browser automation
```

### Testing
```
Playwright 1.40.1    - E2E testing
```

## 📦 Установка и запуск

### Требования

- Python 3.11+
- Node.js 16+
- npm или yarn
- OpenAI API key (для AI агента)

### 1. Клонировать репозиторий

```bash
git clone https://github.com/darkhan2409/job-board-solo.git
cd job-board-solo
```

### 2. Backend

```bash
cd backend

# Создать виртуальное окружение
python -m venv venv

# Активировать (Windows)
venv\Scripts\activate

# Активировать (Linux/Mac)
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Заполнить БД тестовыми данными
python seed_data.py

# Запустить сервер
uvicorn app.main:app --reload
```

Backend будет доступен на http://localhost:8000  
API документация: http://localhost:8000/docs

### 3. Frontend

```bash
cd frontend

# Установить зависимости
npm install

# Создать .env.local
cp .env.local.example .env.local

# Добавить OpenAI API ключ в .env.local
# OPENAI_API_KEY=sk-...

# Запустить dev server
npm run dev
```

Frontend будет доступен на http://localhost:3000

### 4. E2E тесты (опционально)

```bash
# Из корня проекта
npm install

# Установить браузеры
npx playwright install

# Запустить тесты
npm run test:e2e

# UI mode (интерактивный)
npm run test:e2e:ui

# Посмотреть отчет
npm run test:e2e:report
```

## 🎮 Использование

### Поиск вакансий

1. Откройте http://localhost:3000
2. Перейдите на страницу "Jobs"
3. Используйте фильтры:
   - Поиск по ключевым словам
   - Фильтр по локации
   - Фильтр по уровню (junior/middle/senior/lead)

### AI ассистент

1. Кликните на кнопку чата (bottom-right)
2. Попробуйте команды:
   - "Найди мне удаленные React вакансии"
   - "Что такое Next.js?"
   - "Расскажи о компании TechCorp"
   - "Проверь страницу вакансии 5"

### API

Backend API доступен на http://localhost:8000/api

**Endpoints:**
```
GET    /api/jobs              - Список вакансий
GET    /api/jobs/{id}         - Детали вакансии
POST   /api/jobs              - Создать вакансию
PUT    /api/jobs/{id}         - Обновить вакансию
DELETE /api/jobs/{id}         - Удалить вакансию
GET    /api/companies         - Список компаний
GET    /api/companies/{id}    - Детали компании
POST   /api/companies         - Создать компанию
```

**Фильтры для /api/jobs:**
- `search` - Поиск по title/description
- `location` - Фильтр по локации
- `level` - Фильтр по уровню (junior/middle/senior/lead)
- `skip` - Пагинация (offset)
- `limit` - Количество результатов

## 🤖 AI Tools

AI ассистент имеет доступ к 4 инструментам:

### 1. search_jobs
Поиск вакансий через backend API
```typescript
{
  search: "React",
  location: "Remote",
  level: "senior",
  limit: 5
}
```

### 2. get_company_info
Информация о компании и её вакансиях
```typescript
{
  company_id: 1
}
```

### 3. validate_job_page (Playwright MCP)
Валидация страницы вакансии через браузер
```typescript
{
  job_id: 5
}
```

### 4. explain_technology (Context7 MCP)
Объяснение технологий через официальную документацию
```typescript
{
  technology: "Next.js",
  topic: "routing" // опционально
}
```

**Поддерживаемые технологии:**
React, Next.js, FastAPI, Python, TypeScript, Node.js, Docker, Kubernetes, PostgreSQL, MongoDB, Redis, Tailwind CSS

## 📊 Структура проекта

```
job-board-solo/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── models/         # SQLAlchemy модели
│   │   ├── schemas/        # Pydantic схемы
│   │   ├── routes/         # API endpoints
│   │   ├── services/       # Бизнес-логика
│   │   └── utils/          # Утилиты
│   ├── requirements.txt
│   └── seed_data.py        # Заполнение БД
│
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # Pages (App Router)
│   │   ├── components/    # React компоненты
│   │   └── lib/           # Утилиты и API client
│   ├── package.json
│   └── MCP_INTEGRATION.md # MCP документация
│
├── tests/                 # E2E тесты
│   └── e2e/
│       ├── homepage.spec.ts
│       ├── jobs.spec.ts
│       ├── job-detail.spec.ts
│       ├── companies.spec.ts
│       └── chat.spec.ts
│
├── playwright.config.ts   # Playwright конфигурация
├── WORKFLOW.md           # Полная документация процесса
└── README.md             # Этот файл
```

## 🧪 Тестирование

### E2E тесты

**33 теста** покрывают:
- ✅ Homepage navigation
- ✅ Jobs list и фильтры
- ✅ Job detail page
- ✅ Companies pages
- ✅ Chat widget UI

**Запуск:**
```bash
npm run test:e2e           # Запустить все тесты
npm run test:e2e:ui        # UI mode (интерактивный)
npm run test:e2e:report    # Посмотреть отчет
```

### Ручное тестирование

1. **Backend API:**
   - Откройте http://localhost:8000/docs
   - Протестируйте endpoints через Swagger UI

2. **Frontend:**
   - Откройте http://localhost:3000
   - Проверьте все страницы
   - Протестируйте фильтры
   - Попробуйте AI ассистента

## 📚 Документация

- **[WORKFLOW.md](WORKFLOW.md)** - Полная документация процесса разработки
- **[MCP_INTEGRATION.md](frontend/MCP_INTEGRATION.md)** - Документация MCP интеграции
- **[Backend README](backend/README.md)** - Backend инструкции
- **[Frontend README](frontend/README.md)** - Frontend инструкции

## 🎯 Roadmap

### Реализовано ✅
- [x] Backend API (FastAPI + SQLAlchemy)
- [x] Frontend (Next.js + React)
- [x] AI агент (OpenAI GPT-4)
- [x] MCP интеграция (Context7 + Playwright)
- [x] E2E тесты (Playwright)
- [x] Документация

### Планы 🚧
- [ ] User authentication
- [ ] Real-time MCP integration
- [ ] Unit тесты для backend
- [ ] Deployment (Vercel + Railway)
- [ ] Performance optimization
- [ ] More AI tools

## 🤝 Вклад

Проект создан как solo демонстрация, но pull requests приветствуются!

1. Fork репозиторий
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📝 Лицензия

MIT License - см. [LICENSE](LICENSE)

## 👤 Автор

**darkhan2409**
- GitHub: [@darkhan2409](https://github.com/darkhan2409)
- Репозиторий: [job-board-solo](https://github.com/darkhan2409/job-board-solo)

## 🙏 Благодарности

- **Kiro AI** - AI ассистент для разработки
- **OpenAI** - GPT-4 Turbo model
- **Context7** - MCP сервер для документации
- **Playwright** - MCP сервер для браузерной автоматизации
- **FastAPI** - Отличный Python framework
- **Next.js** - Мощный React framework
- **shadcn/ui** - Красивые UI компоненты

---

**⭐ Если проект понравился, поставьте звезду на GitHub!**

**📧 Вопросы? Создайте issue в репозитории.**

---

Сделано с ❤️ и AI в 2025
