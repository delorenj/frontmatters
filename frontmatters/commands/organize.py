import json
import typer
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, Counter
from dataclasses import dataclass
import re

app = typer.Typer()


@dataclass
class FileAnalysis:
    """Analysis results for a single file."""
    path: str
    name: str
    existing_tags: List[str]
    proposed_tags: List[str]
    content_type: str
    directory_context: List[str]
    description: Optional[str] = None


@dataclass
class TagAnalysis:
    """Analysis of tag usage and overlap."""
    tag: str
    frequency: int
    files: List[str]
    related_tags: Set[str]
    semantic_group: Optional[str] = None


@dataclass
class CategoryRule:
    """Rule for deterministic categorization."""
    rule_id: str
    description: str
    condition: str
    category: str
    priority: int


class OrganizationAnalyzer:
    """Analyzes file structure and proposes optimal organization."""
    
    def __init__(self):
        self.files: List[FileAnalysis] = []
        self.tag_analysis: Dict[str, TagAnalysis] = {}
        self.category_rules: List[CategoryRule] = []
        
    def analyze_tree_json(self, tree_data: dict) -> None:
        """Analyze the JSON tree structure and extract file information."""
        self._extract_files_recursive(tree_data, [])
        
    def _extract_files_recursive(self, node: dict, path_context: List[str]) -> None:
        """Recursively extract files from tree structure."""
        if node.get("type") == "file" and node["name"].endswith(".md"):
            # Extract directory context from path
            full_path = node["path"]
            directory_parts = Path(full_path).parent.parts
            
            # Get existing tags and description from frontmatter
            frontmatter = node.get("frontmatter", {})
            existing_tags = frontmatter.get("tags", [])
            description = frontmatter.get("description", "")
            
            # Propose tags based on file analysis
            proposed_tags = self._propose_tags(node["name"], directory_parts, description)
            
            # Determine content type
            content_type = self._determine_content_type(node["name"], directory_parts, description)
            
            file_analysis = FileAnalysis(
                path=full_path,
                name=node["name"],
                existing_tags=existing_tags if isinstance(existing_tags, list) else [],
                proposed_tags=proposed_tags,
                content_type=content_type,
                directory_context=list(directory_parts),
                description=description
            )
            
            self.files.append(file_analysis)
            
        # Recurse into children
        for child in node.get("children", []):
            new_context = path_context + [node["name"]] if node.get("type") == "directory" else path_context
            self._extract_files_recursive(child, new_context)
    
    def _propose_tags(self, filename: str, directory_parts: Tuple[str, ...], description: str) -> List[str]:
        """Propose tags based on filename, location, and description."""
        tags = set()
        
        # Extract from directory structure
        for part in directory_parts:
            if part.lower() in ['ai', 'agents', 'prompts', 'blog', 'research', 'workflows', 'tools']:
                tags.add(part.lower())
        
        # Extract from filename patterns
        filename_lower = filename.lower()
        
        # Content type indicators
        if any(word in filename_lower for word in ['draft', 'wip', 'temp']):
            tags.add('draft')
        if any(word in filename_lower for word in ['blog', 'post', 'article']):
            tags.add('blog')
        if any(word in filename_lower for word in ['prompt', 'system']):
            tags.add('prompt')
        if any(word in filename_lower for word in ['agent', 'bot']):
            tags.add('agent')
        if any(word in filename_lower for word in ['workflow', 'process']):
            tags.add('workflow')
        if any(word in filename_lower for word in ['research', 'analysis']):
            tags.add('research')
        if any(word in filename_lower for word in ['thread', 'conversation']):
            tags.add('thread')
        if any(word in filename_lower for word in ['config', 'settings']):
            tags.add('configuration')
        if any(word in filename_lower for word in ['runbook', 'guide', 'tutorial']):
            tags.add('documentation')
        
        # Technology indicators from description
        if description:
            desc_lower = description.lower()
            if any(tech in desc_lower for tech in ['python', 'javascript', 'typescript', 'rust', 'go']):
                tags.add('programming')
            if any(tech in desc_lower for tech in ['docker', 'kubernetes', 'aws', 'gcp', 'azure']):
                tags.add('infrastructure')
            if any(tech in desc_lower for tech in ['api', 'rest', 'graphql', 'endpoint']):
                tags.add('api')
            if any(tech in desc_lower for tech in ['database', 'sql', 'mongodb', 'postgres']):
                tags.add('database')
        
        return list(tags)
    
    def _determine_content_type(self, filename: str, directory_parts: Tuple[str, ...], description: str) -> str:
        """Determine the primary content type of the file."""
        filename_lower = filename.lower()
        
        # Check for specific patterns
        if 'blog' in directory_parts or any(word in filename_lower for word in ['blog', 'post', 'article']):
            return 'blog'
        elif 'prompt' in directory_parts or 'prompt' in filename_lower:
            return 'prompt'
        elif 'agent' in directory_parts or 'agent' in filename_lower:
            return 'agent'
        elif 'workflow' in directory_parts or 'workflow' in filename_lower:
            return 'workflow'
        elif 'research' in directory_parts or 'research' in filename_lower:
            return 'research'
        elif 'thread' in filename_lower or 'conversation' in filename_lower:
            return 'thread'
        elif any(word in filename_lower for word in ['config', 'settings']):
            return 'configuration'
        elif any(word in filename_lower for word in ['readme', 'guide', 'tutorial', 'doc']):
            return 'documentation'
        elif any(word in filename_lower for word in ['draft', 'wip', 'temp']):
            return 'draft'
        else:
            return 'general'
    
    def analyze_tags(self) -> None:
        """Analyze tag usage patterns and relationships."""
        tag_files = defaultdict(list)
        tag_cooccurrence = defaultdict(lambda: defaultdict(int))
        
        # Collect tag usage
        for file_analysis in self.files:
            all_tags = set(file_analysis.existing_tags + file_analysis.proposed_tags)
            for tag in all_tags:
                tag_files[tag].append(file_analysis.path)
                
                # Track co-occurrence
                for other_tag in all_tags:
                    if tag != other_tag:
                        tag_cooccurrence[tag][other_tag] += 1
        
        # Create tag analysis
        for tag, files in tag_files.items():
            related_tags = set()
            for other_tag, count in tag_cooccurrence[tag].items():
                if count >= 2:  # Appears together in at least 2 files
                    related_tags.add(other_tag)
            
            self.tag_analysis[tag] = TagAnalysis(
                tag=tag,
                frequency=len(files),
                files=files,
                related_tags=related_tags
            )
    
    def generate_category_rules(self) -> None:
        """Generate deterministic rules for categorization conflicts."""
        rules = [
            CategoryRule(
                rule_id="system_prompt_location",
                description="System prompts should be organized by their primary use case, not by project",
                condition="content_type == 'prompt' and 'system' in filename.lower()",
                category="AI/Prompts/System",
                priority=1
            ),
            CategoryRule(
                rule_id="project_specific_agents",
                description="Project-specific agents should live with the project, not in general agents",
                condition="content_type == 'agent' and any(project in directory_context for project in ['RepRally', 'Trinote', 'specific_project'])",
                category="Projects/{project}/Agents",
                priority=2
            ),
            CategoryRule(
                rule_id="blog_content_centralization",
                description="All blog content should be centralized regardless of topic",
                condition="content_type == 'blog' or 'blog' in filename.lower()",
                category="AI/Blog",
                priority=1
            ),
            CategoryRule(
                rule_id="research_by_topic",
                description="Research should be organized by topic, not by type",
                condition="content_type == 'research'",
                category="AI/Research/{topic}",
                priority=3
            ),
            CategoryRule(
                rule_id="workflow_by_domain",
                description="Workflows should be organized by their domain of application",
                condition="content_type == 'workflow'",
                category="AI/Workflows/{domain}",
                priority=2
            )
        ]
        
        self.category_rules = rules


