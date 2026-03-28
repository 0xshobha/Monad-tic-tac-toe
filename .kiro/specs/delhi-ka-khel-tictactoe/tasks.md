# Implementation Plan: Delhi Ka Khel – On-Chain Tic Tac Toe

## Overview

This implementation plan breaks down the Delhi Ka Khel project into sequential, actionable tasks for building a fully on-chain Tic Tac Toe game on Monad Testnet. The project uses Hardhat for smart contract development, Vite + React + TypeScript for the frontend, and wagmi/viem for blockchain interactions. Each task builds incrementally toward a demo-ready dApp with Delhi traffic theming.

## Tasks

- [x] 1. Initialize project structure and dependencies
  - Create root directory with Hardhat and Vite workspaces
  - Initialize Hardhat project in `/contracts` directory
  - Initialize Vite + React + TypeScript project in `/frontend` directory
  - Install Hardhat dependencies: hardhat, @nomicfoundation/hardhat-toolbox, @openzeppelin/contracts
  - Install frontend dependencies: react, typescript, vite, tailwindcss, wagmi, viem, @tanstack/react-query
  - Configure Tailwind CSS with Delhi traffic color scheme (purple-900 base)
  - Set up TypeScript configurations for both workspaces
  - Create `.env.example` files for contract addresses and RPC URLs
  - _Requirements: 20.3, 20.4_

- [x] 2. Implement PlayerBadge smart contract
  - [x] 2.1 Create PlayerBadge.sol with ERC-721 base
    - Import OpenZeppelin ERC-721 contract
    - Define contract inheriting from ERC721
    - Add state variables: `mapping(address => string) public playerNames`, `mapping(address => bool) public hasBadge`, `uint256 private _tokenIdCounter`
    - Implement constructor with name "Delhi Player Badge" and symbol "DPB"
    - _Requirements: 1.1, 1.3, 19.2_
  
  - [x] 2.2 Implement mintBadge function
    - Add `mintBadge(string memory playerName)` external function
    - Validate player name is non-empty with `require(bytes(playerName).length > 0, "Name cannot be empty")`
    - Validate address doesn't already have badge with `require(!hasBadge[msg.sender], "Already has badge")`
    - Mint NFT using `_safeMint(msg.sender, _tokenIdCounter)`
    - Store player name in `playerNames[msg.sender]`
    - Set `hasBadge[msg.sender] = true`
    - Increment `_tokenIdCounter`
    - _Requirements: 1.1, 1.2, 1.5, 14.3_
  
  - [x] 2.3 Implement view functions
    - Add `getPlayerName(address player)` external view returns (string memory)
    - Return `playerNames[player]`
    - _Requirements: 1.4, 13.3_
  
  - [ ]* 2.4 Write property test for PlayerBadge
    - **Property 1: Badge Minting Round Trip**
    - **Property 2: Badge Uniqueness**
    - **Property 3: Empty Name Rejection**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.4, 1.5, 14.3**

- [ ] 3. Implement TicTacToe smart contract core structure
  - [ ] 3.1 Create TicTacToe.sol with enums and structs
    - Define `enum GameStatus { Waiting, Active, Finished }`
    - Define `enum CellState { Empty, X, O }`
    - Define `struct Game` with fields: player1, player2, currentTurn (all address), board (CellState[9]), status (GameStatus), winner (address), isDraw (bool)
    - Add state variables: `mapping(uint256 => Game) public games`, `uint256 private _gameIdCounter`, `address public playerBadgeContract`
    - Implement constructor accepting `address _playerBadgeContract`
    - _Requirements: 2.1, 2.2, 7.3, 13.1_
  
  - [ ] 3.2 Define contract events
    - Add `event GameCreated(uint256 indexed gameId, address indexed player1)`
    - Add `event GameJoined(uint256 indexed gameId, address indexed player2)`
    - Add `event MoveMade(uint256 indexed gameId, address indexed player, uint8 position)`
    - Add `event GameEnded(uint256 indexed gameId, address winner, bool isDraw)`
    - _Requirements: 2.5, 3.4, 4.3, 5.3, 6.3, 15.1, 15.2, 15.3, 15.4_
  
  - [ ] 3.3 Implement badge validation modifier
    - Create `modifier onlyBadgeHolder()` that calls `IPlayerBadge(playerBadgeContract).hasBadge(msg.sender)`
    - Require badge holder with message "Must have player badge"
    - _Requirements: 2.6, 3.5, 19.4_

