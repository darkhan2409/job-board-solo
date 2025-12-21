# Validation Scripts

This directory contains validation scripts for the AI Evidence Collection feature. These scripts verify that all evidence requirements are met for the Job Board Solo project.

## Available Scripts

### 1. Screenshot Validator
**Command:** `npm run check:screenshots`

**Purpose:** Validates screenshot evidence collection

**Checks:**
- Screenshot count >= 15
- Naming convention: `{phase}-{description}-{number}.{ext}`
- Valid phases: backend, frontend, aiagent, mcp, runtime, qa
- Valid extensions: .png, .jpg, .jpeg
- Distribution across phases

**Example Output:**
```
✅ Valid Screenshots by Phase:
   backend: 4 screenshots
   frontend: 5 screenshots
   mcp: 4 screenshots
   runtime: 5 screenshots

📋 Requirements Check:
   Screenshot count: 18/15 ✅
   Backend screenshots: 4/4 ✅
   Frontend screenshots: 5/5 ✅
```

### 2. Documentation Validator
**Command:** `npm run validate:documentation`

**Purpose:** Validates WORKFLOW.md completeness and quality

**Checks:**
- WORKFLOW.md exists
- Required sections present (Overview, Backend, Frontend, AI Agent, MCP, Testing, Evidence)
- Screenshot references (minimum 10)
- MCP documentation (Playwright: 5+, Context7: 10+)
- Test documentation
- Reflection section
- Relative paths usage

**Example Output:**
```
✅ WORKFLOW.md Exists: WORKFLOW.md found
✅ Required Sections: All required sections present
✅ Screenshot References: 15 screenshots referenced (minimum: 10)
✅ MCP Documentation: Playwright: 6/5, Context7: 12/10, Table: ✓
```

### 3. Git History Validator
**Command:** `npm run validate:git`

**Purpose:** Validates git commit history and attribution

**Checks:**
- Git repository exists
- Commit count >= 15
- AI attribution in commits (minimum 5)
- Atomic commits (no generic messages)
- MCP mentions in commits (minimum 2)

**Example Output:**
```
✅ Git Repository: Git repository found
✅ Commit Count: Found 23 commits (minimum: 15)
✅ AI Attribution: 8 commits with AI attribution (34.8%)
✅ Atomic Commits: Commits appear to be atomic
✅ MCP Commits: 3 commits mention MCP (minimum: 2)

📝 Recent Commits:
   a1b2c3d - Add Context7 MCP integration [AI]
   e4f5g6h - Implement Playwright MCP validation [Kiro]
   i7j8k9l - Create chat widget component
```

### 4. Main Evidence Validator
**Command:** `npm run validate:evidence`

**Purpose:** Comprehensive evidence validation (runs all checks)

**Checks:**
- Screenshot count and naming
- Test results existence
- MCP evidence count
- WORKFLOW.md completeness
- Git history
- Cross-references between WORKFLOW.md and screenshots

**Example Output:**
```
📊 VALIDATION REPORT
============================================================
Timestamp: 2024-01-15T10:30:00.000Z
Status: ✅ PASS

Summary: 7/7 checks passed

✅ Screenshot Count: Found 18 screenshots (minimum: 15)
✅ Screenshot Naming: All screenshots follow naming convention
✅ Test Results: Test summary exists
✅ MCP Evidence: Playwright: 6/5, Context7: 12/10
✅ WORKFLOW.md: WORKFLOW.md contains required sections
✅ Git History: Found 23 commits (minimum: 15)
✅ Cross-References: All 15 referenced images exist
```

### 5. Run All Validators
**Command:** `npm run validate:all`

**Purpose:** Runs all validation scripts in sequence

This command executes:
1. `npm run check:screenshots`
2. `npm run validate:documentation`
3. `npm run validate:git`
4. `npm run validate:evidence`

If any validator fails, the command stops and reports the failure.

## Usage

### Quick Validation
To quickly check if all evidence requirements are met:
```bash
npm run validate:all
```

### Individual Validators
To run specific validators:
```bash
# Check screenshots only
npm run check:screenshots

# Check documentation only
npm run validate:documentation

# Check git history only
npm run validate:git

# Run comprehensive evidence check
npm run validate:evidence
```

## Exit Codes

All validators follow standard exit code conventions:
- `0` - All checks passed
- `1` - One or more checks failed

This allows integration with CI/CD pipelines:
```bash
npm run validate:all && echo "Ready for submission!" || echo "Fix issues first"
```

## Validation Properties

These validators implement the correctness properties defined in the design document:

### Property 1: Screenshot Count Sufficiency
*For any* evidence collection, the screenshots directory should contain at least 15 screenshot files with valid image extensions (.png, .jpg, .jpeg)

### Property 2: Screenshot Naming Convention
*For any* screenshot file in the screenshots directory, the filename should match the pattern `{phase}-{description}-{number}.{ext}`

### Property 3: Screenshot-Documentation Cross-Reference
*For any* screenshot file in the screenshots directory, there should exist at least one reference to that file in WORKFLOW.md

### Property 12: Relative Path Usage
*For any* image reference in WORKFLOW.md, the path should be relative (starting with ./ or ../) not absolute

### Property 13: Git Commit Count
*For any* complete project, the git history should contain at least 15 commits

### Property 14: Git Commit AI Attribution
*For any* commit in the git history, if it was AI-generated, the commit message should contain AI attribution keywords

## Troubleshooting

### "Screenshots directory not found"
Create the screenshots directory:
```bash
mkdir screenshots
```

### "WORKFLOW.md not found"
Create WORKFLOW.md in the project root:
```bash
touch WORKFLOW.md
```

### "Not a git repository"
Initialize git:
```bash
git init
```

### "Need more screenshots"
Capture more screenshots following the naming convention:
```
{phase}-{description}-{number}.png

Examples:
- backend-fastapi-setup-1.png
- frontend-jobs-page-1.png
- mcp-playwright-validation-1.png
```

### "Missing required sections in WORKFLOW.md"
Add the required sections:
- Overview
- Backend Development
- Frontend Development
- AI Agent
- MCP Integration
- Testing
- Evidence
- Reflection

## Integration with CI/CD

Add to your CI pipeline:
```yaml
- name: Validate Evidence
  run: npm run validate:all
```

## Development

### Adding New Validators

1. Create a new validator script in `scripts/`
2. Follow the existing pattern:
   - Define check interfaces
   - Implement validation functions
   - Generate report
   - Print results
   - Exit with appropriate code
3. Add script to `package.json`
4. Update this README

### Testing Validators

Test validators by intentionally creating invalid conditions:
```bash
# Test screenshot validator
rm screenshots/*.png
npm run check:screenshots  # Should fail

# Test git validator
git reset --hard HEAD~20
npm run validate:git  # Should fail
```

## Related Documentation

- [Design Document](../.kiro/specs/ai-evidence-collection/design.md)
- [Requirements](../.kiro/specs/ai-evidence-collection/requirements.md)
- [Tasks](../.kiro/specs/ai-evidence-collection/tasks.md)
- [Screenshot Guide](../screenshots/SCREENSHOT_GUIDE.md)
