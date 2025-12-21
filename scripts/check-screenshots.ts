import * as fs from 'fs';
import * as path from 'path';

interface Screenshot {
  filename: string;
  phase: string;
  description: string;
  number: number;
  valid: boolean;
  errors: string[];
}

const VALID_PHASES = ['backend', 'frontend', 'ai-agent', 'aiagent', 'mcp', 'runtime', 'qa'];
const VALID_EXTENSIONS = ['.png', '.jpg', '.jpeg'];
const SCREENSHOTS_DIR = path.join(__dirname, '..', 'screenshots');

function parseScreenshotFilename(filename: string): Screenshot {
  const errors: string[] = [];
  const ext = path.extname(filename).toLowerCase();
  const nameWithoutExt = path.basename(filename, ext);
  
  // Check extension
  if (!VALID_EXTENSIONS.includes(ext)) {
    errors.push(`Invalid extension: ${ext}. Must be one of: ${VALID_EXTENSIONS.join(', ')}`);
  }
  
  // Parse filename pattern: {phase}-{description}-{number}
  const parts = nameWithoutExt.split('-');
  
  if (parts.length < 3) {
    errors.push(`Filename must follow pattern: {phase}-{description}-{number}.{ext}`);
    return {
      filename,
      phase: '',
      description: '',
      number: 0,
      valid: false,
      errors
    };
  }
  
  const phase = parts[0];
  const numberStr = parts[parts.length - 1];
  const description = parts.slice(1, -1).join('-');
  
  // Validate phase
  if (!VALID_PHASES.includes(phase)) {
    errors.push(`Invalid phase: ${phase}. Must be one of: ${VALID_PHASES.join(', ')}`);
  }
  
  // Validate number
  const number = parseInt(numberStr, 10);
  if (isNaN(number) || number < 1) {
    errors.push(`Invalid number: ${numberStr}. Must be a positive integer`);
  }
  
  // Validate description
  if (!description || description.length === 0) {
    errors.push(`Description cannot be empty`);
  }
  
  return {
    filename,
    phase,
    description,
    number,
    valid: errors.length === 0,
    errors
  };
}

function checkScreenshots(): void {
  console.log('🔍 Checking screenshots...\n');
  
  // Check if directory exists
  if (!fs.existsSync(SCREENSHOTS_DIR)) {
    console.error('❌ Screenshots directory not found:', SCREENSHOTS_DIR);
    process.exit(1);
  }
  
  // Get all files
  const files = fs.readdirSync(SCREENSHOTS_DIR)
    .filter(f => {
      const ext = path.extname(f).toLowerCase();
      return VALID_EXTENSIONS.includes(ext);
    });
  
  console.log(`📊 Found ${files.length} screenshot files\n`);
  
  if (files.length === 0) {
    console.log('⚠️  No screenshots found. Please capture screenshots following the guide.');
    console.log('   See: screenshots/SCREENSHOT_GUIDE.md\n');
    process.exit(0);
  }
  
  // Parse and validate each file
  const screenshots = files.map(parseScreenshotFilename);
  const validScreenshots = screenshots.filter(s => s.valid);
  const invalidScreenshots = screenshots.filter(s => !s.valid);
  
  // Group by phase
  const byPhase: Record<string, Screenshot[]> = {};
  validScreenshots.forEach(s => {
    if (!byPhase[s.phase]) {
      byPhase[s.phase] = [];
    }
    byPhase[s.phase].push(s);
  });
  
  // Display results
  console.log('✅ Valid Screenshots by Phase:');
  Object.keys(byPhase).sort().forEach(phase => {
    console.log(`   ${phase}: ${byPhase[phase].length} screenshots`);
    byPhase[phase].forEach(s => {
      console.log(`      - ${s.filename}`);
    });
  });
  console.log();
  
  if (invalidScreenshots.length > 0) {
    console.log('❌ Invalid Screenshots:');
    invalidScreenshots.forEach(s => {
      console.log(`   ${s.filename}`);
      s.errors.forEach(err => {
        console.log(`      - ${err}`);
      });
    });
    console.log();
  }
  
  // Check requirements
  console.log('📋 Requirements Check:');
  
  const totalValid = validScreenshots.length;
  const meetsCount = totalValid >= 15;
  console.log(`   Screenshot count: ${totalValid}/15 ${meetsCount ? '✅' : '❌'}`);
  
  const hasBackend = (byPhase['backend']?.length || 0) >= 4;
  console.log(`   Backend screenshots: ${byPhase['backend']?.length || 0}/4 ${hasBackend ? '✅' : '⚠️'}`);
  
  const hasFrontend = (byPhase['frontend']?.length || 0) >= 5;
  console.log(`   Frontend screenshots: ${byPhase['frontend']?.length || 0}/5 ${hasFrontend ? '✅' : '⚠️'}`);
  
  const hasAIAgent = (byPhase['ai-agent']?.length || 0) >= 4;
  console.log(`   AI Agent screenshots: ${byPhase['ai-agent']?.length || 0}/4 ${hasAIAgent ? '✅' : '⚠️'}`);
  
  const hasMCP = (byPhase['mcp']?.length || 0) >= 4;
  console.log(`   MCP screenshots: ${byPhase['mcp']?.length || 0}/4 ${hasMCP ? '✅' : '⚠️'}`);
  
  const hasRuntime = (byPhase['runtime']?.length || 0) >= 5;
  console.log(`   Runtime screenshots: ${byPhase['runtime']?.length || 0}/5 ${hasRuntime ? '✅' : '⚠️'}`);
  
  console.log();
  
  if (meetsCount && invalidScreenshots.length === 0) {
    console.log('🎉 All screenshot requirements met!');
    process.exit(0);
  } else if (!meetsCount) {
    console.log(`⚠️  Need ${15 - totalValid} more screenshots to meet minimum requirement.`);
    process.exit(1);
  } else {
    console.log('⚠️  Some screenshots have naming issues. Please fix them.');
    process.exit(1);
  }
}

checkScreenshots();