- [ ] 4. Implement game creation and joining
  - [ ] 4.1 Implement createGame function
    - Add `createGame()` external onlyBadgeHolder returns (uint256)
    - Increment `_gameIdCounter`
    - Initialize new Game struct with player1 = msg.sender, status = Waiting, all board cells = Empty
    - Store in `games[_gameIdCounter]`
    - Emit `GameCreated(_gameIdCounter, msg.sender)`
    - Return `_gameIdCounter`
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 15.1_
  
  - [ ]* 4.2 Write property tests for game creation
    - **Property 4: Game ID Uniqueness**
    - **Property 5: New Game Initialization**
    - **Property 6: Badge Holder Access Control**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.6, 19.4**
  
  - [ ] 4.3 Implement joinGame function
    - Add `joinGame(uint256 gameId)` external onlyBadgeHolder
    - Validate game exists with `require(games[gameId].player1 != address(0), "Game does not exist")`
    - Validate game status is Waiting with `require(games[gameId].status == GameStatus.Waiting, "Game not available")`
    - Validate caller is not player1 with `require(games[gameId].player1 != msg.sender, "Cannot join own game")`
    - Set `games[gameId].player2 = msg.sender`
    - Set `games[gameId].status = GameStatus.Active`
    - Set `games[gameId].currentTurn = games[gameId].player1`
    - Emit `GameJoined(gameId, msg.sender)`
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.6, 3.7, 3.8, 14.2, 15.2_
  
  - [ ]* 4.4 Write property tests for game joining
    - **Property 7: Game Join State Transition**
    - **Property 8: Invalid Join Rejection**
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.6, 3.7, 3.8**

- [ ] 5. Implement move execution and validation
  - [ ] 5.1 Implement makeMove function
    - Add `makeMove(uint256 gameId, uint8 position)` external
    - Validate game exists with `require(games[gameId].player1 != address(0), "Game does not exist")`
    - Validate game is active with `require(games[gameId].status == GameStatus.Active, "Game not active")`
    - Validate position range with `require(position < 9, "Invalid position")`
    - Validate cell is empty with `require(games[gameId].board[position] == CellState.Empty, "Cell occupied")`
    - Validate current turn with `require(games[gameId].currentTurn == msg.sender, "Not your turn")`
    - Determine player symbol (X if player1, O if player2)
    - Set `games[gameId].board[position]` to player symbol
    - Emit `MoveMade(gameId, msg.sender, position)`
    - Call internal `_checkWinOrDraw(gameId)` function
    - Switch current turn to other player if game still active
    - _Requirements: 4.1, 4.4, 4.5, 4.7, 7.1, 14.1, 14.2, 15.3, 19.3_
  
  - [ ] 5.2 Implement turn switching logic
    - After move validation and board update, toggle currentTurn
    - If msg.sender == player1, set currentTurn = player2
    - If msg.sender == player2, set currentTurn = player1
    - _Requirements: 4.2_
  
  - [ ]* 5.3 Write property tests for move execution
    - **Property 9: Move Validity**
    - **Property 10: Turn Alternation**
    - **Property 14: Board Immutability After Completion**
    - **Validates: Requirements 4.1, 4.2, 4.4, 4.5, 4.7, 7.1, 7.2, 19.6**

