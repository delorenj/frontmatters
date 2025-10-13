# Features Report and Suggestions

## Introduction

The `frontmatters` tool is a command-line utility designed to streamline the management of frontmatter in markdown files. It offers a suite of features that leverage AI to automate documentation organization, provide structural insights, and ensure consistency across large sets of files. This report details the currently available features and proposes several new features to further enhance its capabilities.

## Available Features

The tool is built around three core commands: `description`, `tree`, and `organize`.

### 1. `description` Command

This is the primary feature for content enrichment. It automatically generates and adds concise, AI-powered descriptions to the frontmatter of markdown files.

- **AI Integration**: Uses the OpenRouter API to access various language models for description generation.
- **Batch Processing**: Can process a single file or an entire directory recursively.
- **Configuration**: Allows users to specify the AI model, set a traversal depth for directories, and force overwrite existing descriptions.
- **Error Handling**: Gracefully skips files that have no content or already have a description (unless forced).

### 2. `tree` Command

This command provides a visual overview of the documentation structure, similar to the `tree` command in Unix systems but with added frontmatter intelligence.

- **Enhanced Visualization**: Displays the directory structure as a tree and can include frontmatter fields like `description` and `tags` alongside filenames.
- **Customizable Output**: Users can control the depth of the tree, choose which frontmatter fields to display, and export the output to a JSON file for programmatic use.
- **Title Fallback**: Intelligently determines a title for each document by checking the frontmatter, looking for a top-level heading, or title-casing the filename.

### 3. `organize` Command

This is the most advanced feature, offering deep analysis of the documentation's organization. It uses the JSON output from the `tree` command as its input.

- **Dual-Mode Analysis**:
    - **Heuristic Mode**: A fast, local analysis that uses file paths, filenames, and existing frontmatter to propose tags, identify content types (e.g., blog, documentation, prompt), and generate deterministic categorization rules.
    - **AI-Powered Multi-Agent Mode**: A more sophisticated analysis that employs a system of specialized AI agents for a deep, semantic understanding of the content. This mode provides superior, context-aware recommendations but requires an OpenRouter API key.
- **Comprehensive Reporting**: Generates a detailed report that includes:
    - Content-type distribution.
    - Tag frequency and relationship analysis.
    - Recommendations for tag consolidation.
    - Suggested categorization rules to resolve organizational conflicts.
    - File-by-file recommendations for new tags.

## New Feature Suggestions

To build upon the existing foundation, the following features are recommended:

### 1. Automatic Tagging Command (`tag`)

While the `organize` command *proposes* tags, a new `tag` command could automatically generate and apply tags to markdown files based on their content, using AI. This would further automate the documentation workflow.

### 2. Frontmatter Validation and Linting (`lint`)

A `lint` or `validate` command would allow users to enforce consistency across their documentation. It would check frontmatter against a user-defined schema (e.g., in a `pyproject.toml` or a dedicated config file) to validate:
- **Required Fields**: Ensure essential keys like `title` or `date` are present.
- **Data Types**: Verify that fields like `tags` are a list or `date` is a valid date string.
- **Allowed Values**: Enforce specific values for fields like `status` (e.g., `draft`, `published`, `archived`).

### 3. Interactive Mode

An interactive mode for the `description` and `tag` commands would enhance user control. Instead of writing changes directly, the tool would present the AI-generated suggestions and prompt the user for confirmation (`[y]es/[n]o/[e]dit`). This prevents unwanted changes and allows for quick corrections.

### 4. Bulk Frontmatter Updates (`bulk-update`)

A command to perform bulk updates on frontmatter would be highly valuable for large-scale maintenance. For example:
- `frontmatters bulk-update --add 'author: Jules' ./docs/`
- `frontmatters bulk-update --remove 'status' --where-tag 'outdated' ./archive/`
- `frontmatters bulk-update --rename 'categories:tags' ./blog/`

### 5. `organize` Command Integration

The `organize` command currently produces a report with recommendations. A powerful next step would be to add an `--apply` flag to automatically implement these suggestions, such as adding proposed tags to files or even restructuring directories based on its analysis. This would make the `organize` feature a fully actionable tool.