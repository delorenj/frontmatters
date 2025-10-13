# Obsidian Note Processor - AI-Powered Knowledge Management System

## Overview

This is a sophisticated n8n workflow system that automatically processes transcripts (from Fireflies or other sources) and transforms them into intelligently categorized, tagged, and enriched Obsidian notes with rich frontmatter metadata.

The system uses AI (Claude Sonnet 4.5 via OpenRouter) to:

1. Generate accurate titles and concise summaries
2. Classify documents into a single, optimal category
3. Generate multiple relevant tags
4. Extract category-specific metadata (e.g., project details for Project category)
5. Write fully-formed markdown notes to your Obsidian vault

## System Architecture

The system consists of **6 workflows** that work together in a pipeline:

```
Fireflies Transcript
        ↓
┌─────────────────────────────────────────┐
│  Main Orchestration Workflow            │
├─────────────────────────────────────────┤
│  1. Validate & Prepare Input            │
│  2. Phase 1: Summarization              │
│  3. Phase 2: Categorization             │
│  4. Phase 3: Tagging                    │
│  5. Phase 4: Enrichment (conditional)   │
│  6. Phase 5: Write to Obsidian          │
└─────────────────────────────────────────┘
        ↓
Obsidian Vault (organized by category)
```

## Category System

The system uses **13 carefully selected, non-overlapping categories**:

| Category           | Description                                        | Special Metadata                                                      |
| ------------------ | -------------------------------------------------- | --------------------------------------------------------------------- |
| **Project**        | Formal 33GOD project with DB ID, repos, components | `project_id`, `repo`, `project_root`, `status`, `stack`, `components` |
| **Prompt**         | Houses/showcases LLM prompts                       | None                                                                  |
| **Thread**         | LLM conversation threads                           | None                                                                  |
| **Documentation**  | Technical docs, API references, READMEs            | None                                                                  |
| **Research**       | AI development workflow research                   | None                                                                  |
| **Blog**           | Blog content, drafts, or writing material          | None                                                                  |
| **Idea**           | Important synthesized thoughts                     | None                                                                  |
| **Reference**      | Pointers to resources (repos, videos, articles)    | None                                                                  |
| **Example**        | Code snippets/repos for LLMs                       | None                                                                  |
| **Transcript**     | Speech-to-text from meetings or recordings         | None                                                                  |
| **Infrastructure** | Home network, homelab documentation                | None                                                                  |
| **Family**         | Personal/family matters                            | None                                                                  |
| **Finance**        | Money-related content                              | None                                                                  |

## Frontmatter Structure

### Universal Fields (All Categories)

```yaml
---
title: "AI-Generated Descriptive Title"
category: Transcript
tags:
  - transcript
  - meeting
  - ai/agents
  - product-development
description: "2-3 sentence summary of the document"
date_created: 2025-01-15T14:30:00Z
date_processed: 2025-01-15T14:35:12Z
source: fireflies
source_id: abc123def456
source_url: https://app.fireflies.ai/view/xyz
primary_domain: product-development
technologies:
  - python
  - docker
---
```

### Project-Specific Fields

When `category: Project`, additional fields are added:

```yaml
project_id: proj_12345
repo: github.com/username/project-name
project_root: /home/user/projects/project-name
status: active # planning | active | on-hold | completed
stack:
  - python
  - fastapi
  - postgresql
components:
  - api-server
  - worker-queue
  - frontend
```

## Tag Strategy

Tags are hierarchical and follow these patterns:

- **Technology**: `python`, `docker`, `kubernetes`, `fastapi`
- **Domain**: `ai/agents`, `devops/ci-cd`, `finance/budgeting`
- **Category-based**: `system-prompt`, `meeting`, `blog/draft`
- **Functional**: `troubleshooting`, `planning`, `reference`

Examples:

- **Prompt**: `#system-prompt`, `#ai/prompts`, `#code-generation`
- **Thread**: `#conversation`, `#ai/claude`, `#troubleshooting`
- **Transcript**: `#meeting`, `#planning`, `#product-development`
- **Infrastructure**: `#networking`, `#homelab`, `#kubernetes`

## Workflow Details

### Phase 1: Summarization & Title Generation

**Purpose**: Generate concise, descriptive titles and high-level summaries

**AI Model**: `anthropic/claude-sonnet-4.5`

**Process**:

1. Takes first 4000 characters of content
2. Generates title (max 8 words)
3. Writes 2-3 sentence summary

**Output**:

```json
{
  "title": "Weekly Product Planning Discussion",
  "summary": "Team discusses Q1 roadmap priorities..."
}
```

### Phase 2: Single Category Classification

**Purpose**: Classify document into exactly ONE category

**AI Model**: `anthropic/claude-sonnet-4.5`

**Process**:

1. Analyzes title, summary, and content sample
2. Considers source metadata (e.g., Fireflies = likely Transcript)
3. Returns category with confidence score

**Output**:

```json
{
  "category": "Transcript",
  "confidence": 0.95,
  "reasoning": "Contains meeting participants and discussion format"
}
```

### Phase 3: Multi-Tag Generation

**Purpose**: Generate 3-7 relevant, hierarchical tags

**AI Model**: `anthropic/claude-sonnet-4.5`

**Process**:

1. Analyzes category, title, summary, and content
2. Generates domain-specific tags
3. Extracts technologies mentioned
4. Automatically adds category as a tag

**Output**:

```json
{
  "tags": ["transcript", "meeting", "product-development", "ai/agents"],
  "primaryDomain": "product-development",
  "technologies": ["python", "docker"]
}
```

### Phase 4: Category-Specific Enrichment

**Purpose**: Extract metadata unique to certain categories (currently only Project)

**AI Model**: `anthropic/claude-sonnet-4.5`

**Process**:

1. Checks if category is "Project"
2. If yes → Extracts project-specific fields
3. If no → Pass through unchanged

**Output** (for Projects):

```json
{
  "projectMetadata": {
    "project_id": "proj_trinote_001",
    "repo": "github.com/delorenj/Trinote",
    "project_root": "/home/delorenj/projects/Trinote",
    "status": "active",
    "stack": ["python", "fastapi", "postgresql"],
    "components": ["api", "worker", "frontend"]
  }
}
```

### Phase 5: Write to Obsidian

**Purpose**: Write fully-formed markdown with frontmatter to Obsidian vault

**Process**:

1. Builds YAML frontmatter with all metadata
2. Constructs document body with sections:
   - Title
   - Metadata summary
   - AI-generated summary
   - Full content
   - AI processing notes
3. Determines file path based on category
4. Creates directory if needed
5. Writes file to Obsidian vault

**File Organization**:

```
/home/delorenj/obsidian-vault/
├── Projects/
├── AI/
│   ├── Prompts/
│   └── Threads/
├── Documentation/
├── Research/
├── Blog/
├── Ideas/
├── References/
├── Examples/
├── Transcripts/
├── Infrastructure/
├── Family/
└── Finance/
```

**Filename Format**:

```
YYYY-MM-DD_HH-MM-SS_Sanitized_Title.md
```

Example: `2025-01-15_14-30-00_Weekly_Product_Planning_Discussion.md`

## Installation & Setup

### 1. Import Workflows

Import all 6 JSON files into n8n:

1. `obsidian-note-processor-workflow.json` (main orchestrator)
2. `phase1-summarization.json`
3. `phase2-categorization.json`
4. `phase3-tagging.json`
5. `phase4-enrichment.json`
6. `phase5-write-obsidian.json`

### 2. Configure OpenRouter API Key

In n8n, create HTTP Header Auth credentials:

- Name: `OpenRouter API`
- Header Name: `Authorization`
- Header Value: `Bearer YOUR_OPENROUTER_API_KEY`

Apply this credential to all HTTP Request nodes in phases 1-4.

