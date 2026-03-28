// Verification script to check if everything is set up correctly
const fs = require('fs');
const path = require('path');

console.log('🔍 Verifying Delhi Ka Khel Setup...\n');

let allGood = true;

// Check 1: Frontend directory exists
console.log('1. Checking frontend directory...');
if (fs.existsSync('frontend')) {
  console.log('   ✅ Frontend directory exists');
} else {
  console.log('   ❌ Frontend directory not found');
  allGood = false;
}

// Check 2: Frontend package.json exists
console.log('\n2. Checking frontend package.json...');
if (fs.existsSync('frontend/package.json')) {
  console.log('   ✅ package.json exists');
  const pkg = JSON.parse(fs.readFileSync('frontend/package.json', 'utf8'));
  console.log('   📦 Dependencies:', Object.keys(pkg.dependencies || {}).length);
} else {
  console.log('   ❌ package.json not found');
  allGood = false;
}

// Check 3: Contract addresses configured
console.log('\n3. Checking contract addresses...');
const addressesPath = 'frontend/src/contracts/addresses.json';
if (fs.existsSync(addressesPath)) {
  const addresses = JSON.parse(fs.readFileSync(addressesPath, 'utf8'));
  console.log('   ✅ addresses.json exists');
  console.log('   📍 PlayerBadge:', addresses.playerBadge);
  console.log('   📍 TicTacToe:', addresses.ticTacToe);
  console.log('   🌐 Network:', addresses.network);
  console.log('   🔗 Chain ID:', addresses.chainId);
  
  if (addresses.playerBadge === '0x0000000000000000000000000000000000000000') {
    console.log('   ⚠️  Warning: PlayerBadge address is placeholder');
  }
  if (addresses.ticTacToe === '0x0000000000000000000000000000000000000000') {
    console.log('   ⚠️  Warning: TicTacToe address is placeholder');
  }
} else {
  console.log('   ❌ addresses.json not found');
  allGood = false;
}

// Check 4: Contract ABIs exist
console.log('\n4. Checking contract ABIs...');
const playerBadgeABI = 'frontend/src/contracts/abis/PlayerBadge.json';
const ticTacToeABI = 'frontend/src/contracts/abis/TicTacToe.json';

if (fs.existsSync(playerBadgeABI)) {
  console.log('   ✅ PlayerBadge ABI exists');
} else {
  console.log('   ❌ PlayerBadge ABI not found');
  allGood = false;
}

if (fs.existsSync(ticTacToeABI)) {
  console.log('   ✅ TicTacToe ABI exists');
} else {
  console.log('   ❌ TicTacToe ABI not found');
  allGood = false;
}

// Check 5: Main components exist
console.log('\n5. Checking React components...');
const components = [
  'frontend/src/App.tsx',
  'frontend/src/main.tsx',
  'frontend/src/components/WalletConnect.tsx',
  'frontend/src/components/BadgeMinting.tsx',
  'frontend/src/components/GameCreation.tsx',
  'frontend/src/components/GameJoining.tsx',
  'frontend/src/components/GameBoard.tsx'
];

let componentsOk = true;
components.forEach(comp => {
  if (fs.existsSync(comp)) {
    console.log(`   ✅ ${path.basename(comp)}`);
  } else {
    console.log(`   ❌ ${path.basename(comp)} not found`);
    componentsOk = false;
    allGood = false;
  }
});

// Check 6: Configuration files
console.log('\n6. Checking configuration files...');
const configs = [
  'frontend/vite.config.ts',
  'frontend/tailwind.config.js',
  'frontend/tsconfig.json',
  'frontend/index.html'
];

configs.forEach(config => {
  if (fs.existsSync(config)) {
    console.log(`   ✅ ${path.basename(config)}`);
  } else {
    console.log(`   ❌ ${path.basename(config)} not found`);
    allGood = false;
  }
});

// Check 7: node_modules
console.log('\n7. Checking dependencies installation...');
if (fs.existsSync('frontend/node_modules')) {
  console.log('   ✅ node_modules exists (dependencies installed)');
} else {
  console.log('   ⚠️  node_modules not found (run: cd frontend && npm install)');
}

// Final summary
console.log('\n' + '='.repeat(50));
if (allGood) {
  console.log('✅ All checks passed! Your setup looks good!');
  console.log('\n📋 Next steps:');
  console.log('   1. cd frontend');
  console.log('   2. npm install (if not done)');
  console.log('   3. npm run dev');
  console.log('   4. Open http://localhost:3000');
} else {
  console.log('❌ Some checks failed. Please review the errors above.');
  console.log('\n📋 To fix:');
  console.log('   1. Make sure all files are created');
  console.log('   2. Check FINAL_SETUP_STEPS.md for guidance');
  console.log('   3. Run this script again to verify');
}
console.log('='.repeat(50) + '\n');

console.log('🔗 Your deployed contracts:');
console.log('   PlayerBadge: 0xBE679568645D1e0fb17eE9Fb0B70BCd3d1009116');
console.log('   TicTacToe:   0x294645FEB89dC2651DBE2B3299880E0126a5FaFA');
console.log('   Explorer:    https://testnet.monadexplorer.com\n');
