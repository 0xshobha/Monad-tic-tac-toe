# 🚀 GitHub Deployment Guide

## Deploy "Delhi Ka Khel" to GitHub

This guide will help you push your complete Tic Tac Toe project to GitHub repository: **Monad-tic-tac-toe**

---

## ✅ Pre-Deployment Checklist

Before pushing to GitHub, verify:

- [x] Contracts deployed to Monad Testnet
  - PlayerBadge: `0xBE679568645D1e0fb17eE9Fb0B70BCd3d1009116`
  - TicTacToe: `0x294645FEB89dC2651DBE2B3299880E0126a5FaFA`
- [x] Frontend tested and working on http://localhost:3001
- [x] `.gitignore` configured (node_modules, .env excluded)
- [x] `.env.example` created (no private keys)
- [x] Documentation complete

---

## 🎯 Step-by-Step Deployment

### Step 1: Initialize Git Repository

Open your terminal in the project root directory and run:

```bash
git init
```

This creates a new Git repository in your project folder.

---

### Step 2: Add All Files

```bash
git add .
```

This stages all your files for commit. The `.gitignore` file ensures sensitive files (like `.env` and `node_modules`) are excluded.

---

### Step 3: Create Initial Commit

```bash
git commit -m "Initial commit: Delhi Ka Khel - On-Chain Tic Tac Toe for Monad Blitz"
```

This creates your first commit with all project files.

---

### Step 4: Rename Branch to Main

```bash
git branch -M main
```

This renames your default branch to `main` (GitHub's standard).

---

### Step 5: Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click the **+** icon in top-right corner
3. Select **New repository**
4. Fill in details:
   - **Repository name**: `Monad-tic-tac-toe`
   - **Description**: "On-Chain Tic Tac Toe game built for Monad Blitz New Delhi hackathon"
   - **Visibility**: Public (so judges can see it!)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **Create repository**

---

### Step 6: Add Remote Origin

Copy the repository URL from GitHub (should look like: `https://github.com/0xshobha/Monad-tic-tac-toe.git`)

Then run:

```bash
git remote add origin https://github.com/0xshobha/Monad-tic-tac-toe.git
```

This links your local repository to GitHub.

---

### Step 7: Push to GitHub

```bash
git push -u origin main
```

This uploads all your code to GitHub!

**Note**: You may be prompted to enter your GitHub credentials:
- **Username**: `0xshobha`
- **Password**: Use a [Personal Access Token](https://github.com/settings/tokens) (not your GitHub password)

---

## 🎉 Verification

After pushing, verify your deployment:

1. Visit: `https://github.com/0xshobha/Monad-tic-tac-toe`
2. Check that all files are present:
   - ✅ `contracts/` folder with Solidity files
   - ✅ `frontend/` folder with React app
   - ✅ `README.md` with project description
   - ✅ Documentation files (REMIX_DEPLOYMENT.md, etc.)
   - ❌ NO `.env` file (should be excluded)
   - ❌ NO `node_modules/` folders (should be excluded)

---

## 📝 Add Repository to Hackathon Submission

When submitting to Monad Blitz:

1. **GitHub Repository**: `https://github.com/0xshobha/Monad-tic-tac-toe`
2. **Live Demo**: Include instructions to run locally (in README.md)
3. **Deployed Contracts**:
   - PlayerBadge: `0xBE679568645D1e0fb17eE9Fb0B70BCd3d1009116`
   - TicTacToe: `0x294645FEB89dC2651DBE2B3299880E0126a5FaFA`
   - Network: Monad Testnet (Chain ID: 10143)
4. **Contract Verification**: Link to Monad Explorer
   - PlayerBadge: `https://testnet.monadexplorer.com/address/0xBE679568645D1e0fb17eE9Fb0B70BCd3d1009116`
   - TicTacToe: `https://testnet.monadexplorer.com/address/0x294645FEB89dC2651DBE2B3299880E0126a5FaFA`

---

## 🔄 Making Updates After Initial Push

If you need to update your code after the initial push:

```bash
# Make your changes to files

# Stage changes
git add .

# Commit changes
git commit -m "Description of what you changed"

# Push to GitHub
git push
```

---

## 🆘 Troubleshooting

### "Permission denied" error
- Make sure you're using a Personal Access Token, not your password
- Generate token at: https://github.com/settings/tokens
- Select scopes: `repo` (full control of private repositories)

### "Repository not found" error
- Verify the repository exists on GitHub
- Check the remote URL: `git remote -v`
- Update if needed: `git remote set-url origin https://github.com/0xshobha/Monad-tic-tac-toe.git`

### "Failed to push" error
- Check your internet connection
- Verify you have write access to the repository
- Try: `git pull origin main --rebase` then `git push`

### Large files warning
- If you accidentally committed `node_modules/`, remove them:
  ```bash
  git rm -r --cached node_modules
  git rm -r --cached frontend/node_modules
  git commit -m "Remove node_modules"
  git push
  ```

---

## 🎯 Quick Command Reference

```bash
# Complete deployment in one go (copy-paste all at once)
git init
git add .
git commit -m "Initial commit: Delhi Ka Khel - On-Chain Tic Tac Toe for Monad Blitz"
git branch -M main
git remote add origin https://github.com/0xshobha/Monad-tic-tac-toe.git
git push -u origin main
```

---

## 🏆 Post-Deployment Checklist

After successful deployment:

- [ ] Repository is public and accessible
- [ ] README.md displays correctly on GitHub
- [ ] All documentation files are present
- [ ] Contract addresses are correct in `frontend/src/contracts/addresses.json`
- [ ] `.env` file is NOT in the repository
- [ ] Add repository link to hackathon submission
- [ ] Share repository link with judges
- [ ] Star your own repo (why not? 😄)

---

## 🎨 Optional: Add Repository Topics

Make your repo more discoverable:

1. Go to your repository on GitHub
2. Click the ⚙️ icon next to "About"
3. Add topics:
   - `monad`
   - `blockchain`
   - `tictactoe`
   - `hackathon`
   - `web3`
   - `solidity`
   - `react`
   - `delhi`

---

## 📞 Need Help?

If you encounter issues:
- Check [GitHub Docs](https://docs.github.com)
- Verify your Git installation: `git --version`
- Ensure you're in the correct directory: `pwd` (should show your project path)

---

**Ready to deploy? Let's go! 🚀**

*Haan Bhai! Code Push Ho Gaya!* 🏆
