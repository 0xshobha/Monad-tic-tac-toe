import { useAccount, useReadContract, useWriteContract, useWatchContractEvent } from 'wagmi';
import { TicTacToeABI, addresses } from '../contracts';
import { CellState, GameStatus } from '../types/game';
import { getRandomDelhiJoke } from '../utils/delhiMessages';
import { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';

interface GameBoardProps {
  gameId: number;
}

export function GameBoard({ gameId }: GameBoardProps) {
  const { address } = useAccount();
  const [message, setMessage] = useState('');
  const [showMessage, setShowMessage] = useState(false);

  // Read game state
  const { data: game, refetch } = useReadContract({
    address: addresses.ticTacToe as `0x${string}`,
    abi: TicTacToeABI,
    functionName: 'getGame',
    args: [BigInt(gameId)],
  });

  // Make move
  const { writeContract, isPending } = useWriteContract();

  // Watch for move events
  useWatchContractEvent({
    address: addresses.ticTacToe as `0x${string}`,
    abi: TicTacToeABI,
    eventName: 'MoveMade',
    onLogs: () => {
      refetch();
      const joke = getRandomDelhiJoke();
      setMessage(joke);
      setShowMessage(true);
      setTimeout(() => setShowMessage(false), 3000);
    },
  });

  // Watch for game end
  useWatchContractEvent({
    address: addresses.ticTacToe as `0x${string}`,
    abi: TicTacToeABI,
    eventName: 'GameEnded',
    onLogs: (logs) => {
      refetch();
      const log = logs[0];
      if (log.args.isDraw) {
        setMessage('Arre Yaar, Traffic Jam! Next Round? 🚧');
      } else if (log.args.winner?.toLowerCase() === address?.toLowerCase()) {
        setMessage('Haan Bhai! Traffic Clear Ho Gaya! 🏆');
        confetti({
          particleCount: 100,
          spread: 70,
          origin: { y: 0.6 },
          colors: ['#581c87', '#f97316', '#fbbf24'],
        });
      } else {
        setMessage('Better luck next time! Metro le le bhai! 🚇');
      }
      setShowMessage(true);
    },
  });

  const handleCellClick = (position: number) => {
    if (!game || isPending) return;

    const [player1, player2, currentTurn, board, status] = game as any;

    if (status !== GameStatus.Active) {
      alert('Game khatam ho gaya! 🏁');
      return;
    }

    if (currentTurn.toLowerCase() !== address?.toLowerCase()) {
      alert('Arre ruk ja, tera turn nahi hai! ⏸️');
      return;
    }

    if (board[position] !== CellState.Empty) {
      alert('Arre bhai, wahan already gaadi khadi hai! 🚗');
      return;
    }

    writeContract({
      address: addresses.ticTacToe as `0x${string}`,
      abi: TicTacToeABI,
      functionName: 'makeMove',
      args: [BigInt(gameId), position],
    });
  };

  if (!game) {
    return (
      <div className="p-6 bg-purple-800 rounded-lg text-white text-center">
        <p>Loading game... ⏳</p>
      </div>
    );
  }

  const [player1, player2, currentTurn, board, status] = game as any;

  const getCellSymbol = (cell: CellState) => {
    if (cell === CellState.X) return '🚦';
    if (cell === CellState.O) return '🛑';
    return '';
  };

  const isMyTurn = currentTurn.toLowerCase() === address?.toLowerCase();
  const isActive = status === GameStatus.Active;

  return (
    <div className="p-6 bg-purple-900 rounded-lg">
      <h3 className="text-2xl font-bold text-white mb-4 text-center">
        Game #{gameId}
      </h3>

      {/* Status */}
      <div className="mb-4 p-4 bg-purple-800 rounded-lg text-white text-center">
        {status === GameStatus.Waiting && <p>Waiting for player 2... ⏳</p>}
        {status === GameStatus.Active && (
          <p className="text-xl font-bold">
            {isMyTurn ? 'Tera Turn Hai! 🚦' : 'Waiting for Dost... 🛑'}
          </p>
        )}
        {status === GameStatus.Finished && (
          <p className="text-xl font-bold">Game Khatam! 🏁</p>
        )}
      </div>

      {/* Board */}
      <div className="grid grid-cols-3 gap-2 mb-4 max-w-md mx-auto">
        {Array.from({ length: 9 }).map((_, i) => (
          <button
            key={i}
            onClick={() => handleCellClick(i)}
            disabled={!isActive || !isMyTurn || isPending}
            className="aspect-square bg-purple-700 hover:bg-purple-600 rounded-lg text-6xl flex items-center justify-center transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {getCellSymbol(board[i])}
          </button>
        ))}
      </div>

      {/* Message */}
      {showMessage && (
        <div className="p-4 bg-delhi-orange rounded-lg text-white text-center font-bold animate-bounce">
          {message}
        </div>
      )}

      {/* Players */}
      <div className="mt-4 text-white text-sm space-y-2">
        <p>🚦 Player 1: {player1.slice(0, 6)}...{player1.slice(-4)}</p>
        {player2 !== '0x0000000000000000000000000000000000000000' && (
          <p>🛑 Player 2: {player2.slice(0, 6)}...{player2.slice(-4)}</p>
        )}
      </div>
    </div>
  );
}
