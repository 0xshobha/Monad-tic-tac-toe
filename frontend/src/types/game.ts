// Game types matching smart contract
export enum CellState {
  Empty = 0,
  X = 1,
  O = 2,
}

export enum GameStatus {
  Waiting = 0,
  Active = 1,
  Finished = 2,
}

export interface Game {
  player1: `0x${string}`;
  player2: `0x${string}`;
  currentTurn: `0x${string}`;
  board: CellState[];
  status: GameStatus;
  winner: `0x${string}`;
  isDraw: boolean;
}

export interface PlayerBadge {
  tokenId: bigint;
  playerName: string;
}
