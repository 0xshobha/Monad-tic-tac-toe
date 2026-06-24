# Requirements Document: Delhi Ka Khel – On-Chain Tic Tac Toe

## Introduction

Delhi Ka Khel is a fully on-chain Tic Tac Toe game built for Monad Testnet, themed around Delhi's chaotic traffic culture. The system enables two players to compete in a blockchain-based game where every move is recorded as a transaction. Players must mint a one-time "Delhi Player Badge" NFT before participating. Games are created and joined via unique game IDs, with real-time board updates via contract events. The system provides instant win/draw detection and maintains a playful Delhi traffic theme throughout the user experience.

## Glossary

- **Player_Badge_Contract**: ERC-721 NFT contract that issues unique player badges
- **TicTacToe_Contract**: Smart contract managing game logic, state, and validation
- **Frontend**: React-based web application providing the user interface
- **Game_ID**: Unique identifier for each game instance
- **Board**: 3x3 grid represented as array of 9 cells (indices 0-8)
- **Cell_State**: Enum representing Empty (0), X (1), or O (2)
- **Game_Status**: Enum representing Waiting (0), Active (1), or Finished (2)
- **Current_Turn**: Address of the player who can make the next move
- **Monad_Testnet**: Blockchain network where contracts are deployed
- **Wallet**: User's blockchain wallet (e.g., MetaMask)
- **Badge_Holder**: Address that has minted a Player Badge NFT
- **Win_Pattern**: Three cells in a row (horizontal, vertical, or diagonal)
- **Event_Listener**: Frontend component monitoring blockchain events

## Requirements

### Requirement 1: Player Badge Management

**User Story:** As a player, I want to mint a unique player badge once per wallet, so that I can participate in games with a personalized identity.

#### Acceptance Criteria

1. WHEN a user calls mintBadge with a valid player name, THE Player_Badge_Contract SHALL mint an ERC-721 NFT to the caller's address
2. WHEN a user attempts to mint a second badge, THE Player_Badge_Contract SHALL reject the transaction
3. WHEN querying badge status for an address, THE Player_Badge_Contract SHALL return true if that address owns a badge
4. WHEN querying player name for a badge holder, THE Player_Badge_Contract SHALL return the name provided during minting
5. THE Player_Badge_Contract SHALL enforce that player names are non-empty strings

### Requirement 2: Game Creation

**User Story:** As a player, I want to create a new game, so that I can invite another player to compete.

#### Acceptance Criteria

1. WHEN a badge holder calls createGame, THE TicTacToe_Contract SHALL generate a unique Game_ID
2. WHEN a game is created, THE TicTacToe_Contract SHALL initialize the Board with all cells set to Empty
3. WHEN a game is created, THE TicTacToe_Contract SHALL set Game_Status to Waiting
4. WHEN a game is created, THE TicTacToe_Contract SHALL set player1 to the caller's address
5. WHEN a game is created, THE TicTacToe_Contract SHALL emit a GameCreated event with the Game_ID and player1 address
6. IF a non-badge holder attempts to create a game, THEN THE TicTacToe_Contract SHALL reject the transaction

### Requirement 3: Game Joining

**User Story:** As a player, I want to join an existing game using a Game_ID, so that I can play against the game creator.

#### Acceptance Criteria

1. WHEN a badge holder calls joinGame with a valid Game_ID, THE TicTacToe_Contract SHALL set player2 to the caller's address
2. WHEN a player joins a game, THE TicTacToe_Contract SHALL change Game_Status from Waiting to Active
3. WHEN a player joins a game, THE TicTacToe_Contract SHALL set Current_Turn to player1
4. WHEN a player joins a game, THE TicTacToe_Contract SHALL emit a GameJoined event with the Game_ID and player2 address
5. IF a non-badge holder attempts to join a game, THEN THE TicTacToe_Contract SHALL reject the transaction
6. IF a user attempts to join a non-existent Game_ID, THEN THE TicTacToe_Contract SHALL reject the transaction
7. IF a user attempts to join a game that is not in Waiting status, THEN THE TicTacToe_Contract SHALL reject the transaction
8. IF player1 attempts to join their own game, THEN THE TicTacToe_Contract SHALL reject the transaction

