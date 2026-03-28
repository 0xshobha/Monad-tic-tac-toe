import { useWriteContract, useWaitForTransactionReceipt } from 'wagmi';
import { TicTacToeABI, addresses } from '../contracts';
import { useState, useEffect } from 'react';

interface GameCreationProps {
  onGameCreated: (gameId: number) => void;
}

export function GameCreation({ onGameCreated }: GameCreationProps) {
  const [createdGameId, setCreatedGameId] = useState<number | null>(null);

  const { data: hash, writeContract, isPending } = useWriteContract();

  const { isLoading: isConfirming, isSuccess } = useWaitForTransactionReceipt({
    hash,
  });

  useEffect(() => {
    if (isSuccess && hash) {
      // In a real app, we'd parse the event logs to get the game ID
      // For now, we'll use a simple counter approach
      const gameId = Date.now() % 1000; // Temporary solution
      setCreatedGameId(gameId);
      onGameCreated(gameId);
    }
  }, [isSuccess, hash, onGameCreated]);

  const handleCreateGame = () => {
    writeContract({
      address: addresses.ticTacToe as `0x${string}`,
      abi: TicTacToeABI,
      functionName: 'createGame',
    });
  };

  const copyGameId = () => {
    if (createdGameId) {
      navigator.clipboard.writeText(createdGameId.toString());
      alert('Game ID copied! Dost ko bhej de! 📱');
    }
  };

  return (
    <div className="p-6 bg-purple-800 rounded-lg">
      <h3 className="text-2xl font-bold text-white mb-4 text-center">
        🎮 Naya Game Shuru Karo
      </h3>
      
      <button
        onClick={handleCreateGame}
        disabled={isPending || isConfirming}
        className="w-full px-6 py-3 bg-green-500 hover:bg-green-600 text-white rounded-lg font-bold text-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isPending || isConfirming ? 'Creating... ⏳' : 'Create New Game 🚦'}
      </button>
      
      {createdGameId && (
        <div className="mt-4 p-4 bg-green-600 rounded-lg text-white">
          <p className="text-sm mb-2">Game ID:</p>
          <p className="text-2xl font-bold mb-2">{createdGameId}</p>
          <button
            onClick={copyGameId}
            className="w-full px-4 py-2 bg-white text-green-600 rounded-lg font-bold hover:bg-gray-100 transition"
          >
            Copy Game ID 📋
          </button>
          <p className="text-sm mt-2 opacity-80">Dost ko bhej de! 📱</p>
        </div>
      )}
      
      {hash && (
        <p className="text-white text-sm text-center mt-4">
          Transaction: <a href={`https://testnet.monadexplorer.com/tx/${hash}`} target="_blank" rel="noopener noreferrer" className="underline">{hash.slice(0, 10)}...</a>
        </p>
      )}
    </div>
  );
}
