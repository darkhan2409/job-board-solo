import * as fs from 'fs';
import * as path from 'path';

/**
 * Documentation validation check result
 */
interface DocValidationCheck {
  name: string;
  passed: boolean;
  message: string;
  details?: string[];
}

/**
 * Documentation validation report
 */
interface DocValidationReport {
  timestamp: string;
  overallStatus: 'pass' | 'fail';
  checks: DocValidationCheck[];
  summary: {
    total: number;
    passed: number;
    failed: number;
  };
}

const WORKFLOW_PATH = path.join(__dirname, '..', 'WORKFLOW.md');
const SCREENSHOTS_DIR = path.join(__dirname, '..', 'screenshots');

/**
 * Main documentation validation function
 */
function validateDocumentation(): DocValidationReport {
  const checks: DocValidationCheck[] = [];
  
  console.log('📄 Validating documentation...\n');
  
  // Check 1: WORKFLOW.md exists
  checks.push(validateWorkflowExists());
  
  // Check 2: Required sections present
  checks.push(validateRequiredSections());
  
  // Check 3: Screenshot references
  checks.push(validateScreenshotReferences());
  
  // Check 4: MCP usage documentation
  checks.push(validateMCPDocumentation());
  
  // Check 5: Test results documentation
  checks.push(validateTestDocumentation());
  
  // Check 6: Reflection section
  checks.push(validateReflectionSection());
  
  // Check 7: Relative paths usage
  checks.push(validateRelativePaths());
  
  return generateReport(checks);
}

/**
 * Check if WORKFLOW.md exists
 */
function validateWorkflowExists(): DocValidationCheck {
  try {
    const exists = fs.existsSync(WORKFLOW_PATH);
    
    return {
      name: 'WORKFLOW.md Exists',
      passed: exists,
      message: exists ? 'WORKFLOW.md found' : 'WORKFLOW.md not found',
      details: !exists ? [`Expected path: ${WORKFLOW_PATH}`] : undefined
    };
  } catch (error) {
    return {
      name: 'WORKFLOW.md Exists',
      passed: false,
      message: 'Error checking WORKFLOW.md',
      details: [String(error)]
    };
  }
}

/**
 * Validate required sections are present
 */
