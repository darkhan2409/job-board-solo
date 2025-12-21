import * as fs from 'fs';
import * as path from 'path';

/**
 * Validation check result
 */
interface ValidationCheck {
  name: string;
  passed: boolean;
  message: string;
  details?: string[];
}

/**
 * Complete validation report
 */
interface ValidationReport {
  timestamp: string;
  overallStatus: 'pass' | 'fail';
  checks: ValidationCheck[];
  summary: {
    total: number;
    passed: number;
    failed: number;
  };
}

/**
 * Main validation function
 */
function validateEvidence(): ValidationReport {
  const checks: ValidationCheck[] = [];
  
  console.log('🔍 Starting evidence validation...\n');
  
  // Check 1: Screenshot count >= 15
  checks.push(validateScreenshotCount());
  
  // Check 2: Screenshot naming convention
  checks.push(validateScreenshotNaming());
  
  // Check 3: Test results exist
  checks.push(validateTestResults());
  
  // Check 4: MCP evidence count
  checks.push(validateMCPEvidence());
  
  // Check 5: WORKFLOW.md completeness
  checks.push(validateWorkflowDoc());
  
  // Check 6: Git commit count >= 15
  checks.push(validateGitHistory());
  
  // Check 7: Cross-references valid
  checks.push(validateCrossReferences());
  
  return generateReport(checks);
}

/**
 * Validate screenshot count
 */
function validateScreenshotCount(): ValidationCheck {
  const screenshotsDir = path.join(__dirname, '..', 'screenshots');
  
  try {
    if (!fs.existsSync(screenshotsDir)) {
      return {
        name: 'Screenshot Count',
        passed: false,
        message: 'Screenshots directory does not exist',
        details: [`Expected directory: ${screenshotsDir}`]
      };
    }
    
    const files = fs.readdirSync(screenshotsDir);
    const imageFiles = files.filter(f => /\.(png|jpg|jpeg)$/i.test(f));
    const count = imageFiles.length;
    
    return {
      name: 'Screenshot Count',
      passed: count >= 15,
      message: `Found ${count} screenshots (minimum: 15)`,
      details: count < 15 ? [`Need ${15 - count} more screenshots`] : undefined
    };
  } catch (error) {
    return {
      name: 'Screenshot Count',
      passed: false,
      message: 'Error checking screenshots',
      details: [String(error)]
    };
  }
}

/**
 * Validate screenshot naming convention
 */
function validateScreenshotNaming(): ValidationCheck {
  const screenshotsDir = path.join(__dirname, '..', 'screenshots');
  const pattern = /^(backend|frontend|ai-agent|aiagent|qa|mcp|runtime)-.+?-\d+\.(png|jpg|jpeg)$/i;
  
  try {
    if (!fs.existsSync(screenshotsDir)) {
      return {
        name: 'Screenshot Naming',
        passed: false,
        message: 'Screenshots directory does not exist'
      };
    }
    
    const files = fs.readdirSync(screenshotsDir);
    const imageFiles = files.filter(f => /\.(png|jpg|jpeg)$/i.test(f));
    const invalidFiles = imageFiles.filter(f => !pattern.test(f));
    
    return {
      name: 'Screenshot Naming',
      passed: invalidFiles.length === 0,
      message: invalidFiles.length === 0 
        ? 'All screenshots follow naming convention'
        : `${invalidFiles.length} screenshots have invalid names`,
      details: invalidFiles.length > 0 ? invalidFiles : undefined
    };
  } catch (error) {
    return {
      name: 'Screenshot Naming',
      passed: false,
      message: 'Error checking screenshot names',
      details: [String(error)]
    };
  }
}

/**
 * Validate test results exist
 */
function validateTestResults(): ValidationCheck {
  const summaryPath = path.join(__dirname, '..', 'test-results', 'summary.md');
  
  try {
    const exists = fs.existsSync(summaryPath);
    
    return {
      name: 'Test Results',
      passed: exists,
      message: exists 
        ? 'Test summary exists'
        : 'Test summary not found',
      details: !exists ? [`Expected file: ${summaryPath}`] : undefined
    };
  } catch (error) {
    return {
      name: 'Test Results',
      passed: false,
      message: 'Error checking test results',
      details: [String(error)]
    };
  }
}

/**
 * Validate MCP evidence count
 */
function validateMCPEvidence(): ValidationCheck {
  const workflowPath = path.join(__dirname, '..', 'WORKFLOW.md');
  
  try {
    if (!fs.existsSync(workflowPath)) {
      return {
        name: 'MCP Evidence',
        passed: false,
        message: 'WORKFLOW.md not found'
      };
    }
    
    const content = fs.readFileSync(workflowPath, 'utf-8');
    
    // Count Playwright MCP mentions (need 5+)
    const playwrightMatches = content.match(/playwright\s+mcp/gi) || [];
    const playwrightCount = playwrightMatches.length;
    
    // Count Context7 MCP mentions (need 10+)
    const context7Matches = content.match(/context7\s+mcp/gi) || [];
    const context7Count = context7Matches.length;
    
    const passed = playwrightCount >= 5 && context7Count >= 10;
    
    return {
      name: 'MCP Evidence',
      passed,
      message: `Playwright: ${playwrightCount}/5, Context7: ${context7Count}/10`,
      details: !passed ? [
        playwrightCount < 5 ? `Need ${5 - playwrightCount} more Playwright examples` : '',
        context7Count < 10 ? `Need ${10 - context7Count} more Context7 examples` : ''
      ].filter(Boolean) : undefined
    };
  } catch (error) {
    return {
      name: 'MCP Evidence',
      passed: false,
      message: 'Error checking MCP evidence',
      details: [String(error)]
    };
  }
}