@app.command()
def analyze(
    json_file: Path = typer.Argument(..., help="JSON file from tree command"),
    output_file: Path = typer.Option(None, "--output", "-o", help="Write analysis report to file"),
    min_tag_frequency: int = typer.Option(2, "--min-freq", help="Minimum frequency for tag recommendations"),
    max_categories: int = typer.Option(20, "--max-categories", help="Maximum number of primary categories"),
):
    """
    Analyze JSON tree output and propose optimal organizational strategy.
    
    This command analyzes the structure and content of your documentation
    to propose an optimal tagging and categorization system.
    """
    if not json_file.exists():
        typer.echo(f"Error: JSON file '{json_file}' does not exist", err=True)
        raise typer.Exit(1)
    
    # Load and parse JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            tree_data = json.load(f)
    except json.JSONDecodeError as e:
        typer.echo(f"Error: Invalid JSON in '{json_file}': {e}", err=True)
        raise typer.Exit(1)
    
    # Initialize analyzer
    analyzer = OrganizationAnalyzer()
    
    # Analyze the tree structure
    analyzer.analyze_tree_json(tree_data)
    analyzer.analyze_tags()
    analyzer.generate_category_rules()
    
    # Generate report
    report = generate_analysis_report(analyzer, min_tag_frequency, max_categories)
    
    # Output report
    if output_file:
        output_file.write_text(report, encoding='utf-8')
        typer.echo(f"Analysis report written to {output_file}")
    else:
        typer.echo(report)