function validateRequiredSections(): DocValidationCheck {
  try {
    if (!fs.existsSync(WORKFLOW_PATH)) {
      return {
        name: 'Required Sections',
        passed: false,
        message: 'WORKFLOW.md not found'
      };
    }
    
    const content = fs.readFileSync(WORKFLOW_PATH, 'utf-8');
    
    const requiredSections = [
      { name: 'Overview', pattern: /##?\s+overview/i },
      { name: 'Backend Development', pattern: /##?\s+backend/i },
      { name: 'Frontend Development', pattern: /##?\s+frontend/i },
      { name: 'AI Agent', pattern: /##?\s+ai\s+agent/i },
      { name: 'MCP Integration', pattern: /##?\s+mcp/i },
      { name: 'Testing', pattern: /##?\s+test/i },
      { name: 'Evidence', pattern: /##?\s+evidence/i }
    ];
    
    const missingSections = requiredSections.filter(section => 
      !section.pattern.test(content)
    ).map(s => s.name);
    
    return {
      name: 'Required Sections',
      passed: missingSections.length === 0,
      message: missingSections.length === 0
        ? 'All required sections present'
        : `Missing ${missingSections.length} required sections`,
      details: missingSections.length > 0 ? missingSections : undefined
    };
  } catch (error) {
    return {
      name: 'Required Sections',
      passed: false,
      message: 'Error checking sections',
      details: [String(error)]
    };
  }
}

/**
 * Validate screenshot references
 */
function validateScreenshotReferences(): DocValidationCheck {
  try {
    if (!fs.existsSync(WORKFLOW_PATH)) {
      return {
        name: 'Screenshot References',
        passed: false,
        message: 'WORKFLOW.md not found'
      };
    }
    
    const content = fs.readFileSync(WORKFLOW_PATH, 'utf-8');
    
    // Extract image references
    const imageRegex = /!\[.*?\]\(([^)]+)\)/g;
    const matches = [...content.matchAll(imageRegex)];
    const imageRefs = matches.map(m => m[1]);
    
    if (imageRefs.length === 0) {
      return {
        name: 'Screenshot References',
        passed: false,
        message: 'No screenshots referenced in WORKFLOW.md',
        details: ['Add screenshot references using ![caption](./screenshots/filename.png)']
      };
    }
    
    // Check if referenced files exist
    const missingFiles: string[] = [];
    const screenshotRefs = imageRefs.filter(ref => ref.includes('screenshots/'));
    
    for (const ref of screenshotRefs) {
      const cleanPath = ref.replace(/^\.\//, '').replace(/^screenshots\//, '');
      const fullPath = path.join(SCREENSHOTS_DIR, cleanPath);
      
      if (!fs.existsSync(fullPath)) {
        missingFiles.push(cleanPath);
      }
    }
    
    return {
      name: 'Screenshot References',
      passed: missingFiles.length === 0 && screenshotRefs.length >= 10,
      message: missingFiles.length === 0
        ? `${screenshotRefs.length} screenshots referenced (minimum: 10)`
        : `${missingFiles.length} referenced screenshots not found`,
      details: missingFiles.length > 0 ? missingFiles : 
               screenshotRefs.length < 10 ? [`Need ${10 - screenshotRefs.length} more screenshot references`] : undefined
    };
  } catch (error) {
    return {
      name: 'Screenshot References',
      passed: false,
      message: 'Error checking screenshot references',
      details: [String(error)]
    };
  }
}

/**
 * Validate MCP documentation
 */
function validateMCPDocumentation(): DocValidationCheck {
  try {
    if (!fs.existsSync(WORKFLOW_PATH)) {
      return {
        name: 'MCP Documentation',
        passed: false,
        message: 'WORKFLOW.md not found'
      };
    }
    
    const content = fs.readFileSync(WORKFLOW_PATH, 'utf-8');
    
    // Check for MCP mentions
    const playwrightMentions = (content.match(/playwright\s+mcp/gi) || []).length;
    const context7Mentions = (content.match(/context7\s+mcp/gi) || []).length;
    
    // Check for MCP usage table
    const hasMCPTable = /\|\s*Phase\s*\|.*MCP.*\|/i.test(content);
    
    const issues: string[] = [];
    if (playwrightMentions < 5) {
      issues.push(`Need ${5 - playwrightMentions} more Playwright MCP examples`);
    }
    if (context7Mentions < 10) {
      issues.push(`Need ${10 - context7Mentions} more Context7 MCP examples`);
    }
    if (!hasMCPTable) {
      issues.push('Missing MCP usage summary table');
    }
    
    return {
      name: 'MCP Documentation',
      passed: issues.length === 0,
      message: issues.length === 0
        ? `Playwright: ${playwrightMentions}/5, Context7: ${context7Mentions}/10, Table: ✓`
        : 'MCP documentation incomplete',
      details: issues.length > 0 ? issues : undefined
    };
  } catch (error) {
    return {
      name: 'MCP Documentation',
      passed: false,
      message: 'Error checking MCP documentation',
      details: [String(error)]
    };
  }
}

/**
 * Validate test documentation
 */
function validateTestDocumentation(): DocValidationCheck {
  try {
    if (!fs.existsSync(WORKFLOW_PATH)) {
      return {
        name: 'Test Documentation',
        passed: false,
        message: 'WORKFLOW.md not found'
      };
    }
    
    const content = fs.readFileSync(WORKFLOW_PATH, 'utf-8');
    
    // Check for test-related content
    const hasTestSection = /##?\s+test/i.test(content);
    const hasTestResults = /test\s+results?/i.test(content);
    const hasE2EMention = /e2e|end.to.end/i.test(content);
    
    const issues: string[] = [];
    if (!hasTestSection) issues.push('Missing test section');
    if (!hasTestResults) issues.push('Missing test results documentation');
    if (!hasE2EMention) issues.push('Missing E2E test mention');
    
    return {
      name: 'Test Documentation',
      passed: issues.length === 0,
      message: issues.length === 0
        ? 'Test documentation complete'
        : 'Test documentation incomplete',
      details: issues.length > 0 ? issues : undefined
    };
  } catch (error) {
    return {
      name: 'Test Documentation',
      passed: false,
      message: 'Error checking test documentation',
      details: [String(error)]
    };
  }
}

/**
 * Validate reflection section
 */
function validateReflectionSection(): DocValidationCheck {
  try {
    if (!fs.existsSync(WORKFLOW_PATH)) {
      return {
        name: 'Reflection Section',
        passed: false,
        message: 'WORKFLOW.md not found'
      };
    }
    
    const content = fs.readFileSync(WORKFLOW_PATH, 'utf-8');
    
    // Check for reflection-related content
    const hasReflection = /##?\s+reflection/i.test(content);
    const hasLessons = /lesson|learn/i.test(content);
    const hasChallenges = /challenge|difficult|problem/i.test(content);
    
    const issues: string[] = [];
    if (!hasReflection) issues.push('Missing reflection section');
    if (!hasLessons) issues.push('Missing lessons learned');
    if (!hasChallenges) issues.push('Missing challenges discussion');
    
    return {
      name: 'Reflection Section',
      passed: issues.length === 0,
      message: issues.length === 0
        ? 'Reflection section complete'
        : 'Reflection section incomplete',
      details: issues.length > 0 ? issues : undefined
    };
  } catch (error) {
    return {
      name: 'Reflection Section',
      passed: false,
      message: 'Error checking reflection section',
      details: [String(error)]
    };
  }
}

/**
 * Validate relative paths are used
 */
function validateRelativePaths(): DocValidationCheck {
  try {
    if (!fs.existsSync(WORKFLOW_PATH)) {
      return {
        name: 'Relative Paths',
        passed: false,
        message: 'WORKFLOW.md not found'
      };
    }
    
    const content = fs.readFileSync(WORKFLOW_PATH, 'utf-8');
    
    // Check for absolute paths in image references
    const imageRegex = /!\[.*?\]\(([^)]+)\)/g;
    const matches = [...content.matchAll(imageRegex)];
    const absolutePaths = matches
      .map(m => m[1])
      .filter(path => path.startsWith('/') || /^[A-Z]:/i.test(path));
    
    return {
      name: 'Relative Paths',
      passed: absolutePaths.length === 0,
      message: absolutePaths.length === 0
        ? 'All image paths are relative'
        : `${absolutePaths.length} absolute paths found`,
      details: absolutePaths.length > 0 ? absolutePaths : undefined
    };
  } catch (error) {
    return {
      name: 'Relative Paths',
      passed: false,
      message: 'Error checking paths',
      details: [String(error)]
    };
  }
}

/**
 * Generate validation report
 */
function generateReport(checks: DocValidationCheck[]): DocValidationReport {
  const passed = checks.filter(c => c.passed).length;
  const failed = checks.filter(c => !c.passed).length;
  
  return {
    timestamp: new Date().toISOString(),
    overallStatus: failed === 0 ? 'pass' : 'fail',
    checks,
    summary: {
      total: checks.length,
      passed,
      failed
    }
  };
}

/**
 * Print report to console
 */
function printReport(report: DocValidationReport): void {
  console.log('\n' + '='.repeat(60));
  console.log('📄 DOCUMENTATION VALIDATION REPORT');
  console.log('='.repeat(60));
  console.log(`Timestamp: ${report.timestamp}`);
  console.log(`Status: ${report.overallStatus === 'pass' ? '✅ PASS' : '❌ FAIL'}`);
  console.log(`\nSummary: ${report.summary.passed}/${report.summary.total} checks passed\n`);
  
  for (const check of report.checks) {
    const icon = check.passed ? '✅' : '❌';
    console.log(`${icon} ${check.name}: ${check.message}`);
    
    if (check.details && check.details.length > 0) {
      for (const detail of check.details) {
        console.log(`   - ${detail}`);
      }
    }
  }
  
  console.log('\n' + '='.repeat(60));
  
  if (report.overallStatus === 'fail') {
    console.log('\n⚠️  Some documentation checks failed. Please address the issues above.');
  } else {
    console.log('\n🎉 All documentation checks passed!');
  }
}

// Run validation
const report = validateDocumentation();
printReport(report);

// Exit with appropriate code
process.exit(report.overallStatus === 'pass' ? 0 : 1);