### 3. Configure Obsidian Vault Path

Edit Phase 5 (`phase5-write-obsidian.json`):

- Find the "Build Markdown with Frontmatter" node
- Update the `fullPath` variable:

```javascript
const fullPath = `/home/delorenj/obsidian-vault/${subdir}/${filename}`;
```

Change `/home/delorenj/obsidian-vault/` to your actual Obsidian vault path.

### 4. Connect to Your Fireflies Workflow

Option A: **Modify existing workflow**

Add "Execute Workflow" node at the end of your Fireflies workflow:

- Workflow: Select "Obsidian Note Processor - Main Workflow"
- Source: From "Extract and Process Transcript" node output

Option B: **Use integration workflow**

Import `fireflies-to-obsidian-integration.json` and connect it between your Fireflies workflow and the main processor.

## Usage Examples

### Example 1: Meeting Transcript

**Input**: Fireflies transcript from product planning meeting

**Output**:

```yaml
---
title: "Q1 Product Roadmap Planning Session"
category: Transcript
tags:
  - transcript
  - meeting
  - product-development
  - roadmap
  - ai/agents
description: "Team discusses Q1 priorities including new AI agent features, infrastructure improvements, and customer feedback integration."
date_created: 2025-01-15T14:30:00Z
source: fireflies
primary_domain: product-development
technologies:
  - python
  - kubernetes
---
```

### Example 2: Project Documentation

**Input**: Document describing a new project called "Trinote"

**Output**:

```yaml
---
title: "Trinote Project Overview"
category: Project
tags:
  - project
  - ai/agents
  - python
  - documentation
description: "AI-powered note-taking system that automatically organizes and enriches markdown notes with intelligent metadata."
date_created: 2025-01-15T15:00:00Z
project_id: proj_trinote_001
repo: github.com/delorenj/Trinote
project_root: /home/delorenj/projects/Trinote
status: active
stack:
  - python
  - fastapi
  - postgresql
components:
  - api-server
  - worker-queue
  - frontend
---
```

### Example 3: AI Prompt

**Input**: Document containing a system prompt for code generation

**Output**:

```yaml
---
title: "Python Code Generation System Prompt"
category: Prompt
tags:
  - prompt
  - system-prompt
  - ai/prompts
  - code-generation
  - python
description: "Comprehensive system prompt for generating production-ready Python code with error handling and documentation."
date_created: 2025-01-15T16:00:00Z
primary_domain: ai-development
technologies:
  - python
---
```

## Integration with Frontmatters Tool

This system is designed to work seamlessly with your `frontmatters` Python tool:

### Using `frontmatters organize analyze`

After processing notes, you can analyze your vault structure:

```bash
# Generate JSON tree
frontmatters tree show /home/delorenj/obsidian-vault \
  --json --both --depth 5 \
  --output vault-structure.json

# Analyze organization
frontmatters organize analyze vault-structure.json \
  --output organization-report.md
```

This will generate a report showing:

- Tag frequency and overlap
- Content type distribution
- Optimization recommendations

### Using AI-Powered Analysis

For deeper insights:

```bash
frontmatters organize analyze vault-structure.json \
  --agents \
  --model anthropic/claude-sonnet-4.5 \
  --output ai-analysis-report.md
```

This uses a multi-agent system to:

- Analyze content at scale
- Identify tag consolidation opportunities
- Suggest taxonomy improvements
- Generate categorization rules

## Advanced Configuration

### Customizing Categories

To add or modify categories:

1. Edit Phase 2 (`phase2-categorization.json`)
2. Update the AI prompt with new category definitions
3. Edit the validation list in "Parse & Validate Category" node
4. Edit Phase 5 (`phase5-write-obsidian.json`)
5. Add new category to `categoryPaths` object

### Adding New Enrichment Rules

To add enrichment for other categories (like Transcript, Research):

1. Edit Phase 4 (`phase4-enrichment.json`)
2. Add new conditional branches in "Is Project Category?" node
3. Create new HTTP Request nodes for AI extraction
4. Update parsing logic