### Requirement 4: Move Execution

**User Story:** As a player, I want to make moves on the game board, so that I can progress toward winning the game.

#### Acceptance Criteria

1. WHEN the Current_Turn player calls makeMove with a valid position, THE TicTacToe_Contract SHALL update the Board at that position with the player's symbol
2. WHEN a move is made, THE TicTacToe_Contract SHALL switch Current_Turn to the other player
3. WHEN a move is made, THE TicTacToe_Contract SHALL emit a MoveMade event with Game_ID, player address, and position
4. IF a player attempts to move when it is not their turn, THEN THE TicTacToe_Contract SHALL reject the transaction
5. IF a player attempts to move to an occupied cell, THEN THE TicTacToe_Contract SHALL reject the transaction
6. IF a player attempts to move to a position outside 0-8 range, THEN THE TicTacToe_Contract SHALL reject the transaction
7. IF a player attempts to move in a game with status other than Active, THEN THE TicTacToe_Contract SHALL reject the transaction
8. WHEN a move is made, THE TicTacToe_Contract SHALL check for win or draw conditions before completing the transaction

### Requirement 5: Win Detection

**User Story:** As a player, I want the system to automatically detect when I win, so that the game concludes correctly and I receive recognition.

#### Acceptance Criteria

1. WHEN a player completes a Win_Pattern, THE TicTacToe_Contract SHALL set Game_Status to Finished
2. WHEN a win is detected, THE TicTacToe_Contract SHALL set the winner field to the winning player's address
3. WHEN a win is detected, THE TicTacToe_Contract SHALL emit a GameEnded event with Game_ID and winner address
4. THE TicTacToe_Contract SHALL check all eight Win_Patterns: three rows, three columns, and two diagonals
5. WHEN checking for a win, THE TicTacToe_Contract SHALL verify that all three cells in a pattern contain the same non-Empty symbol
6. WHEN a game is won, THE Frontend SHALL display a victory message with confetti animation

### Requirement 6: Draw Detection

**User Story:** As a player, I want the system to detect when the game ends in a draw, so that neither player is incorrectly declared the winner.

#### Acceptance Criteria

1. WHEN all nine Board cells are filled and no Win_Pattern exists, THE TicTacToe_Contract SHALL set Game_Status to Finished
2. WHEN a draw is detected, THE TicTacToe_Contract SHALL set the isDraw field to true
3. WHEN a draw is detected, THE TicTacToe_Contract SHALL emit a GameEnded event indicating a draw
4. WHEN a draw is detected, THE TicTacToe_Contract SHALL ensure the winner field remains address(0)
5. WHEN a game ends in a draw, THE Frontend SHALL display a draw message

### Requirement 7: Game State Immutability

**User Story:** As a player, I want completed games to be immutable, so that results cannot be altered after the game ends.

#### Acceptance Criteria

1. WHEN Game_Status is Finished, THE TicTacToe_Contract SHALL reject any makeMove attempts for that Game_ID
2. WHEN a game is finished, THE TicTacToe_Contract SHALL prevent any modifications to the Board state
3. WHEN querying a finished game, THE TicTacToe_Contract SHALL return the final game state accurately

### Requirement 8: Real-Time Board Updates

**User Story:** As a player, I want to see board updates in real-time, so that I can follow the game progress without manual refreshing.

#### Acceptance Criteria

1. WHEN a MoveMade event is emitted, THE Event_Listener SHALL capture the event within 2 seconds
2. WHEN a move event is received, THE Frontend SHALL update the Board display to reflect the new Cell_State
3. WHEN a GameJoined event is emitted, THE Event_Listener SHALL notify the Frontend that the game has started
4. WHEN a GameEnded event is emitted, THE Event_Listener SHALL trigger the appropriate victory or draw display
5. WHILE monitoring events, THE Frontend SHALL maintain accurate synchronization with on-chain game state

### Requirement 9: Wallet Connection