/**
 * Validate WORKFLOW.md completeness
 */
function validateWorkflowDoc(): ValidationCheck {
  const workflowPath = path.join(__dirname, '..', 'WORKFLOW.md');
  
  try {
    if (!fs.existsSync(workflowPath)) {
      return {
        name: 'WORKFLOW.md',
        passed: false,
        message: 'WORKFLOW.md not found'
      };
    }
    
    const content = fs.readFileSync(workflowPath, 'utf-8');
    
    // Check for required sections
    const requiredSections = [
      'MCP',
      'Test',
      'Screenshot',
      'Evidence'
    ];
    
    const missingSections = requiredSections.filter(section => 
      !content.toLowerCase().includes(section.toLowerCase())
    );
    
    return {
      name: 'WORKFLOW.md',
      passed: missingSections.length === 0,
      message: missingSections.length === 0
        ? 'WORKFLOW.md contains required sections'
        : `Missing ${missingSections.length} required sections`,
      details: missingSections.length > 0 ? missingSections : undefined
    };
  } catch (error) {
    return {
      name: 'WORKFLOW.md',
      passed: false,
      message: 'Error checking WORKFLOW.md',
      details: [String(error)]
    };
  }
}

/**
 * Validate git history
 */
function validateGitHistory(): ValidationCheck {
  const { execSync } = require('child_process');
  
  try {
    // Check if git repo exists
    execSync('git rev-parse --git-dir', { 
      cwd: path.join(__dirname, '..'),
      stdio: 'pipe'
    });
    
    // Get commit count
    const output = execSync('git rev-list --count HEAD', {
      cwd: path.join(__dirname, '..'),
      encoding: 'utf-8',
      stdio: 'pipe'
    });
    
    const count = parseInt(output.trim(), 10);
    
    return {
      name: 'Git History',
      passed: count >= 15,
      message: `Found ${count} commits (minimum: 15)`,
      details: count < 15 ? [`Need ${15 - count} more commits`] : undefined
    };
  } catch (error) {
    return {
      name: 'Git History',
      passed: false,
      message: 'Error checking git history',
      details: ['Run: npm run validate:git for detailed git validation']
    };
  }
}

/**
 * Validate cross-references
 */
function validateCrossReferences(): ValidationCheck {
  const workflowPath = path.join(__dirname, '..', 'WORKFLOW.md');
  const screenshotsDir = path.join(__dirname, '..', 'screenshots');
  
  try {
    if (!fs.existsSync(workflowPath)) {
      return {
        name: 'Cross-References',
        passed: false,
        message: 'WORKFLOW.md not found'
      };
    }
    
    const content = fs.readFileSync(workflowPath, 'utf-8');
    
    // Extract image references from markdown
    const imageRegex = /!\[.*?\]\((\.\/screenshots\/[^)]+)\)/g;
    const matches = [...content.matchAll(imageRegex)];
    const referencedImages = matches.map(m => m[1].replace('./screenshots/', ''));
    
    // Check if referenced images exist
    const missingImages: string[] = [];
    for (const img of referencedImages) {
      const imgPath = path.join(screenshotsDir, img);
      if (!fs.existsSync(imgPath)) {
        missingImages.push(img);
      }
    }
    
    return {
      name: 'Cross-References',
      passed: missingImages.length === 0,
      message: missingImages.length === 0
        ? `All ${referencedImages.length} referenced images exist`
        : `${missingImages.length} referenced images not found`,
      details: missingImages.length > 0 ? missingImages : undefined
    };
  } catch (error) {
    return {
      name: 'Cross-References',
      passed: false,
      message: 'Error checking cross-references',
      details: [String(error)]
    };
  }
}

/**
 * Generate validation report
 */
function generateReport(checks: ValidationCheck[]): ValidationReport {
  const passed = checks.filter(c => c.passed).length;
  const failed = checks.filter(c => !c.passed).length;
  
  const report: ValidationReport = {
    timestamp: new Date().toISOString(),
    overallStatus: failed === 0 ? 'pass' : 'fail',
    checks,
    summary: {
      total: checks.length,
      passed,
      failed
    }
  };
  
  return report;
}

/**
 * Print report to console
 */
function printReport(report: ValidationReport): void {
  console.log('\n' + '='.repeat(60));
  console.log('📊 VALIDATION REPORT');
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
    console.log('\n⚠️  Some validation checks failed. Please address the issues above.');
  } else {
    console.log('\n🎉 All validation checks passed!');
  }
}

// Run validation
const report = validateEvidence();
printReport(report);

// Exit with appropriate code
process.exit(report.overallStatus === 'pass' ? 0 : 1);
