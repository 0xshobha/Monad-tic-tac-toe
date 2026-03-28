import { useState } from 'react';
import { useWriteContract, useWaitForTransactionReceipt } from 'wagmi';
import { TicTacToeABI, addresses } from '../contracts';

interface GameJoiningProps {
  onGameJoined: (gameId: number) => void;
}

export function GameJoining({ onGameJoined }: GameJoiningProps) {
  const [gameId, setGameId] = useState('');

  const { data: hash, writeContract, isPending } = useWriteContract();

  const { isLoading: isConfirming, isSuccess } = useWaitForTransactionReceipt({
    hash,
  });

  const handleJoinGame = () => {
    if (!gameId.trim()) {
      alert('Game ID daal bhai! 🔢');
      return;
    }

    const gameIdNum = parseInt(gameId);
    if (isNaN(gameIdNum)) {
      alert('Valid Game ID daal! 🔍');
      return;
    }

    writeContract({
      address: addresses.ticTacToe as `0x${string}`,
      abi: TicTacToeABI,
      functionName: 'joinGame',
      args: [BigInt(gameIdNum)],
    });

    if (isSuccess) {
      onGameJoined(gameIdNum);
    }
  };

  return (
    <div className="p-6 bg-purple-800 rounded-lg">
      <h3 className="text-2xl font-bold text-white mb-4 text-center">
        🤝 Game Join Karo
      </h3>
      
      <div className="flex flex-col gap-4">
        <input
          type="text"
          placeholder="Enter Game ID"
          value={gameId}
          onChange={(e) => setGameId(e.target.value)}
          className="px-4 py-3 rounded-lg text-lg"
          disabled={isPending || isConfirming}
        />
        
        <button
          onClick={handleJoinGame}
          disabled={isPending || isConfirming || !gameId.trim()}
          className="px-6 py-3 bg-delhi-orange hover:bg-orange-600 text-white rounded-lg font-bold text-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isPending || isConfirming ? 'Joining... ⏳' : 'Join Game 🛑'}
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
