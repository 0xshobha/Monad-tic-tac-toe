import { useAccount, useConnect, useDisconnect } from 'wagmi';
import { monadTestnet } from '../config/wagmi';

export function WalletConnect() {
  const { address, isConnected, chain } = useAccount();
  const { connect, connectors } = useConnect();
  const { disconnect } = useDisconnect();

  const isCorrectNetwork = chain?.id === monadTestnet.id;

  if (isConnected && address) {
    return (
      <div className="flex flex-col items-center gap-4 p-6 bg-purple-800 rounded-lg">
        <div className="text-white text-center">
          <p className="text-sm opacity-80">Connected Wallet</p>
          <p className="font-mono text-lg">
            {address.slice(0, 6)}...{address.slice(-4)}
          </p>
        </div>
        
        {!isCorrectNetwork && (
          <div className="bg-red-600 text-white px-6 py-4 rounded-lg text-center border-2 border-red-400">
            <p className="text-xl font-bold mb-2">⚠️ WRONG NETWORK!</p>
            <p className="mb-3">You're on: {chain?.name || 'Unknown Network'}</p>
            <p className="mb-3">Please switch to <strong>Monad Testnet</strong></p>
            <div className="bg-red-700 p-3 rounded text-sm mb-3">
              <p className="font-bold mb-1">Add Monad Testnet to MetaMask:</p>
              <p className="text-xs">Network: Monad Testnet</p>
              <p className="text-xs">RPC: https://testnet-rpc.monad.xyz</p>
              <p className="text-xs">Chain ID: 10143</p>
              <p className="text-xs">Currency: MON</p>
            </div>
            <p className="text-sm opacity-90">
              After adding, switch to Monad Testnet in MetaMask
            </p>
          </div>
        )}
        
        <button
          onClick={() => disconnect()}
          className="px-6 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg font-bold transition"
        >
          Disconnect
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center gap-4 p-6 bg-purple-800 rounded-lg">
      <h2 className="text-2xl font-bold text-white">🚦 Delhi Ka Khel 🛑</h2>
      <p className="text-white opacity-80 text-center">
        On-Chain Tic Tac Toe on Monad Testnet
      </p>
      <button
        onClick={() => connect({ connector: connectors[0] })}
        className="px-8 py-3 bg-delhi-orange hover:bg-orange-600 text-white rounded-lg font-bold text-lg transition transform hover:scale-105"
      >
        Connect Wallet 🔗
      </button>
      <p className="text-sm text-white opacity-60">
        Need MON tokens? <a href="https://faucet.monad.xyz" target="_blank" rel="noopener noreferrer" className="underline">Get from faucet</a>
      </p>
    </div>
  );
}