**User Story:** As a user, I want to connect my wallet to the application, so that I can interact with the blockchain and play games.

#### Acceptance Criteria

1. WHEN a user clicks the connect wallet button, THE Frontend SHALL prompt the Wallet to request connection
2. WHEN the Wallet approves connection, THE Frontend SHALL display the connected address
3. WHEN the Wallet rejects connection, THE Frontend SHALL display an appropriate error message
4. WHILE the Wallet is not connected, THE Frontend SHALL disable all game interaction features
5. WHEN the Wallet disconnects, THE Frontend SHALL return to the connection prompt state
6. THE Frontend SHALL verify that the Wallet is connected to Monad_Testnet before allowing transactions

### Requirement 10: User Interface Theme

**User Story:** As a player, I want a playful Delhi traffic-themed interface, so that the game is entertaining and culturally relevant for the hackathon demo.

#### Acceptance Criteria

1. THE Frontend SHALL use traffic-themed symbols: 🚦 for X and 🛑 for O
2. WHEN displaying turn status, THE Frontend SHALL show Delhi-style messages like "Tera Turn Hai! 🚦" or "Waiting for Dost... 🛑"
3. WHEN a move is made, THE Frontend SHALL display a random Delhi traffic-related joke or phrase
4. WHEN an error occurs, THE Frontend SHALL display error messages in Delhi colloquial style
5. THE Frontend SHALL use a color scheme inspired by Delhi traffic and urban aesthetics
6. WHEN a player wins, THE Frontend SHALL display a celebratory message with Delhi cultural references

### Requirement 11: Transaction Confirmation

**User Story:** As a player, I want clear feedback on transaction status, so that I know when my actions are being processed and completed.

#### Acceptance Criteria

1. WHEN a user initiates a transaction, THE Frontend SHALL display a pending status indicator
2. WHEN a transaction is confirmed on-chain, THE Frontend SHALL display a success notification
3. IF a transaction fails, THEN THE Frontend SHALL display an error message with the failure reason
4. WHEN waiting for transaction confirmation, THE Frontend SHALL show an estimated time based on Monad_Testnet block times
5. THE Frontend SHALL provide transaction hash links to Monad Testnet Explorer for all completed transactions

### Requirement 12: Gas Management

**User Story:** As a player, I want to know if I have sufficient funds for transactions, so that I can obtain testnet tokens before attempting to play.

#### Acceptance Criteria

1. WHEN a user attempts a transaction with insufficient MON balance, THE Frontend SHALL detect this before submission
2. IF insufficient balance is detected, THEN THE Frontend SHALL display a message directing the user to the Monad faucet
3. THE Frontend SHALL provide a direct link to https://faucet.monad.xyz when gas is insufficient
4. WHEN displaying transaction prompts, THE Frontend SHALL show estimated gas costs

### Requirement 13: Game State Queries

**User Story:** As a player, I want to view current game state, so that I can understand the board position and game status.

#### Acceptance Criteria

1. WHEN a user requests game state for a valid Game_ID, THE TicTacToe_Contract SHALL return the complete Game struct
2. WHEN querying the Board, THE TicTacToe_Contract SHALL return all nine Cell_State values in order
3. THE TicTacToe_Contract SHALL provide view functions that do not modify state or consume gas
4. WHEN the Frontend loads a game, THE Frontend SHALL query and display current Board state, player addresses, and Current_Turn

### Requirement 14: Input Validation

**User Story:** As a developer, I want comprehensive input validation, so that invalid data cannot corrupt game state or cause unexpected behavior.

#### Acceptance Criteria

1. WHEN validating position inputs, THE TicTacToe_Contract SHALL ensure values are between 0 and 8 inclusive
2. WHEN validating Game_ID inputs, THE TicTacToe_Contract SHALL ensure the game exists before processing
3. WHEN validating player names, THE Player_Badge_Contract SHALL ensure strings are non-empty
4. THE Frontend SHALL validate all user inputs before submitting transactions to prevent unnecessary gas costs
5. IF validation fails, THEN THE system SHALL provide clear error messages indicating the validation failure reason

