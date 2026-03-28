import { useState } from 'react';
import { useAccount, useReadContract } from 'wagmi';
import { WalletConnect } from './components/WalletConnect';
import { BadgeMinting } from './components/BadgeMinting';
import { GameCreation } from './components/GameCreation';
import { GameJoining } from './components/GameJoining';
import { GameBoard } from './components/GameBoard';
import { PlayerBadgeABI, addresses } from './contracts';
import { monadTestnet } from './config/wagmi';

function App() {
  const { address, isConnected, chain } = useAccount();
  const [currentGameId, setCurrentGameId] = useState<number | null>(null);

  const isCorrectNetwork = chain?.id === monadTestnet.id;

  // Check if user has badge
  const { data: hasBadge } = useReadContract({
    address: addresses.playerBadge as `0x${string}`,
    abi: PlayerBadgeABI,
    functionName: 'hasBadge',
    args: [address],
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-purple-900 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-white mb-2">
            🚦 Delhi Ka Khel 🛑
          </h1>
          <p className="text-xl text-white opacity-80">
            On-Chain Tic Tac Toe on Monad Testnet
          </p>
          <p className="text-sm text-white opacity-60 mt-2">
            Traffic Light vs Red Signal - Let's Play!
          </p>
        </div>

        {/* Wallet Connection */}
        {!isConnected && (
          <div className="max-w-md mx-auto">
            <WalletConnect />
          </div>
        )}

        {/* Show wallet connect component if connected but wrong network */}
        {isConnected && !isCorrectNetwork && (
          <div className="max-w-md mx-auto">
            <WalletConnect />
          </div>
        )}

        {/* Badge Minting */}
        {isConnected && isCorrectNetwork && !hasBadge && (
          <div className="max-w-md mx-auto">
            <BadgeMinting />
          </div>
        )}

        {/* Game Interface */}
        {isConnected && isCorrectNetwork && hasBadge && (
          <div className="space-y-6">
            {/* Game Creation and Joining */}
            {!currentGameId && (
              <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
                <GameCreation onGameCreated={setCurrentGameId} />
                <GameJoining onGameJoined={setCurrentGameId} />
              </div>
            )}

            {/* Game Board */}
            {currentGameId && (
              <div className="max-w-2xl mx-auto">
                <button
                  onClick={() => setCurrentGameId(null)}
                  className="mb-4 px-4 py-2 bg-purple-700 hover:bg-purple-600 text-white rounded-lg transition"
                >
                  ← Back to Games
                </button>
                <GameBoard gameId={currentGameId} />
              </div>
            )}

            {/* Fun Facts */}
            <div className="max-w-2xl mx-auto p-6 bg-purple-800 rounded-lg text-white text-center">
              <p className="text-sm opacity-80">
                💡 Fun Fact: Every move is a real blockchain transaction on Monad Testnet!
              </p>
              <p className="text-xs opacity-60 mt-2">
                Need MON tokens? <a href="https://faucet.monad.xyz" target="_blank" rel="noopener noreferrer" className="underline">Get from faucet</a>
              </p>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 text-white opacity-60 text-sm">
          <p>Built for Monad Blitz New Delhi 🇮🇳</p>
          <p className="mt-2">
            <a href="https://testnet.monadexplorer.com" target="_blank" rel="noopener noreferrer" className="underline">
              View on Monad Explorer
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
