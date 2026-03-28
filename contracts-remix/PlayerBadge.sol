// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

/**
 * @title PlayerBadge
 * @dev ERC-721 NFT for Delhi Ka Khel players - mint once per wallet with a fun Delhi name!
 * 
 * REMIX DEPLOYMENT INSTRUCTIONS:
 * 1. Copy this entire file into Remix IDE
 * 2. Compile with Solidity 0.8.28
 * 3. Deploy (no constructor arguments needed)
 * 4. Copy the deployed contract address for TicTacToe deployment
 */

// Minimal ERC-721 implementation for Remix (no external dependencies)
contract PlayerBadge {
    // ERC-721 Token name and symbol
    string public name = "Delhi Player Badge";
    string public symbol = "DPB";
    
    // State variables
    mapping(address => string) public playerNames;
    mapping(address => bool) public hasBadge;
    mapping(uint256 => address) private _owners;
    mapping(address => uint256) private _balances;
    uint256 private _tokenIdCounter;

    // Events
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);

    constructor() {
        _tokenIdCounter = 1; // Start from 1
    }

    /**
     * @dev Mint a player badge with a Delhi-style name
     * @param playerName The player's chosen name (e.g., "Delhi Speedster", "Traffic Warrior")
     * @return tokenId The minted token ID
     */
    function mintBadge(string memory playerName) external returns (uint256) {
        require(bytes(playerName).length > 0, "Name cannot be empty");
        require(!hasBadge[msg.sender], "Already has badge");

        uint256 tokenId = _tokenIdCounter;
        
        // Mint the token
        _owners[tokenId] = msg.sender;
        _balances[msg.sender] += 1;
        
        playerNames[msg.sender] = playerName;
        hasBadge[msg.sender] = true;
        _tokenIdCounter++;

        emit Transfer(address(0), msg.sender, tokenId);
        return tokenId;
    }

    /**
     * @dev Get player name for an address
     * @param player The player's address
     * @return The player's name
     */
    function getPlayerName(address player) external view returns (string memory) {
        return playerNames[player];
    }

    /**
     * @dev Returns the owner of the `tokenId` token
     */
    function ownerOf(uint256 tokenId) public view returns (address) {
        address owner = _owners[tokenId];
        require(owner != address(0), "Token does not exist");
        return owner;
    }

    /**
     * @dev Returns the number of tokens in `owner`'s account
     */
    function balanceOf(address owner) public view returns (uint256) {
        require(owner != address(0), "Invalid address");
        return _balances[owner];
    }
}
