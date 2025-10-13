# SSH Commit Signing Guide

## Why Are My Commits Not Verified?

Using an SSH key for Git authentication (push/pull) is **different** from using an SSH key for commit signing. To have verified commits on GitHub, you need to:

1. Configure Git to sign your commits with an SSH key
2. Add your SSH public key to GitHub as a **signing key** (not just an authentication key)

## Setup Instructions

### 1. Generate an SSH Key (if you don't have one)

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Or for RSA:
```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

### 2. Configure Git to Use SSH for Signing

Tell Git to use SSH for signing commits:

```bash
git config --global gpg.format ssh
```

### 3. Specify Your SSH Signing Key

Point Git to your SSH public key:

```bash
git config --global user.signingkey ~/.ssh/id_ed25519.pub
```

Or if you're using RSA:
```bash
git config --global user.signingkey ~/.ssh/id_rsa.pub
```

**Note:** Use the path to your **public key** (.pub file), not the private key.

### 4. Enable Automatic Commit Signing

To sign all commits automatically:

```bash
git config --global commit.gpgsign true
```

### 5. Add Your SSH Key to GitHub

1. Copy your SSH public key:
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

2. Go to GitHub Settings → [SSH and GPG keys](https://github.com/settings/keys)

3. Click **"New SSH key"**

4. Select **"Signing Key"** as the key type (this is important!)

5. Paste your public key and give it a descriptive title

6. Click **"Add SSH key"**

### 6. Verify Your Configuration

Check your Git configuration:

```bash
git config --list | grep -E "(gpg|sign)"
```

You should see:
```
gpg.format=ssh
user.signingkey=/path/to/your/.ssh/id_ed25519.pub
commit.gpgsign=true
```

### 7. Test Signing a Commit

Create a test commit:

```bash
git commit --allow-empty -m "Test signed commit"
```

Verify the commit is signed:

```bash
git log --show-signature -1
```

You should see signature information in the output.

## Troubleshooting

### "error: gpg failed to sign the data"

- Make sure you specified the **public key** (.pub), not the private key
- Verify the path to your SSH key is correct
- Check that the key file exists and is readable

### Commits Still Show as "Unverified" on GitHub

- Make sure you added the SSH key to GitHub as a **Signing Key** (not just an Authentication Key)
- The email in your commits must match an email in your GitHub account
- Verify with: `git config user.email`

### Using Different Keys for Different Repositories

For repository-specific configuration (without `--global`):

```bash
cd /path/to/your/repo
git config gpg.format ssh
git config user.signingkey ~/.ssh/id_ed25519.pub
git config commit.gpgsign true
```

## Alternative: Using GPG Instead of SSH

If you prefer GPG over SSH for signing:

1. Install GPG: `brew install gnupg` (macOS) or `apt-get install gnupg` (Linux)
2. Generate a GPG key: `gpg --full-generate-key`
3. List keys: `gpg --list-secret-keys --keyid-format=long`
4. Configure Git: `git config --global user.signingkey YOUR_KEY_ID`
5. Enable signing: `git config --global commit.gpgsign true`
6. Add GPG key to GitHub in [Settings → SSH and GPG keys](https://github.com/settings/keys)

## Resources

- [GitHub Docs: Managing commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification)
- [GitHub Docs: Telling Git about your signing key](https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key)
- [GitHub Docs: Signing commits](https://docs.github.com/en/authentication/managing-commit-signature-verification/signing-commits)
