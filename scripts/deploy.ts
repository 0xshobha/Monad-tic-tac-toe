import { ethers } from "hardhat";
import * as fs from "fs";
import * as path from "path";

async function main() {
  console.log("🚦 Deploying Delhi Ka Khel contracts to Monad Testnet...\n");

  // Deploy PlayerBadge first
  console.log("📛 Deploying PlayerBadge contract...");
  const PlayerBadge = await ethers.getContractFactory("PlayerBadge");
  const playerBadge = await PlayerBadge.deploy();
  await playerBadge.waitForDeployment();
  const playerBadgeAddress = await playerBadge.getAddress();
  console.log("✅ PlayerBadge deployed to:", playerBadgeAddress);

  // Deploy TicTacToe with PlayerBadge address
  console.log("\n🎮 Deploying TicTacToe contract...");
  const TicTacToe = await ethers.getContractFactory("TicTacToe");
  const ticTacToe = await TicTacToe.deploy(playerBadgeAddress);
  await ticTacToe.waitForDeployment();
  const ticTacToeAddress = await ticTacToe.getAddress();
  console.log("✅ TicTacToe deployed to:", ticTacToeAddress);

  // Save addresses to frontend
  const addresses = {
    playerBadge: playerBadgeAddress,
    ticTacToe: ticTacToeAddress,
    network: "monadTestnet",
    chainId: 10143,
  };

  const frontendDir = path.join(__dirname, "../frontend/src/contracts");
  if (!fs.existsSync(frontendDir)) {
    fs.mkdirSync(frontendDir, { recursive: true });
  }

  fs.writeFileSync(
    path.join(frontendDir, "addresses.json"),
    JSON.stringify(addresses, null, 2)
  );

  console.log("\n📝 Contract addresses saved to frontend/src/contracts/addresses.json");
  console.log("\n🎉 Deployment complete! Haan Bhai!");
  console.log("\n📋 Summary:");
  console.log("   PlayerBadge:", playerBadgeAddress);
  console.log("   TicTacToe:", ticTacToeAddress);
  console.log("   Explorer:", `https://testnet.monadexplorer.com/address/${ticTacToeAddress}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
