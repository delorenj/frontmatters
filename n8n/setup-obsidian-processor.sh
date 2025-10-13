#!/bin/bash

# Obsidian Note Processor Setup Script
# This script helps you set up and validate the workflow system

set -e

echo "╔══════════════════════════════════════════════╗"
echo "║  Obsidian Note Processor Setup               ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
OBSIDIAN_VAULT_PATH="/home/delorenj/obsidian-vault"
WORKFLOW_FILES=(
	"obsidian-note-processor-workflow.json"
	"phase1-summarization.json"
	"phase2-categorization.json"
	"phase3-tagging.json"
	"phase4-enrichment.json"
	"phase5-write-obsidian.json"
	"fireflies-to-obsidian-integration.json"
)

# Step 1: Check for required files
echo "📋 Step 1: Checking for workflow files..."
MISSING_FILES=0
for file in "${WORKFLOW_FILES[@]}"; do
	if [ -f "$file" ]; then
		echo -e "${GREEN}✓${NC} Found: $file"
	else
		echo -e "${RED}✗${NC} Missing: $file"
		MISSING_FILES=$((MISSING_FILES + 1))
	fi
done

if [ $MISSING_FILES -gt 0 ]; then
	echo -e "${RED}Error: $MISSING_FILES workflow file(s) missing${NC}"
	exit 1
fi
echo ""

# Step 2: Validate Obsidian vault path
echo "📁 Step 2: Validating Obsidian vault path..."
if [ -d "$OBSIDIAN_VAULT_PATH" ]; then
	echo -e "${GREEN}✓${NC} Vault exists: $OBSIDIAN_VAULT_PATH"
else
	echo -e "${YELLOW}⚠${NC}  Vault not found at: $OBSIDIAN_VAULT_PATH"
	read -p "Enter your Obsidian vault path: " USER_VAULT_PATH
	OBSIDIAN_VAULT_PATH="$USER_VAULT_PATH"

	if [ ! -d "$OBSIDIAN_VAULT_PATH" ]; then
		echo -e "${RED}Error: Invalid vault path${NC}"
		exit 1
	fi
fi
echo ""

# Step 3: Create category directories
echo "📂 Step 3: Creating category directories..."
CATEGORIES=(
	"Projects"
	"AI/Prompts"
	"AI/Threads"
	"Documentation"
	"Research"
	"Blog"
	"Ideas"
	"References"
	"Examples"
	"Transcripts"
	"Infrastructure"
	"Family"
	"Finance"
)

for category in "${CATEGORIES[@]}"; do
	DIR_PATH="$OBSIDIAN_VAULT_PATH/$category"
	if [ ! -d "$DIR_PATH" ]; then
		mkdir -p "$DIR_PATH"
		echo -e "${GREEN}✓${NC} Created: $category"
	else
		echo -e "${YELLOW}•${NC} Exists: $category"
	fi
done
echo ""

# Step 4: Check for OpenRouter API key
echo "🔑 Step 4: Checking environment variables..."
if [ -z "$OPENROUTER_API_KEY" ]; then
	echo -e "${YELLOW}⚠${NC}  OPENROUTER_API_KEY not set in environment"
	echo "   You'll need to configure this in n8n as HTTP Header Auth"
	echo "   Header Name: Authorization"
	echo "   Header Value: Bearer YOUR_API_KEY"
else
	echo -e "${GREEN}✓${NC} OPENROUTER_API_KEY found"
fi
echo ""

# Step 5: Update workflow files with vault path
echo "⚙️  Step 5: Updating workflows with vault path..."
for file in "${WORKFLOW_FILES[@]}"; do
	if grep -q "/home/delorenj/obsidian-vault" "$file"; then
		# Create backup
		cp "$file" "$file.backup"

		# Replace path
		sed -i "s|/home/delorenj/obsidian-vault|$OBSIDIAN_VAULT_PATH|g" "$file"
		echo -e "${GREEN}✓${NC} Updated: $file"
	fi
done
echo ""

# Step 6: Generate import instructions
echo "📥 Step 6: Import Instructions"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Open your n8n instance"
echo "2. Go to Workflows → Import from File"
echo "3. Import these files in order:"
echo ""
for i in "${!WORKFLOW_FILES[@]}"; do
	echo "   $((i + 1)). ${WORKFLOW_FILES[$i]}"
done
echo ""
echo "4. Configure OpenRouter API credentials:"
echo "   - Name: 'OpenRouter API'"
echo "   - Type: HTTP Header Auth"
echo "   - Header: Authorization"
echo "   - Value: Bearer YOUR_OPENROUTER_API_KEY"
echo ""
echo "5. Apply credentials to all HTTP Request nodes in:"
echo "   - Phase 1: Summarization"
echo "   - Phase 2: Categorization"
echo "   - Phase 3: Tagging"
echo "   - Phase 4: Enrichment"
echo ""
echo "6. Test with a sample Fireflies transcript"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Step 7: Create test data
echo "🧪 Step 7: Creating test data..."
TEST_FILE="$OBSIDIAN_VAULT_PATH/test-transcript-$(date +%s).md"
cat >"$TEST_FILE" <<'TESTDATA'
---
title: Test Transcript
category: Transcript
tags:
  - test
description: Test transcript for workflow validation
---

# Test Transcript

This is a test transcript to validate the Obsidian Note Processor workflow.

## Sample Content

- Participant 1: Hello, let's discuss the new AI features
- Participant 2: Great! I think we should focus on agent capabilities
- Participant 1: Agreed. What about infrastructure requirements?
- Participant 2: We'll need to consider Docker and Kubernetes

## Action Items

- [ ] Research agent frameworks
- [ ] Set up development environment
- [ ] Schedule follow-up meeting
TESTDATA

echo -e "${GREEN}✓${NC} Created test file: $TEST_FILE"
echo ""

# Summary
echo "✨ Setup Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Next steps:"
echo "1. Import workflows into n8n"
echo "2. Configure OpenRouter API credentials"
echo "3. Test with the sample transcript"
echo "4. Connect to your Fireflies workflow"
echo ""
echo "Documentation: OBSIDIAN_NOTE_PROCESSOR_README.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