def generate_analysis_report(analyzer: OrganizationAnalyzer, min_freq: int, max_categories: int) -> str:
    """Generate a comprehensive analysis report."""
    report_lines = []
    
    # Header
    report_lines.extend([
        "# Documentation Organization Analysis Report",
        f"Generated for {len(analyzer.files)} markdown files",
        "",
        "## Executive Summary",
        "",
        f"- **Total Files Analyzed**: {len(analyzer.files)}",
        f"- **Unique Tags Proposed**: {len(analyzer.tag_analysis)}",
        f"- **Content Types Identified**: {len(set(f.content_type for f in analyzer.files))}",
        "",
    ])
    
    # Content type distribution
    content_types = Counter(f.content_type for f in analyzer.files)
    report_lines.extend([
        "## Content Type Distribution",
        "",
        "| Content Type | Count | Percentage |",
        "|--------------|-------|------------|",
    ])
    
    total_files = len(analyzer.files)
    for content_type, count in content_types.most_common():
        percentage = (count / total_files) * 100
        report_lines.append(f"| {content_type} | {count} | {percentage:.1f}% |")
    
    report_lines.append("")
    
    # Tag frequency analysis
    frequent_tags = {tag: analysis for tag, analysis in analyzer.tag_analysis.items() 
                    if analysis.frequency >= min_freq}
    
    report_lines.extend([
        f"## Proposed Tag Analysis (≥{min_freq} occurrences)",
        "",
        "| Tag | Frequency | Related Tags |",
        "|-----|-----------|--------------|",
    ])
    
    for tag, analysis in sorted(frequent_tags.items(), key=lambda x: x[1].frequency, reverse=True):
        related = ", ".join(sorted(analysis.related_tags)[:3])  # Top 3 related tags
        if len(analysis.related_tags) > 3:
            related += "..."
        report_lines.append(f"| {tag} | {analysis.frequency} | {related} |")
    
    report_lines.append("")
    
    # Category rules
    report_lines.extend([
        "## Categorization Rules",
        "",
        "These rules resolve conflicts when files could belong to multiple categories:",
        "",
    ])
    
    for i, rule in enumerate(analyzer.category_rules, 1):
        report_lines.extend([
            f"### Rule {i}: {rule.description}",
            f"- **Condition**: `{rule.condition}`",
            f"- **Category**: `{rule.category}`",
            f"- **Priority**: {rule.priority}",
            "",
        ])
    
    # Optimization recommendations
    report_lines.extend([
        "## Optimization Recommendations",
        "",
        "### 1. Tag Consolidation Opportunities",
        "",
    ])
    
    # Find overlapping tags
    overlapping_tags = []
    for tag1, analysis1 in frequent_tags.items():
        for tag2, analysis2 in frequent_tags.items():
            if tag1 < tag2:  # Avoid duplicates
                overlap = len(set(analysis1.files) & set(analysis2.files))
                if overlap >= 2:
                    overlapping_tags.append((tag1, tag2, overlap))
    
    overlapping_tags.sort(key=lambda x: x[2], reverse=True)
    
    for tag1, tag2, overlap in overlapping_tags[:5]:  # Top 5 overlaps
        report_lines.append(f"- **{tag1}** and **{tag2}**: {overlap} files in common")
    
    if not overlapping_tags:
        report_lines.append("- No significant tag overlaps found")
    
    report_lines.extend([
        "",
        "### 2. Suggested Primary Categories",
        "",
        "Based on content analysis, these primary categories would provide optimal organization:",
        "",
    ])
    
    # Generate primary categories based on content types and frequency
    primary_categories = []
    for content_type, count in content_types.most_common(max_categories):
        if count >= 3:  # Only suggest categories with sufficient content
            primary_categories.append(f"- **{content_type.title()}** ({count} files)")
    
    report_lines.extend(primary_categories)
    
    # File-by-file recommendations
    report_lines.extend([
        "",
        "## File-by-File Tag Recommendations",
        "",
        "| File | Current Tags | Proposed Tags | Content Type |",
        "|------|--------------|---------------|--------------|",
    ])
    
    for file_analysis in sorted(analyzer.files, key=lambda x: x.path):
        current_tags = ", ".join(file_analysis.existing_tags) if file_analysis.existing_tags else "None"
        proposed_tags = ", ".join(file_analysis.proposed_tags) if file_analysis.proposed_tags else "None"
        
        # Truncate long paths for readability
        display_path = file_analysis.path
        if len(display_path) > 50:
            display_path = "..." + display_path[-47:]
        
        report_lines.append(f"| {display_path} | {current_tags} | {proposed_tags} | {file_analysis.content_type} |")
    
    return "\n".join(report_lines)


if __name__ == "__main__":
    app()
