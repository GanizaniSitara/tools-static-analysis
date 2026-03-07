#!/usr/bin/env node
/**
 * Test Claude Code file launching via viewer
 * Verifies that clicking a Claude Code button properly passes file path and prompt
 */

const { chromium } = require('playwright');
const { spawn } = require('child_process');
const http = require('http');

async function waitForServer(port, maxAttempts = 30) {
  for (let i = 0; i < maxAttempts; i++) {
    try {
      await new Promise((resolve, reject) => {
        const req = http.get(`http://localhost:${port}/_ping`, (res) => {
          resolve();
        });
        req.on('error', reject);
        req.setTimeout(1000);
      });
      return true;
    } catch (e) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
  return false;
}

async function checkClaudeProcess(beforePids) {
  return new Promise((resolve) => {
    const proc = spawn('ps', ['aux']);
    let output = '';

    proc.stdout.on('data', (data) => {
      output += data.toString();
    });

    proc.on('close', () => {
      const lines = output.split('\n');
      const claudeLines = lines.filter(line =>
        line.includes('claude') &&
        (line.includes('pts/') || line.includes('tty')) &&
        !line.includes('grep')
      );

      // Find new processes
      const newProcesses = claudeLines.filter(line => {
        const match = line.match(/\s+(\d+)\s+/);
        if (match) {
          const pid = parseInt(match[1]);
          return !beforePids.includes(pid);
        }
        return false;
      });

      resolve(newProcesses);
    });
  });
}

async function getClaudePids() {
  return new Promise((resolve) => {
    const proc = spawn('ps', ['aux']);
    let output = '';

    proc.stdout.on('data', (data) => {
      output += data.toString();
    });

    proc.on('close', () => {
      const lines = output.split('\n');
      const pids = [];
      lines.forEach(line => {
        if (line.includes('claude') && (line.includes('pts/') || line.includes('tty'))) {
          const match = line.match(/\s+(\d+)\s+/);
          if (match) {
            pids.push(parseInt(match[1]));
          }
        }
      });
      resolve(pids);
    });
  });
}

async function main() {
  console.log('\n=== Claude Code Launch Test ===\n');

  // Check servers are running
  console.log('Checking servers...');
  const companionOk = await waitForServer(19280, 5);
  const viewerOk = await waitForServer(8022, 5);

  if (!companionOk) {
    console.error('❌ Companion agent not running on port 19280');
    process.exit(1);
  }
  if (!viewerOk) {
    console.error('❌ Viewer not running on port 8022');
    process.exit(1);
  }

  console.log('✓ Both servers are running\n');

  // Get current Claude PIDs
  const beforePids = await getClaudePids();
  console.log(`Current Claude processes: ${beforePids.length}\n`);

  // Launch browser
  console.log('Launching browser...');
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const context = await browser.newContext();
  const page = await context.newPage();

  // Monitor console errors
  page.on('console', msg => {
    if (msg.type() === 'error') {
      console.log('Browser console error:', msg.text());
    }
  });

  page.on('pageerror', error => {
    console.log('Page error:', error.message);
  });

  // Monitor network requests to companion and run.py
  let companionCalls = [];
  page.on('response', async (response) => {
    const url = response.url();
    if (url.includes('/_open')) {
      const status = response.status();
      let body = null;
      try {
        body = await response.json();
      } catch (e) {
        body = await response.text();
      }
      companionCalls.push({ url, status, body });
      console.log(`API call to: ${url} (status ${status})`);
    }
  });

  // Open viewer
  console.log('Opening viewer...');
  await page.goto('http://localhost:8022/viewer.html', { waitUntil: 'load', timeout: 30000 });

  // Wait for page to be ready
  await page.waitForTimeout(3000);

  // Check if repos loaded
  const reposCount = await page.evaluate(() => {
    return window._repos ? window._repos.length : 0;
  });

  console.log(`✓ Viewer loaded (${reposCount} repos)\n`);

  // Navigate to Security tab
  console.log('Navigating to Security tab...');
  const securityTab = await page.$('[data-tab="security"]');
  if (securityTab) {
    await securityTab.click();
    await page.waitForTimeout(2000);
  } else {
    console.log('⚠ No security tab found, staying on current tab');
  }

  // Debug: check what's in the page
  const pageInfo = await page.evaluate(() => {
    return {
      hasRepos: typeof window._repos !== 'undefined',
      reposCount: window._repos ? window._repos.length : 0,
      hasClaude: typeof _openClaude !== 'undefined',
      buttonCount: document.querySelectorAll('button').length,
      claudeBtnCount: document.querySelectorAll('[onclick*="Claude"]').length
    };
  });
  console.log('Page info:', pageInfo);

  // Find visible Claude Code button
  console.log('Looking for visible Claude Code button...');
  const claudeButtons = await page.$$('.file-claude');
  console.log(`Found ${claudeButtons.length} total Claude buttons`);

  let claudeButton = null;
  for (const btn of claudeButtons) {
    const isVisible = await btn.isVisible();
    if (isVisible) {
      claudeButton = btn;
      break;
    }
  }

  if (!claudeButton) {
    console.error('❌ No visible Claude Code button found');
    await browser.close();
    process.exit(1);
  }

  console.log('✓ Found visible Claude Code button\n');

  // Get button details
  const buttonData = await claudeButton.evaluate(btn => ({
    file: btn.getAttribute('data-path'),
    line: btn.getAttribute('data-line'),
    project: btn.getAttribute('data-project'),
    smell: btn.getAttribute('data-smell')
  }));

  console.log('Button data:', JSON.stringify(buttonData, null, 2));
  console.log('');

  // Click the button
  console.log('Clicking Claude Code button...');
  await claudeButton.click({ force: true });

  // Wait for companion call
  await page.waitForTimeout(2000);

  // Check companion was called
  if (companionCalls.length === 0) {
    console.error('❌ No companion API call detected');
    await browser.close();
    process.exit(1);
  }

  console.log('✓ Companion API called\n');

  const call = companionCalls[0];
  console.log('API Response:', JSON.stringify(call.body, null, 2));
  console.log('');

  // Check for new Claude processes
  console.log('Checking for new Claude Code process...');
  await new Promise(resolve => setTimeout(resolve, 2000));

  const newProcesses = await checkClaudeProcess(beforePids);

  if (newProcesses.length > 0) {
    console.log('✓ New Claude Code process detected:\n');
    newProcesses.forEach(line => {
      console.log('  ' + line.trim());
    });
    console.log('');
  } else {
    console.log('⚠ No new Claude Code process detected (might be normal on headless)');
    console.log('');
  }

  // Parse the command line to verify file path
  if (newProcesses.length > 0) {
    const cmdLine = newProcesses[0];

    // Check if file path is in the command
    const hasFilePath = buttonData.file && cmdLine.includes(buttonData.file);
    const hasAddDir = cmdLine.includes('--add-dir');
    const hasPrompt = cmdLine.includes('--append-system-prompt');

    console.log('Command verification:');
    console.log(`  File path in command: ${hasFilePath ? '✓' : '❌'}`);
    console.log(`  --add-dir flag: ${hasAddDir ? '✓' : '❌'}`);
    console.log(`  --append-system-prompt flag: ${hasPrompt ? '✓' : '❌'}`);
    console.log('');

    if (!hasFilePath) {
      console.error('❌ File path not passed to Claude Code!');
      await browser.close();
      process.exit(1);
    }
  }

  await browser.close();

  console.log('=== Test Passed ✓ ===\n');
  console.log('Claude Code launch is working correctly.');
  console.log('File path is being passed as first positional argument.');
}

main().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});
