// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

/**
 * @title PlayerBadge
 * @dev ERC-721 NFT for Delhi Ka Khel players - mint once per wallet with a fun Delhi name!
 */
contract PlayerBadge is ERC721 {
    // State variables
    mapping(address => string) public playerNames;
    mapping(address => bool) public hasBadge;
    uint256 private _tokenIdCounter;

    constructor() ERC721("Delhi Player Badge", "DPB") {
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
        _safeMint(msg.sender, tokenId);
        
        playerNames[msg.sender] = playerName;
        hasBadge[msg.sender] = true;
        _tokenIdCounter++;

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
}
