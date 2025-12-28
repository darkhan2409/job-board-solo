# Frontend Developer AI Rules

## Role
Frontend Engineer using Next.js 14 + React 18 + TypeScript + Tailwind CSS

## System Rules

### Code Generation Philosophy
- You are a **production frontend architect**, not a tutorial writer
- Generate **complete, runnable components** with zero placeholders
- Use **Server Components by default**, Client Components only when needed
- Follow **Next.js App Router** conventions strictly
- Code must be **type-safe** (no `any` types)
- Use **Tailwind CSS** for all styling (no custom CSS files)

### Technology Stack Mandate
- Next.js 14+ (App Router)
- React 18+
- TypeScript 5+
- Tailwind CSS 3+
- shadcn/ui for UI components
- Lucide React for icons

## Project Structure (MANDATORY)
```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx           # Root layout
│   │   ├── page.tsx             # Homepage
│   │   ├── jobs/                # Jobs pages
│   │   ├── companies/           # Companies pages
│   │   └── api/                 # API routes
│   ├── components/
│   │   ├── ui/                  # shadcn/ui components
│   │   └── ...                  # Custom components
│   └── lib/
│       ├── api.ts               # API client
│       ├── types.ts             # TypeScript types
│       └── utils.ts             # Utility functions
├── public/                      # Static assets
└── package.json
```

## Component Strategy

### Server Components (Default)
- All `page.tsx` files
- Fetch data directly with async/await
- Pass data as props to Client Components

### Client Components ('use client')
- Only when needed: forms, filters, state, event handlers
- Examples: FilterBar, ChatWidget, SearchBar

## Completion Checklist

Frontend is complete when:
- [ ] All pages render correctly
- [ ] Server Components fetch data
- [ ] Client Components handle interactivity
- [ ] Types match backend schemas
- [ ] Tailwind CSS styling applied
- [ ] shadcn/ui components integrated
- [ ] API client working
- [ ] Error handling implemented
- [ ] Responsive design working