### Requirement 15: Event Emission Guarantees

**User Story:** As a frontend developer, I want guaranteed event emissions for all state changes, so that the UI can reliably track game progress.

#### Acceptance Criteria

1. WHEN createGame completes successfully, THE TicTacToe_Contract SHALL emit a GameCreated event
2. WHEN joinGame completes successfully, THE TicTacToe_Contract SHALL emit a GameJoined event
3. WHEN makeMove completes successfully, THE TicTacToe_Contract SHALL emit a MoveMade event
4. WHEN a game ends, THE TicTacToe_Contract SHALL emit a GameEnded event
5. WHEN mintBadge completes successfully, THE Player_Badge_Contract SHALL emit a Transfer event per ERC-721 standard
6. THE contracts SHALL emit events before transaction completion to ensure they are included in transaction receipts

### Requirement 16: Performance Targets

**User Story:** As a demo presenter, I want fast transaction confirmations and responsive UI, so that the hackathon demo runs smoothly without awkward delays.

#### Acceptance Criteria

1. WHEN a transaction is submitted to Monad_Testnet, THE system SHALL confirm within 2 seconds under normal network conditions
2. WHEN the Frontend receives an event, THE Frontend SHALL update the UI within 500 milliseconds
3. WHEN the Frontend loads initially, THE Frontend SHALL render within 2 seconds
4. THE TicTacToe_Contract SHALL optimize gas usage to minimize transaction costs
5. THE Frontend SHALL support at least 10 simultaneous games without performance degradation

### Requirement 17: Error Recovery

**User Story:** As a player, I want the system to handle errors gracefully, so that temporary issues do not prevent me from continuing to play.

#### Acceptance Criteria

1. IF a network request fails, THEN THE Frontend SHALL implement retry logic with exponential backoff
2. IF the Event_Listener loses connection, THEN THE Frontend SHALL automatically reconnect and resync game state
3. IF a transaction times out, THEN THE Frontend SHALL provide a retry option to the user
4. WHEN an error occurs, THE Frontend SHALL log error details for debugging while showing user-friendly messages
5. THE Frontend SHALL implement fallback polling every 3 seconds if event listening fails

### Requirement 18: Multi-Game Support

**User Story:** As a player, I want to participate in multiple games simultaneously, so that I can play with different opponents concurrently.

#### Acceptance Criteria

1. THE TicTacToe_Contract SHALL allow a single address to be player1 or player2 in multiple games
2. WHEN displaying active games, THE Frontend SHALL show a list of all games involving the connected address
3. WHEN switching between games, THE Frontend SHALL load and display the correct Board state for the selected Game_ID
4. THE system SHALL maintain independent state for each Game_ID without interference

### Requirement 19: Smart Contract Security

**User Story:** As a developer, I want secure smart contracts, so that game integrity is maintained and exploits are prevented.

#### Acceptance Criteria

1. THE TicTacToe_Contract SHALL use Solidity 0.8.28 built-in overflow protection
2. THE Player_Badge_Contract SHALL use OpenZeppelin's audited ERC-721 implementation
3. THE contracts SHALL validate all inputs with require statements before state modifications
4. THE contracts SHALL implement access control to ensure only Badge_Holders can play
5. THE contracts SHALL prevent reentrancy attacks on state-changing functions
6. WHEN a game is finished, THE TicTacToe_Contract SHALL prevent any further state modifications for that Game_ID

### Requirement 20: Deployment and Configuration

**User Story:** As a developer, I want straightforward deployment to Monad Testnet, so that the demo can be set up quickly for the hackathon.

#### Acceptance Criteria

1. THE deployment scripts SHALL deploy Player_Badge_Contract first and pass its address to TicTacToe_Contract
2. THE deployment process SHALL verify contract deployment on Monad Testnet Explorer
3. THE Frontend SHALL load contract addresses and ABIs from configuration files
4. THE system SHALL provide clear documentation for deploying to Monad_Testnet
5. THE deployment SHALL complete within 5 minutes under normal network conditions
