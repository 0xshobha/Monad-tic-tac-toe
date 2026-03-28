# 🚦 Delhi Ka Khel - On-Chain Tic Tac Toe 🛑

A fully on-chain Tic Tac Toe game built for **Monad Blitz New Delhi** hackathon! Every move is a real blockchain transaction on Monad Testnet, showcasing Monad's blazing-fast speed with playful Delhi traffic theming.

## 🔗 Deployed Contracts (Monad Testnet)

| Contract | Address | Explorer |
|----------|---------|----------|
| **PlayerBadge** | `0xBE679568645D1e0fb17eE9Fb0B70BCd3d1009116` | [View on Explorer](https://testnet.monadexplorer.com/address/0xBE679568645D1e0fb17eE9Fb0B70BCd3d1009116) |
| **TicTacToe** | `0x294645FEB89dC2651DBE2B3299880E0126a5FaFA` | [View on Explorer](https://testnet.monadexplorer.com/address/0x294645FEB89dC2651DBE2B3299880E0126a5FaFA) |

**Network Details:**
- Chain ID: `10143`
- RPC URL: `https://testnet-rpc.monad.xyz`
- Explorer: `https://testnet.monadexplorer.com`
- Faucet: `https://faucet.monad.xyz`

## 🎮 Features

- **Fully On-Chain**: Every move is a real transaction on Monad Testnet
- **Player Badge NFT**: Mint once per wallet with your Delhi-style name
- **Real-Time Updates**: Board updates instantly via contract events
- **Delhi Traffic Theme**: 🚦 (Green Light) vs 🛑 (Red Signal) with playful messages
- **Multi-Game Support**: Create and join multiple games simultaneously
- **Win Celebrations**: Confetti animation with Delhi-style victory messages
- **Mobile Friendly**: Responsive design for demo on any device

## 🚀 Quick Start

### Two Deployment Options

**Option 1: Remix IDE (Easiest - No Setup Required!)**
- Perfect for quick deployment
- Browser-based, no installation needed
- See [REMIX_DEPLOYMENT.md](REMIX_DEPLOYMENT.md) for full guide
- See [REMIX_STEP_BY_STEP.md](REMIX_STEP_BY_STEP.md) for visual walkthrough

**Option 2: Hardhat (For Local Development)**
- Full development environment
- Automated deployment
- See instructions below

### Prerequisites

- Node.js 18+ or 20+
- MetaMask or compatible Web3 wallet
- MON tokens from [Monad Faucet](https://faucet.monad.xyz)

### Installation

```bash
# Install dependencies
npm install

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Configuration

1. Create `.env` file:
```bash
cp .env.example .env
```

2. Add your private key to `.env`:
```
MONAD_RPC_URL=https://testnet-rpc.monad.xyz
PRIVATE_KEY=your_private_key_here
```

⚠️ **Never commit your `.env` file!**

### Deploy Contracts

```bash
# Compile contracts
npx hardhat compile

# Deploy to Monad Testnet
npx hardhat run scripts/deploy.ts --network monadTestnet
```

The deployment script will automatically save contract addresses to `frontend/src/contracts/addresses.json`.

### Run Frontend

```bash
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📋 DEMO FLOW FOR JUDGES

### Preparation (Before Demo)

1. **Get MON Tokens**: Visit [https://faucet.monad.xyz](https://faucet.monad.xyz) and get testnet tokens for 2 wallets
2. **Deploy Contracts**: Run deployment script (takes ~30 seconds)
3. **Test Setup**: Open app in 2 browsers/devices with different wallets
4. **Mint Badges**: Mint player badges for both wallets with fun names like "Delhi Speedster" and "Traffic Warrior"

### Live Demo Script (5 minutes)

#### Part 1: Introduction (30 seconds)
- "Welcome to Delhi Ka Khel - an on-chain Tic Tac Toe game on Monad Testnet!"
- "Every move is a real blockchain transaction, showcasing Monad's speed"
- "Theme: Traffic Light 🚦 vs Red Signal 🛑 - classic Delhi style!"

#### Part 2: Game Creation (1 minute)
- Connect wallet on main screen
- Show player badge (already minted)
- Click "Create New Game"
- Transaction confirms in ~1-2 seconds (highlight Monad's speed!)
- Copy Game ID and show it prominently

#### Part 3: Joining Game (1 minute)
- Switch to second device/browser
- Connect second wallet
- Paste Game ID and click "Join Game"
- Transaction confirms instantly
- Both screens now show active game board

#### Part 4: Playing Game (2 minutes)
- Make moves alternately between two devices
- Highlight:
  - Each move is a blockchain transaction
  - Real-time board updates via events
  - Playful Delhi messages after each move
  - Turn indicators: "Tera Turn Hai! 🚦" / "Waiting for Dost... 🛑"
- Play until win or draw

#### Part 5: Victory & Wrap-up (30 seconds)
- Show win celebration with confetti
- Display message: "Haan Bhai! Traffic Clear Ho Gaya! 🏆"
- Show transaction history on Monad Explorer
- Emphasize: "All moves recorded on-chain, permanent and verifiable!"

### Backup Plan

If network issues occur:
- Have pre-recorded video of gameplay
- Show deployed contracts on Monad Explorer
- Walk through code and architecture

## 🏗️ Architecture

### Smart Contracts

- **PlayerBadge.sol**: ERC-721 NFT for player identification
- **TicTacToe.sol**: Game logic with win/draw detection

### Frontend

- **Vite + React + TypeScript**: Fast, modern development
- **Tailwind CSS**: Delhi traffic-themed styling
- **wagmi + viem**: Type-safe blockchain interactions
- **canvas-confetti**: Win celebrations

### Network

- **Monad Testnet**
  - Chain ID: 10143
  - RPC: https://testnet-rpc.monad.xyz
  - Explorer: https://testnet.monadexplorer.com
  - Faucet: https://faucet.monad.xyz

## 🎯 Game Rules

1. **Mint Badge**: One-time NFT mint with your Delhi name
2. **Create Game**: Player 1 creates game and gets Game ID
3. **Join Game**: Player 2 joins using Game ID
4. **Play**: Players alternate moves (Player 1 = 🚦, Player 2 = 🛑)
5. **Win**: First to get 3 in a row (horizontal, vertical, or diagonal)
6. **Draw**: All cells filled with no winner

## 🔧 Development

### Project Structure

```
delhi-ka-khel/
├── contracts/              # Solidity smart contracts
│   ├── PlayerBadge.sol
│   └── TicTacToe.sol
├── scripts/               # Deployment scripts
│   └── deploy.ts
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── config/       # wagmi configuration
│   │   ├── contracts/    # ABIs and addresses
│   │   ├── types/        # TypeScript types
│   │   └── utils/        # Helper functions
│   └── package.json
├── hardhat.config.ts     # Hardhat configuration
└── package.json
```

### Testing Locally

```bash
# Start local Hardhat node
npx hardhat node

# Deploy to local network
npx hardhat run scripts/deploy.ts --network localhost

# Run frontend
cd frontend
npm run dev
```

## 🎨 Delhi Theme Messages

The app includes playful Delhi traffic-themed messages:

- "Traffic jam ho gaya! 🚧"
- "Signal tod diya! 🚦"
- "Metro le le bhai! 🚇"
- "Horn mat baja, patience rakh! 📯"
- "Carpool karo, pollution kam karo! 🌱"
- And many more!

## 🔐 Security

- OpenZeppelin ERC-721 for battle-tested NFT implementation
- Input validation on all contract functions
- Access control: Only badge holders can play
- Solidity 0.8.28 with built-in overflow protection

## 📝 License

MIT License - Built for Monad Blitz New Delhi 🇮🇳

## 🙏 Acknowledgments

- Monad team for the amazing testnet
- Delhi traffic for endless inspiration 🚦🛑
- All hackathon participants and judges

## 🐛 Troubleshooting

### "Insufficient funds" error
- Get MON tokens from [faucet](https://faucet.monad.xyz)

### "Wrong network" warning or "0 ETH / No changes" in MetaMask
**This is the most common issue!** Your MetaMask is connected to the wrong network.

**Solution:**
1. Open MetaMask
2. Click the network dropdown (top-left)
3. Select "Monad Testnet" (Chain ID: 10143)
4. If not listed, add manually:
   - Network Name: `Monad Testnet`
   - RPC URL: `https://testnet-rpc.monad.xyz`
   - Chain ID: `10143`
   - Currency Symbol: `MON`
   - Block Explorer: `https://testnet.monadexplorer.com`

**Why this happens:**
- Contracts are deployed on Monad Testnet
- If MetaMask is on Ethereum/other network, contracts don't exist there
- Transactions show "0 ETH" and "No changes" because there's nothing to interact with

See [FIX_NETWORK_ERROR.md](FIX_NETWORK_ERROR.md) for detailed troubleshooting.

### Transactions not confirming
- Check Monad Testnet status
- Ensure you have enough MON for gas
- Try increasing gas limit

### Frontend not connecting
- Clear browser cache
- Reconnect wallet
- Check console for errors

## 📞 Support

For issues or questions:
- Check [Monad Docs](https://docs.monad.xyz)
- Visit [Monad Discord](https://discord.gg/monad)

---

**Built with ❤️ for Monad Blitz New Delhi**

*Haan Bhai! Traffic Clear Ho Gaya!* 🏆
