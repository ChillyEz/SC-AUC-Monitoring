#!/bin/bash
# Download Stalcraft items database from GitHub

set -e

echo "Downloading Stalcraft items database..."

# Configuration
REPO="EXBO-Studio/stalcraft-database"
BRANCH="main"
TARGET_DIR="backend/data/stalcraft-database"

# Create target directory
mkdir -p "$TARGET_DIR"

# Clone or update repository
if [ -d "$TARGET_DIR/.git" ]; then
    echo "Updating existing database..."
    cd "$TARGET_DIR"
    git pull origin "$BRANCH"
else
    echo "Cloning database repository..."
    git clone --depth 1 --branch "$BRANCH" "https://github.com/$REPO.git" "$TARGET_DIR"
fi

echo "Database downloaded successfully to $TARGET_DIR"
