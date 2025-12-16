#!/bin/bash

# Deployment script for mindmekka.com
# Usage: ./deploy.sh [user@host] [remote-path]

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
REMOTE_USER_HOST=${1:-"user@mindmekka.com"}
REMOTE_PATH=${2:-"/path/to/public_html"}

echo -e "${YELLOW}Deploying to ${REMOTE_USER_HOST}:${REMOTE_PATH}${NC}"

# Check if rsync is available
if ! command -v rsync &> /dev/null; then
    echo -e "${RED}Error: rsync is not installed. Please install it first.${NC}"
    exit 1
fi

# Deploy files (excluding git and Site Content directory)
rsync -avz --progress \
  --exclude '.git' \
  --exclude 'Site Content' \
  --exclude '.gitignore' \
  --exclude 'DEPLOYMENT.md' \
  --exclude 'deploy.sh' \
  --exclude '.DS_Store' \
  ./ "${REMOTE_USER_HOST}:${REMOTE_PATH}/"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Deployment successful!${NC}"
    echo -e "${YELLOW}Note: Don't forget to update the email address in includes/contact_form.php on the server${NC}"
else
    echo -e "${RED}✗ Deployment failed${NC}"
    exit 1
fi