- [ ] 6. Implement win and draw detection
  - [ ] 6.1 Implement _checkWinOrDraw internal function
    - Create internal function `_checkWinOrDraw(uint256 gameId)`
    - Call `_checkWinner(gameId)` and store result
    - If winner found, set status = Finished, set winner address, emit GameEnded
    - If no winner, call `_checkDraw(gameId)`
    - If draw found, set status = Finished, set isDraw = true, emit GameEnded
    - _Requirements: 4.8, 5.1, 6.1_
  
  - [ ] 6.2 Implement _checkWinner internal function
    - Create internal view function `_checkWinner(uint256 gameId)` returns (bool, address)
    - Define winning patterns array: [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
    - Loop through each pattern
    - For each pattern, check if all three cells are non-Empty and identical
    - If match found, return (true, winner address)
    - Return (false, address(0)) if no winner
    - _Requirements: 5.1, 5.2, 5.4, 5.5_
  
  - [ ] 6.3 Implement _checkDraw internal function
    - Create internal view function `_checkDraw(uint256 gameId)` returns (bool)
    - Loop through all 9 board cells
    - If any cell is Empty, return false
    - If all cells filled, return true
    - _Requirements: 6.1, 6.2_
  
  - [ ]* 6.4 Write property tests for win/draw detection
    - **Property 11: Win Detection Completeness**
    - **Property 12: Draw Detection**
    - **Property 13: Game Finality**
    - **Validates: Requirements 5.1, 5.2, 5.4, 5.5, 6.1, 6.2, 6.4**

- [ ] 7. Implement contract view functions
  - [ ] 7.1 Add game state query functions
    - Implement `getGame(uint256 gameId)` external view returns (Game memory)
    - Implement `getBoard(uint256 gameId)` external view returns (CellState[9] memory)
    - Return games[gameId] and games[gameId].board respectively
    - _Requirements: 7.3, 13.1, 13.2, 13.3_
  
  - [ ]* 7.2 Write property test for state queries
    - **Property 15: State Query Consistency**
    - **Validates: Requirements 7.3, 13.1, 13.2**

- [ ] 8. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Configure Hardhat for Monad Testnet deployment
  - [ ] 9.1 Update hardhat.config.ts
    - Add Monad Testnet network configuration with RPC URL: https://testnet-rpc.monad.xyz
    - Add chainId: 10143 (Monad Testnet)
    - Configure accounts from environment variable PRIVATE_KEY
    - Add etherscan configuration for contract verification (if supported)
    - _Requirements: 20.1, 20.4_
  
  - [ ] 9.2 Create deployment script
    - Create `scripts/deploy.ts`
    - Deploy PlayerBadge contract first
    - Deploy TicTacToe contract with PlayerBadge address as constructor argument
    - Log both contract addresses
    - Save contract addresses to `frontend/src/contracts/addresses.json`
    - _Requirements: 20.1, 20.2, 20.3_

- [ ] 10. Set up frontend project structure
  - [ ] 10.1 Configure wagmi and providers
    - Create `frontend/src/config/wagmi.ts`
    - Configure Monad Testnet chain with chainId 10143, RPC URL, block explorer
    - Set up wagmi config with injected connector (MetaMask)
    - Configure @tanstack/react-query client
    - _Requirements: 9.1, 9.6, 20.3_
  
  - [ ] 10.2 Create TypeScript types
    - Create `frontend/src/types/game.ts`
    - Define CellState enum (Empty = 0, X = 1, O = 2)
    - Define GameStatus enum (Waiting = 0, Active = 1, Finished = 2)
    - Define Game interface matching contract struct
    - Define PlayerBadge interface
    - _Requirements: 13.1, 13.2_
  
  - [ ] 10.3 Set up contract ABIs and addresses
    - Create `frontend/src/contracts/` directory
    - Copy compiled ABIs from Hardhat artifacts to `frontend/src/contracts/abis/`
    - Create `addresses.json` for contract addresses (populated by deployment script)
    - Create `frontend/src/contracts/index.ts` to export ABIs and addresses
    - _Requirements: 20.3_

- [ ] 11. Implement wallet connection component
  - [ ] 11.1 Create WalletConnect component
    - Create `frontend/src/components/WalletConnect.tsx`
    - Use wagmi's `useAccount`, `useConnect`, `useDisconnect` hooks
    - Display connect button when not connected
    - Display connected address and disconnect button when connected
    - Show network validation message if not on Monad Testnet
    - Style with Tailwind using Delhi traffic theme colors
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 9.6_
  
  - [ ]* 11.2 Write unit tests for WalletConnect
    - Test component renders connect button when disconnected
    - Test component shows address when connected
    - Mock wagmi hooks for testing
    - _Requirements: 9.1, 9.2_

- [ ] 12. Implement PlayerBadge minting component
  - [ ] 12.1 Create BadgeMinting component
    - Create `frontend/src/components/BadgeMinting.tsx`
    - Use wagmi's `useContractRead` to check if user has badge
    - Use wagmi's `useContractWrite` for mintBadge function
    - Add input field for player name with validation
    - Display minting button if no badge exists
    - Show transaction pending state during minting
    - Display success message and player name after minting
    - Add Delhi-style messaging: "Badge le le, phir khel! 🎫"
    - _Requirements: 1.1, 1.3, 1.4, 1.5, 11.1, 11.2, 14.4_
  
  - [ ]* 12.2 Write property test for badge minting flow
    - **Property 1: Badge Minting Round Trip** (frontend validation)
    - **Property 3: Empty Name Rejection** (frontend validation)
    - **Validates: Requirements 1.1, 1.5, 14.3, 14.4**

- [ ] 13. Implement game creation and joining components
  - [ ] 13.1 Create GameCreation component
    - Create `frontend/src/components/GameCreation.tsx`
    - Use wagmi's `useContractWrite` for createGame function
    - Add "Create New Game" button
    - Display transaction pending state
    - Show generated Game ID prominently after creation
    - Add copy-to-clipboard button for Game ID
    - Display Delhi-style message: "Game ID: {id} - Dost ko bhej de! 📱"
    - _Requirements: 2.1, 2.5, 11.1, 11.2, 11.5_
  
  - [ ] 13.2 Create GameJoining component
    - Create `frontend/src/components/GameJoining.tsx`
    - Add input field for Game ID with validation
    - Use wagmi's `useContractWrite` for joinGame function
    - Add "Join Game" button
    - Validate Game ID exists before allowing join
    - Display transaction pending state
    - Show error messages for invalid joins with Delhi style
    - _Requirements: 3.1, 3.6, 11.1, 11.2, 14.2, 14.4_
  
  - [ ]* 13.3 Write property tests for game creation/joining
    - **Property 4: Game ID Uniqueness** (frontend validation)
    - **Property 6: Badge Holder Access Control** (frontend validation)
    - **Property 8: Invalid Join Rejection** (frontend validation)
    - **Validates: Requirements 2.1, 2.6, 3.6, 3.7, 3.8**

- [ ] 14. Implement game board component
  - [ ] 14.1 Create GameBoard component
    - Create `frontend/src/components/GameBoard.tsx`
    - Accept gameId as prop
    - Use wagmi's `useContractRead` to fetch game state
    - Render 3x3 grid using Tailwind grid classes
    - Display each cell with traffic symbols: 🚦 for X, 🛑 for O, empty for Empty
    - Show player addresses and current turn indicator
    - Display game status (Waiting, Active, Finished)
    - Style with purple-900 background and Delhi traffic aesthetics
    - _Requirements: 7.3, 10.1, 10.2, 10.5, 13.1, 13.2, 13.4_
  
  - [ ] 14.2 Add cell click handling
    - Make cells clickable only when game is Active and it's user's turn
    - Use wagmi's `useContractWrite` for makeMove function
    - Pass gameId and cell position (0-8) to makeMove
    - Disable cell clicks when not user's turn
    - Show "Tera Turn Hai! 🚦" when user's turn
    - Show "Waiting for Dost... 🛑" when opponent's turn
    - _Requirements: 4.1, 4.4, 9.4, 10.2_
  
  - [ ]* 14.3 Write unit tests for GameBoard
    - Test board renders correctly with different game states
    - Test cells are clickable only during user's turn
    - Test traffic symbols display correctly
    - Mock contract reads and writes
    - _Requirements: 10.1, 10.2, 13.4_

- [ ] 15. Implement real-time event listeners
  - [ ] 15.1 Create useGameEvents custom hook
    - Create `frontend/src/hooks/useGameEvents.ts`
    - Use wagmi's `useContractEvent` for MoveMade events
    - Use wagmi's `useContractEvent` for GameJoined events
    - Use wagmi's `useContractEvent` for GameEnded events
    - Filter events by gameId parameter
    - Return event data to consuming components
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 15.3, 15.4_
  
  - [ ] 15.2 Integrate events into GameBoard
    - Import and use useGameEvents hook in GameBoard component
    - Update board state when MoveMade event received
    - Trigger game start UI when GameJoined event received
    - Trigger end game UI when GameEnded event received
    - Ensure UI updates within 500ms of event receipt
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 16.2_
  
  - [ ]* 15.3 Write property test for event synchronization
    - **Property 16: Frontend State Synchronization**
    - **Validates: Requirement 8.5**

- [ ] 16. Implement Delhi traffic theme and messaging
  - [ ] 16.1 Create DelhiMessages utility
    - Create `frontend/src/utils/delhiMessages.ts`
    - Define array of Delhi traffic jokes/phrases
    - Export function `getRandomDelhiJoke()` that returns random message
    - Include messages like: "Traffic jam ho gaya! 🚧", "Signal tod diya! 🚦", "Metro le le bhai! 🚇"
    - _Requirements: 10.3_
  
  - [ ] 16.2 Add message display to GameBoard
    - Display random Delhi joke after each move using getRandomDelhiJoke()
    - Show joke in a toast notification or message box
    - Auto-dismiss after 3 seconds
    - _Requirements: 10.3_
  
  - [ ] 16.3 Style error messages with Delhi theme
    - Update all error messages to use Delhi colloquial style
    - Examples: "Arre bhai, wahan already gaadi khadi hai! 🚗", "Game ID nahi mila! Check kar le bhai 🔍"
    - Apply to validation errors, transaction failures, network errors
    - _Requirements: 10.4, 14.5_

- [ ] 17. Implement game end states and celebrations
  - [ ] 17.1 Create GameResult component
    - Create `frontend/src/components/GameResult.tsx`
    - Accept game state as prop
    - Display winner address if game won
    - Display draw message if game drawn
    - Show Delhi-style victory message: "Haan Bhai! Traffic Clear Ho Gaya! 🏆"
    - Show Delhi-style draw message: "Arre Yaar, Traffic Jam! Next Round? 🚧"
    - Show Delhi-style loss message: "Better luck next time! Metro le le bhai! 🚇"
    - _Requirements: 5.6, 6.5, 10.6_
  
  - [ ] 17.2 Add confetti animation for wins
    - Install canvas-confetti package
    - Import and trigger confetti when user wins
    - Use Delhi traffic colors for confetti (purple, orange, yellow)
    - _Requirements: 5.6_
  
  - [ ]* 17.3 Write unit tests for GameResult
    - Test correct message displays for win/draw/loss
    - Test confetti triggers on win
    - Mock game states for testing
    - _Requirements: 5.6, 6.5_

- [ ] 18. Implement transaction feedback and error handling
  - [ ] 18.1 Create TransactionStatus component
    - Create `frontend/src/components/TransactionStatus.tsx`
    - Display pending spinner during transaction processing
    - Show success notification with transaction hash link
    - Show error notification with failure reason
    - Include link to Monad Testnet Explorer for completed transactions
    - Display estimated confirmation time during pending state
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_
  
  - [ ] 18.2 Add gas balance checking
    - Create utility function to check user's MON balance
    - Display warning if balance is low before transaction
    - Show faucet link: https://faucet.monad.xyz when insufficient gas
    - Add message: "MON tokens khatam! Faucet se le le: 💰"
    - _Requirements: 12.1, 12.2, 12.3_
  
  - [ ] 18.3 Implement error recovery
    - Add retry button for failed transactions
    - Implement exponential backoff for network retries
    - Add fallback polling every 3 seconds if event listening fails
    - Log errors to console for debugging
    - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5_
  
  - [ ]* 18.4 Write property tests for transaction handling
    - **Property 18: Transaction Feedback**
    - **Property 19: Transaction Explorer Links**
    - **Property 20: Balance Validation**
    - **Validates: Requirements 11.1, 11.2, 11.3, 11.5, 12.1**

- [ ] 19. Implement multi-game support
  - [ ] 19.1 Create GameList component
    - Create `frontend/src/components/GameList.tsx`
    - Query all GameCreated and GameJoined events for connected address
    - Display list of active games with Game IDs
    - Show game status for each (Waiting, Active, Finished)
    - Add click handler to load selected game into GameBoard
    - _Requirements: 18.1, 18.2_
  
  - [ ] 19.2 Add game switching functionality
    - Store current gameId in React state
    - Update gameId when user selects different game from list
    - Ensure GameBoard re-renders with new game state
    - Maintain independent event listeners for each game
    - _Requirements: 18.3, 18.4_
  
  - [ ]* 19.3 Write property test for multi-game independence
    - **Property 24: Multi-Game Independence**
    - **Validates: Requirements 18.1, 18.3, 18.4**

- [ ] 20. Integrate all components into main App
  - [ ] 20.1 Create App.tsx layout
    - Create `frontend/src/App.tsx`
    - Wrap app with WagmiConfig and QueryClientProvider
    - Add WalletConnect component at top
    - Conditionally render BadgeMinting if no badge
    - Show GameCreation and GameJoining components side by side
    - Display GameList component
    - Render GameBoard for selected game
    - Apply Delhi traffic theme styling with purple-900 background
    - _Requirements: 9.1, 10.5, 16.3_
  
  - [ ] 20.2 Add responsive layout
    - Use Tailwind responsive classes for mobile and desktop
    - Ensure game board is centered and properly sized
    - Make components stack vertically on mobile
    - _Requirements: 16.3_

- [ ] 21. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 22. Deploy contracts to Monad Testnet
  - [ ] 22.1 Prepare deployment environment
    - Create `.env` file with PRIVATE_KEY for deployment wallet
    - Ensure deployment wallet has MON tokens from faucet
    - Verify Monad Testnet RPC is accessible
    - _Requirements: 20.1, 20.4_
  
  - [ ] 22.2 Execute deployment
    - Run `npx hardhat run scripts/deploy.ts --network monadTestnet`
    - Verify both contracts deploy successfully
    - Confirm contract addresses are saved to frontend/src/contracts/addresses.json
    - Verify contracts on Monad Testnet Explorer
    - _Requirements: 20.1, 20.2, 20.5_

- [ ] 23. Test complete dApp flow on Monad Testnet
  - [ ] 23.1 End-to-end manual testing
    - Connect wallet to Monad Testnet
    - Mint player badge with test name
    - Create new game and note Game ID
    - Open second browser/wallet and join game with Game ID
    - Play complete game to win condition
    - Verify all events fire and UI updates correctly
    - Test draw scenario
    - Test multiple simultaneous games
    - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5_
  
  - [ ] 23.2 Performance validation
    - Verify transactions confirm within 2 seconds
    - Verify UI updates within 500ms of events
    - Verify page loads within 2 seconds
    - Test with 10+ simultaneous games
    - _Requirements: 16.1, 16.2, 16.3, 16.5_
  
  - [ ] 23.3 Error scenario testing
    - Test insufficient gas handling
    - Test invalid Game ID entry
    - Test wrong turn move attempts
    - Test network disconnection recovery
    - Verify all error messages display correctly with Delhi theme
    - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5_

- [ ] 24. Prepare demo and documentation
  - [ ] 24.1 Create README.md
    - Document project overview and Delhi Ka Khel concept
    - Add setup instructions for local development
    - Include deployment instructions for Monad Testnet
    - Add usage guide with screenshots
    - List all dependencies and versions
    - Include links to deployed contracts on explorer
    - _Requirements: 20.4_
  
  - [ ] 24.2 Prepare demo script
    - Write step-by-step demo flow for hackathon presentation
    - Prepare two wallets with badges and MON tokens
    - Create demo game scenarios (quick win, draw)
    - Test demo flow multiple times for smooth presentation
    - Prepare backup plan for network issues
    - _Requirements: 16.1_

- [ ] 25. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional property-based and unit tests that can be skipped for faster MVP delivery
- Each task references specific requirements from the requirements document for traceability
- Checkpoints ensure incremental validation at key milestones
- Property tests validate universal correctness properties from the design document
- The implementation follows a bottom-up approach: contracts first, then frontend integration
- All Delhi traffic theming should be consistent across components
- Transaction feedback is critical for good UX during the demo
- Multi-game support enables impressive demo scenarios with multiple concurrent games