Example: Add Infrastructure-specific fields:

```javascript
if (data.category === "Infrastructure") {
  // Extract: network_topology, devices, services
}
```

### Adjusting AI Behavior

Modify prompts in HTTP Request nodes to change AI behavior:

**More conservative classification** (higher accuracy, fewer tags):

```javascript
temperature: 0.1; // Default: 0.2-0.4
```

**More creative tagging** (more tags, broader coverage):

```javascript
temperature: 0.6; // Default: 0.4
max_tokens: 500; // Default: 300
```

## Monitoring & Debugging

### Check Processing Stages

Each workflow adds a `processingStage` field:

1. `initialized` - Input validated
2. `summarized` - Title and summary generated
3. `categorized` - Category assigned
4. `tagged` - Tags generated
5. `enriched` - Metadata extracted
6. `complete` - Written to Obsidian

### View AI Confidence Scores

Frontmatter includes AI processing notes:

```yaml
## AI Processing Notes

- **Category Confidence**: 95.0%
- **Category Reasoning**: Contains meeting participants and discussion format
- **Processing Stage**: complete
```

### Common Issues

**Issue**: Notes categorized incorrectly

**Solution**:

- Check `categoryReasoning` in frontmatter
- Adjust temperature in Phase 2 (lower = more conservative)
- Add more context to prompts

**Issue**: Tags too generic

**Solution**:

- Increase context window (currently 1500 chars)
- Add domain-specific examples to Phase 3 prompt
- Use lower temperature for more precise tags

**Issue**: Project metadata missing

**Solution**:

- Ensure project info is in first 2000 characters
- Check AI response parsing in Phase 4
- Manually add missing fields to frontmatter

## Performance Considerations

### API Costs

Approximate costs per note (using Claude Sonnet 4.5):

- Phase 1 (Summarization): ~$0.01
- Phase 2 (Categorization): ~$0.008
- Phase 3 (Tagging): ~$0.012
- Phase 4 (Enrichment): ~$0.015 (only for Projects)

**Total per note**: ~$0.03-$0.045

For 100 notes: ~$3-$4.50

### Processing Time

Average processing time per note:

- Phase 1: 2-3 seconds
- Phase 2: 1-2 seconds
- Phase 3: 2-3 seconds
- Phase 4: 2-3 seconds (conditional)
- Phase 5: <1 second

**Total**: 7-12 seconds per note

### Optimization Tips

1. **Batch processing**: Use n8n's batch execution for multiple notes
2. **Caching**: Store common patterns (e.g., frequently used tags)
3. **Parallel execution**: Run multiple workflows simultaneously
4. **Model selection**: Use cheaper models for simple tasks

## Future Enhancements

### Planned Features

- [ ] Support for more source types (Google Meet, Zoom, etc.)
- [ ] Intelligent linking between related notes
- [ ] Automatic embedding generation for vector search
- [ ] Multi-language support
- [ ] Custom taxonomy learning from user corrections
- [ ] Integration with graph databases (Neo4j)
- [ ] Real-time processing via webhooks

### Integration Opportunities

- **Obsidian Plugins**: Dataview, Templater
- **Search Systems**: Elasticsearch, Meilisearch
- **Vector DBs**: Pinecone, Weaviate, Qdrant
- **RAG Systems**: LangChain, LlamaIndex

## Contributing

This system is part of the 33GOD ecosystem. For improvements:

1. Test changes thoroughly on sample notes
2. Document any prompt modifications
3. Measure accuracy/performance impact
4. Update this README with new features

## License

Part of 33GOD internal tooling.

## Support

For issues or questions:

- Check n8n execution logs
- Review AI processing notes in frontmatter
- Analyze vault structure with `frontmatters` tool
- Validate workflow connections in n8n

---

**Built with**: n8n, Claude Sonnet 4.5, OpenRouter, Obsidian, Python (frontmatters)
