# Job Board Frontend

Next.js 12 frontend for job board application with TypeScript, Tailwind CSS, and shadcn/ui.

## Tech Stack

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **UI Components:** shadcn/ui
- **Icons:** Lucide React

## Setup

### 1. Install dependencies

```bash
npm install
```

### 2. Configure environment

```bash
cp .env.local.example .env.local
# Edit .env.local with your settings
```

### 3. Run development server

```bash
npm run dev
```

### 4. Open browser

Navigate to http://localhost:3000

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx           # Root layout
│   │   ├── page.tsx             # Homepage
│   │   ├── jobs/                # Jobs pages
│   │   ├── companies/           # Companies pages
│   │   └── api/                 # API routes (AI chat)
│   ├── components/
│   │   ├── ui/                  # shadcn/ui components
│   │   └── ...                  # Custom components
│   └── lib/
│       ├── api.ts               # API client
│       ├── types.ts             # TypeScript types
│       └── utils.ts             # Utility functions
├── public/                      # Static assets
├── tailwind.config.ts
├── next.config.js
└── package.json
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## Features

- Server-side rendering with Next.js App Router
- Type-safe API calls with TypeScript
- Responsive design with Tailwind CSS
- Accessible UI components from shadcn/ui
- AI-powered job search assistant

## Development

Generated with AI assistance using Kiro.
