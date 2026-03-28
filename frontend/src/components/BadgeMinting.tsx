import { useState } from 'react';
import { useAccount, useReadContract, useWriteContract, useWaitForTransactionReceipt } from 'wagmi';
import { PlayerBadgeABI, addresses } from '../contracts';

export function BadgeMinting() {
  const { address } = useAccount();
  const [playerName, setPlayerName] = useState('');

  // Check if user has badge
  const { data: hasBadge, refetch } = useReadContract({
    address: addresses.playerBadge as `0x${string}`,
    abi: PlayerBadgeABI,
    functionName: 'hasBadge',
    args: [address],
  });

  // Mint badge
  const { data: hash, writeContract, isPending } = useWriteContract();

  const { isLoading: isConfirming } = useWaitForTransactionReceipt({
    hash,
  });

  const handleMint = () => {
    if (!playerName.trim()) {
      alert('Arre bhai, naam toh daal! 📝');
      return;
    }

    writeContract({
      address: addresses.playerBadge as `0x${string}`,
      abi: PlayerBadgeABI,
      functionName: 'mintBadge',
      args: [playerName],
    });
  };

  if (hasBadge) {
    return (
      <div className="p-6 bg-green-600 rounded-lg text-white text-center">
        <p className="text-2xl mb-2">✅ Badge Mil Gaya!</p>
        <p className="opacity-80">You're ready to play!</p>
      </div>
    );
  }

  return (
    <div className="p-6 bg-purple-800 rounded-lg">
      <h3 className="text-2xl font-bold text-white mb-4 text-center">
        🎫 Pehle Badge Le Le!
      </h3>
      <p className="text-white opacity-80 mb-4 text-center">
        Mint your Delhi Player Badge to start playing
      </p>
      
      <div className="flex flex-col gap-4">
        <input
          type="text"
          placeholder="Enter your Delhi name (e.g., Traffic Warrior)"
          value={playerName}
          onChange={(e) => setPlayerName(e.target.value)}
          className="px-4 py-3 rounded-lg text-lg"
          disabled={isPending || isConfirming}
        />
        
        <button
          onClick={handleMint}
          disabled={isPending || isConfirming || !playerName.trim()}
          className="px-6 py-3 bg-delhi-orange hover:bg-orange-600 text-white rounded-lg font-bold text-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isPending || isConfirming ? 'Minting... ⏳' : 'Mint Badge 🎫'}
        </button>
        
        {hash && (
          <p className="text-white text-sm text-center">
            Transaction: <a href={`https://testnet.monadexplorer.com/tx/${hash}`} target="_blank" rel="noopener noreferrer" className="underline">{hash.slice(0, 10)}...</a>
          </p>
        )}
      </div>
    </div>
  );
}
