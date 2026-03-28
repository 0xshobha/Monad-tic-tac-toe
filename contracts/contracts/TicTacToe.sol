// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

interface IPlayerBadge {
    function hasBadge(address player) external view returns (bool);
}

/**
 * @title TicTacToe
 * @dev On-chain Tic Tac Toe game for Monad Testnet - Delhi Ka Khel! 🚦 vs 🛑
 */
contract TicTacToe {
    // Enums
    enum GameStatus { Waiting, Active, Finished }
    enum CellState { Empty, X, O }

    // Structs
    struct Game {
        address player1;
        address player2;
        address currentTurn;
        CellState[9] board;
        GameStatus status;
        address winner;
        bool isDraw;
    }

    // State variables
    mapping(uint256 => Game) public games;
    uint256 private _gameIdCounter;
    address public playerBadgeContract;

    // Events
    event GameCreated(uint256 indexed gameId, address indexed player1);
    event GameJoined(uint256 indexed gameId, address indexed player2);
    event MoveMade(uint256 indexed gameId, address indexed player, uint8 position);
    event GameEnded(uint256 indexed gameId, address winner, bool isDraw);

    // Modifier
    modifier onlyBadgeHolder() {
        require(IPlayerBadge(playerBadgeContract).hasBadge(msg.sender), "Must have player badge");
        _;
    }

    constructor(address _playerBadgeContract) {
        playerBadgeContract = _playerBadgeContract;
        _gameIdCounter = 1;
    }

    /**
     * @dev Create a new game - Traffic light ready! 🚦
     * @return gameId The created game ID
     */
    function createGame() external onlyBadgeHolder returns (uint256) {
        uint256 gameId = _gameIdCounter;
        
        Game storage game = games[gameId];
        game.player1 = msg.sender;
        game.status = GameStatus.Waiting;
        // board is already initialized to Empty (default)
        
        _gameIdCounter++;
        emit GameCreated(gameId, msg.sender);
        
        return gameId;
    }

    /**
     * @dev Join an existing game - Let's play! 🛑
     * @param gameId The game ID to join
     */
    function joinGame(uint256 gameId) external onlyBadgeHolder {
        Game storage game = games[gameId];
        
        require(game.player1 != address(0), "Game does not exist");
        require(game.status == GameStatus.Waiting, "Game not available");
        require(game.player1 != msg.sender, "Cannot join own game");
        
        game.player2 = msg.sender;
        game.status = GameStatus.Active;
        game.currentTurn = game.player1; // Player 1 goes first
        
        emit GameJoined(gameId, msg.sender);
    }

    /**
     * @dev Make a move - Tera turn hai! 🚦
     * @param gameId The game ID
     * @param position The board position (0-8)
     */
    function makeMove(uint256 gameId, uint8 position) external {
        Game storage game = games[gameId];
        
        require(game.player1 != address(0), "Game does not exist");
        require(game.status == GameStatus.Active, "Game not active");
        require(position < 9, "Invalid position");
        require(game.board[position] == CellState.Empty, "Cell occupied");
        require(game.currentTurn == msg.sender, "Not your turn");
        
        // Determine player symbol
        CellState symbol = (msg.sender == game.player1) ? CellState.X : CellState.O;
        game.board[position] = symbol;
        
        emit MoveMade(gameId, msg.sender, position);
        
        // Check for win or draw
        _checkWinOrDraw(gameId);
        
        // Switch turn if game still active
        if (game.status == GameStatus.Active) {
            game.currentTurn = (game.currentTurn == game.player1) ? game.player2 : game.player1;
        }
    }

    /**
     * @dev Internal function to check win or draw conditions
     * @param gameId The game ID
     */
    function _checkWinOrDraw(uint256 gameId) internal {
        Game storage game = games[gameId];
        
        // Check for winner
        (bool hasWinner, address winner) = _checkWinner(gameId);
        if (hasWinner) {
            game.status = GameStatus.Finished;
            game.winner = winner;
            emit GameEnded(gameId, winner, false);
            return;
        }
        
        // Check for draw
        if (_checkDraw(gameId)) {
            game.status = GameStatus.Finished;
            game.isDraw = true;
            emit GameEnded(gameId, address(0), true);
        }
    }

    /**
     * @dev Check if there's a winner - Traffic clear ho gaya! 🏆
     * @param gameId The game ID
     * @return hasWinner True if there's a winner
     * @return winner The winner's address
     */
    function _checkWinner(uint256 gameId) internal view returns (bool, address) {
        Game storage game = games[gameId];
        
        // Winning patterns: rows, columns, diagonals
        uint8[3][8] memory patterns = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columns
            [0, 4, 8], [2, 4, 6]              // Diagonals
        ];
        
        for (uint i = 0; i < 8; i++) {
            uint8 a = patterns[i][0];
            uint8 b = patterns[i][1];
            uint8 c = patterns[i][2];
            
            if (game.board[a] != CellState.Empty &&
                game.board[a] == game.board[b] &&
                game.board[b] == game.board[c]) {
                // Found a winner!
                address winner = (game.board[a] == CellState.X) ? game.player1 : game.player2;
                return (true, winner);
            }
        }
        
        return (false, address(0));
    }

    /**
     * @dev Check if the game is a draw - Traffic jam! 🚧
     * @param gameId The game ID
     * @return True if it's a draw
     */
    function _checkDraw(uint256 gameId) internal view returns (bool) {
        Game storage game = games[gameId];
        
        // Check if all cells are filled
        for (uint i = 0; i < 9; i++) {
            if (game.board[i] == CellState.Empty) {
                return false;
            }
        }
        
        return true;
    }

    /**
     * @dev Get complete game state
     * @param gameId The game ID
     * @return The game struct
     */
    function getGame(uint256 gameId) external view returns (Game memory) {
        return games[gameId];
    }

    /**
     * @dev Get game board
     * @param gameId The game ID
     * @return The board array
     */
    function getBoard(uint256 gameId) external view returns (CellState[9] memory) {
        return games[gameId].board;
    }
}
