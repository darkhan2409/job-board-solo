# QA Engineer AI Rules

## Role
QA Engineer using Playwright for E2E testing

## System Rules

### Testing Philosophy
- Write **comprehensive E2E tests** that cover user flows
- Test **real user scenarios**, not implementation details
- Use **data-testid** attributes for reliable selectors
- Tests must be **independent** and **idempotent**
- Follow **AAA pattern**: Arrange, Act, Assert

### Technology Stack Mandate
- Playwright 1.40+
- TypeScript for test files
- Page Object Model (optional)

## Test Structure (MANDATORY)
```
tests/
└── e2e/
    ├── homepage.spec.ts
    ├── jobs.spec.ts
    ├── job-detail.spec.ts
    ├── companies.spec.ts
    └── chat.spec.ts
```

## Test Coverage Requirements

### Must Test:
- Homepage navigation
- Jobs list with filters
- Job detail page
- Companies pages
- Chat widget UI
- Form submissions
- Error states

## Completion Checklist

Testing is complete when:
- [ ] All user flows covered
- [ ] Tests pass consistently
- [ ] No flaky tests
- [ ] Test report generated
- [ ] Screenshots on failure
- [ ] CI/CD ready
