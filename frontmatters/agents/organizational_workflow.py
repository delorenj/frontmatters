"""
Agno-based Multi-Agent Organizational Analysis System

This module implements a sophisticated multi-agent system using Agno framework
to analyze documentation structure and provide intelligent organizational strategies.

Agents:
- Content Analyzer: Deep semantic analysis of file content
- Categorizer: Determines optimal category placement  
- Tagger: Suggests relevant tags based on content understanding
- Relationship Mapper: Identifies connections between documents
- Data Science Optimizer: Statistical analysis and optimization
- Organizational Strategist: High-level strategy and rule creation
"""

import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.team import Team
from agno.workflow.workflow import Workflow
from agno.workflow.step import Step, StepInput, StepOutput
from agno.db.sqlite import SqliteDb


@dataclass
class DocumentAnalysis:
    """Structured analysis result for a single document."""
    path: str
    content_summary: str
    semantic_tags: List[str]
    category_recommendation: str
    relationships: List[str]
    confidence_score: float
    reasoning: str


@dataclass
class OrganizationalStrategy:
    """Complete organizational strategy result."""
    document_analyses: List[DocumentAnalysis]
    tag_taxonomy: Dict[str, List[str]]
    category_hierarchy: Dict[str, List[str]]
    optimization_recommendations: List[str]
    implementation_rules: List[str]


class ContentAnalyzerAgent:
    """Agent specialized in deep semantic content analysis."""
    
    def __init__(self):
        self.agent = Agent(
            name="Content Analyzer",
            role="Expert content analyst specializing in semantic understanding of technical documentation",
            model=Claude(id="claude-3-5-sonnet-20241022"),
            instructions=[
                "You are an expert content analyst with deep understanding of technical documentation.",
                "Analyze file content for semantic meaning, key concepts, and technical depth.",
                "Identify the primary purpose, audience, and technical domain of each document.",
                "Extract key concepts, technologies, methodologies, and subject matter.",
                "Provide confidence scores for your analysis based on content clarity and completeness.",
                "Focus on understanding what the document is about, not just what it says.",
            ],
            markdown=True,
        )
    
    async def analyze_content(self, file_path: str, content: str, description: str) -> Dict[str, Any]:
        """Perform deep semantic analysis of document content."""
        prompt = f"""
        Analyze this document for semantic understanding and content classification:
        
        **File Path:** {file_path}
        **Description:** {description}
        **Content Preview:** {content[:2000]}...
        
        Provide a comprehensive analysis including:
        1. **Content Summary** (2-3 sentences about what this document covers)
        2. **Primary Purpose** (what is this document trying to achieve?)
        3. **Technical Domain** (AI, infrastructure, development, documentation, etc.)
        4. **Key Concepts** (main ideas, technologies, methodologies mentioned)
        5. **Audience Level** (beginner, intermediate, expert, mixed)
        6. **Content Type** (tutorial, reference, analysis, planning, etc.)
        7. **Confidence Score** (0.0-1.0 based on content clarity and completeness)
        8. **Reasoning** (explain your analysis and confidence level)
        
        Format as JSON with these exact keys:
        {{
            "content_summary": "...",
            "primary_purpose": "...",
            "technical_domain": "...",
            "key_concepts": ["concept1", "concept2", ...],
            "audience_level": "...",
            "content_type": "...",
            "confidence_score": 0.85,
            "reasoning": "..."
        }}
        """
        
        response = await self.agent.arun(prompt)
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "content_summary": "Analysis failed - unable to parse content",
                "primary_purpose": "unknown",
                "technical_domain": "unknown",
                "key_concepts": [],
                "audience_level": "unknown",
                "content_type": "unknown",
                "confidence_score": 0.0,
                "reasoning": "JSON parsing failed"
            }


class CategorizerAgent:
    """Agent specialized in determining optimal category placement."""
    
    def __init__(self):
        self.agent = Agent(
            name="Categorizer",
            role="Expert information architect specializing in taxonomic organization",
            model=Claude(id="claude-3-5-sonnet-20241022"),
            instructions=[
                "You are an expert information architect with deep knowledge of taxonomic organization.",
                "Determine optimal category placement for documents based on content analysis.",
                "Consider existing directory structure, content relationships, and organizational principles.",
                "Recommend category hierarchies that minimize cognitive load and maximize findability.",
                "Balance specificity with generality to avoid over-categorization.",
                "Consider user workflows and access patterns when recommending categories.",
            ],
            markdown=True,
        )
    
    async def categorize_document(self, content_analysis: Dict[str, Any], current_path: str, 
                                existing_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Determine optimal category placement for a document."""
        prompt = f"""
        Based on the content analysis, determine the optimal category placement:
        
        **Content Analysis:**
        {json.dumps(content_analysis, indent=2)}
        
        **Current Path:** {current_path}
        
        **Existing Structure Overview:**
        {json.dumps(existing_structure, indent=2)}
        
        Recommend:
        1. **Primary Category** (main organizational bucket)
        2. **Subcategory Path** (full hierarchical path)
        3. **Alternative Categories** (other valid placements)
        4. **Category Rationale** (why this placement is optimal)
        5. **Structural Improvements** (suggestions for category hierarchy)
        
        Format as JSON:
        {{
            "primary_category": "AI/Documentation",
            "subcategory_path": "AI/Documentation/Guides",
            "alternative_categories": ["AI/Tutorials", "Documentation/AI"],
            "category_rationale": "...",
            "structural_improvements": ["suggestion1", "suggestion2"]
        }}
        """
        
        response = await self.agent.arun(prompt)
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {
                "primary_category": "Uncategorized",
                "subcategory_path": "Uncategorized",
                "alternative_categories": [],
                "category_rationale": "Categorization failed",
                "structural_improvements": []
            }


class TaggerAgent:
    """Agent specialized in intelligent tag suggestion."""
    
    def __init__(self):
        self.agent = Agent(
            name="Tagger",
            role="Expert metadata specialist focusing on semantic tagging systems",
            model=OpenAIChat(id="gpt-4o"),
            instructions=[
                "You are an expert metadata specialist with deep knowledge of semantic tagging systems.",
                "Generate relevant, specific, and useful tags based on content analysis.",
                "Balance broad categorical tags with specific technical tags.",
                "Consider tag hierarchies and relationships to avoid redundancy.",
                "Focus on tags that improve searchability and discoverability.",
                "Suggest both explicit (directly mentioned) and implicit (inferred) tags.",
            ],
            markdown=True,
        )
    
    async def suggest_tags(self, content_analysis: Dict[str, Any], 
                          existing_tags: List[str], tag_frequency_data: Dict[str, int]) -> Dict[str, Any]:
        """Generate intelligent tag suggestions based on content analysis."""
        prompt = f"""
        Generate optimal tags for this document based on content analysis:
        
        **Content Analysis:**
        {json.dumps(content_analysis, indent=2)}
        
        **Existing Tags:** {existing_tags}
        
        **Tag Frequency in Collection:**
        {json.dumps(tag_frequency_data, indent=2)}
        
        Provide:
        1. **Primary Tags** (3-5 most important tags)
        2. **Secondary Tags** (additional relevant tags)
        3. **Technical Tags** (specific technologies/methodologies)
        4. **Contextual Tags** (workflow, purpose, audience tags)
        5. **Tag Rationale** (explain tag choices)
        6. **Tag Relationships** (how tags relate to each other)
        
        Format as JSON:
        {{
            "primary_tags": ["tag1", "tag2", "tag3"],
            "secondary_tags": ["tag4", "tag5"],
            "technical_tags": ["python", "api"],
            "contextual_tags": ["tutorial", "beginner"],
            "tag_rationale": "...",
            "tag_relationships": {{"parent_tag": ["child1", "child2"]}}
        }}
        """
        
        response = await self.agent.arun(prompt)
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {
                "primary_tags": [],
                "secondary_tags": [],
                "technical_tags": [],
                "contextual_tags": [],
                "tag_rationale": "Tag generation failed",
                "tag_relationships": {}
            }


class RelationshipMapperAgent:
    """Agent specialized in identifying document relationships."""
    
    def __init__(self):
        self.agent = Agent(
            name="Relationship Mapper",
            role="Expert knowledge graph specialist focusing on document relationships",
            model=Claude(id="claude-3-5-sonnet-20241022"),
            instructions=[
                "You are an expert knowledge graph specialist with deep understanding of document relationships.",
                "Identify semantic, topical, and structural relationships between documents.",
                "Consider content similarity, complementary information, and workflow relationships.",
                "Map both explicit references and implicit conceptual connections.",
                "Identify document clusters and knowledge domains.",
                "Suggest relationship types and strengths.",
            ],
            markdown=True,
        )
    
    async def map_relationships(self, current_doc: Dict[str, Any], 
                              other_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Identify relationships between current document and others."""
        prompt = f"""
        Identify relationships between this document and others in the collection:
        
        **Current Document:**
        {json.dumps(current_doc, indent=2)}
        
        **Other Documents (sample):**
        {json.dumps(other_docs[:10], indent=2)}  # Limit for context
        
        Identify:
        1. **Strong Relationships** (highly related documents)
        2. **Weak Relationships** (somewhat related documents)
        3. **Relationship Types** (prerequisite, complementary, similar, etc.)
        4. **Content Clusters** (groups of related documents)
        5. **Knowledge Gaps** (missing connections or documents)
        
        Format as JSON:
        {{
            "strong_relationships": [
                {{"document": "path/to/doc", "type": "prerequisite", "strength": 0.9, "reason": "..."}}
            ],
            "weak_relationships": [
                {{"document": "path/to/doc", "type": "similar", "strength": 0.6, "reason": "..."}}
            ],
            "content_clusters": ["cluster_name"],
            "knowledge_gaps": ["gap_description"]
        }}
        """
        
        response = await self.agent.arun(prompt)
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {
                "strong_relationships": [],
                "weak_relationships": [],
                "content_clusters": [],
                "knowledge_gaps": []
            }


class DataScienceOptimizerAgent:
    """Agent specialized in statistical analysis and optimization."""

    def __init__(self):
        self.agent = Agent(
            name="Data Science Optimizer",
            role="Expert data scientist specializing in information architecture optimization",
            model=OpenAIChat(id="gpt-4o"),
            instructions=[
                "You are an expert data scientist with deep knowledge of information architecture optimization.",
                "Analyze tag frequency distributions, category balance, and organizational efficiency.",
                "Identify statistical patterns, outliers, and optimization opportunities.",
                "Recommend data-driven improvements to organizational structure.",
                "Consider information theory principles like entropy and mutual information.",
                "Focus on measurable improvements to findability and cognitive load.",
            ],
            markdown=True,
        )

    async def optimize_structure(self, tag_analysis: Dict[str, Any],
                               category_analysis: Dict[str, Any],
                               relationship_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform statistical analysis and optimization recommendations."""
        prompt = f"""
        Analyze the organizational structure for optimization opportunities:

        **Tag Analysis:**
        {json.dumps(tag_analysis, indent=2)}

        **Category Analysis:**
        {json.dumps(category_analysis, indent=2)}

        **Relationship Data:**
        {json.dumps(relationship_data, indent=2)}

        Provide data-driven optimization recommendations:
        1. **Tag Consolidation** (merge similar/redundant tags)
        2. **Category Rebalancing** (address over/under-populated categories)
        3. **Hierarchy Optimization** (improve category depth/breadth)
        4. **Search Optimization** (improve findability metrics)
        5. **Cognitive Load Reduction** (simplify decision-making)
        6. **Metrics** (quantify improvements)

        Format as JSON:
        {{
            "tag_consolidation": [
                {{"merge": ["tag1", "tag2"], "into": "new_tag", "impact": "reduces redundancy by 15%"}}
            ],
            "category_rebalancing": [
                {{"action": "split", "category": "AI", "reason": "too broad", "suggestion": ["AI/Core", "AI/Applications"]}}
            ],
            "hierarchy_optimization": {{"max_depth": 3, "optimal_breadth": "5-9 per level"}},
            "search_optimization": ["add cross-references", "improve tag coverage"],
            "cognitive_load_reduction": ["reduce decision points", "clearer naming"],
            "metrics": {{"tag_reduction": "25%", "category_balance": "improved", "findability": "+30%"}}
        }}
        """

        response = await self.agent.arun(prompt)
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {
                "tag_consolidation": [],
                "category_rebalancing": [],
                "hierarchy_optimization": {},
                "search_optimization": [],
                "cognitive_load_reduction": [],
                "metrics": {}
            }


class OrganizationalStrategistAgent:
    """Agent specialized in high-level organizational strategy."""

    def __init__(self):
        self.agent = Agent(
            name="Organizational Strategist",
            role="Expert organizational strategist with deep knowledge of information architecture principles",
            model=Claude(id="claude-3-5-sonnet-20241022"),
            instructions=[
                "You are an expert organizational strategist with deep knowledge of information architecture.",
                "Synthesize all agent analyses into a coherent organizational strategy.",
                "Create deterministic rules for consistent categorization decisions.",
                "Design implementation plans that minimize disruption while maximizing benefit.",
                "Consider user workflows, maintenance overhead, and long-term scalability.",
                "Provide clear, actionable recommendations with implementation priorities.",
            ],
            markdown=True,
        )

    async def create_strategy(self, all_analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Create comprehensive organizational strategy from all agent analyses."""
        prompt = f"""
        Synthesize all agent analyses into a comprehensive organizational strategy:

        **All Agent Analyses:**
        {json.dumps(all_analyses, indent=2)}

        Create a comprehensive strategy including:
        1. **Executive Summary** (key findings and recommendations)
        2. **Implementation Plan** (phased approach with priorities)
        3. **Categorization Rules** (deterministic decision rules)
        4. **Tag Taxonomy** (hierarchical tag structure)
        5. **Migration Strategy** (how to transition existing content)
        6. **Success Metrics** (how to measure improvement)
        7. **Maintenance Guidelines** (ongoing organizational practices)

        Format as JSON:
        {{
            "executive_summary": "...",
            "implementation_plan": [
                {{"phase": 1, "priority": "high", "actions": ["action1", "action2"], "timeline": "1-2 weeks"}}
            ],
            "categorization_rules": [
                {{"rule": "if content_type == 'blog' then category = 'AI/Blog'", "priority": 1}}
            ],
            "tag_taxonomy": {{"parent_tag": ["child1", "child2"]}},
            "migration_strategy": {{"approach": "gradual", "steps": ["step1", "step2"]}},
            "success_metrics": ["metric1", "metric2"],
            "maintenance_guidelines": ["guideline1", "guideline2"]
        }}
        """

        response = await self.agent.arun(prompt)
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {
                "executive_summary": "Strategy creation failed",
                "implementation_plan": [],
                "categorization_rules": [],
                "tag_taxonomy": {},
                "migration_strategy": {},
                "success_metrics": [],
                "maintenance_guidelines": []
            }


class OrganizationalWorkflow:
    """Main workflow orchestrating all organizational agents."""

    def __init__(self, db_path: str = "tmp/organizational_analysis.db"):
        self.db = SqliteDb(
            session_table="organizational_session",
            db_file=db_path,
        )

        # Initialize all agents
        self.content_analyzer = ContentAnalyzerAgent()
        self.categorizer = CategorizerAgent()
        self.tagger = TaggerAgent()
        self.relationship_mapper = RelationshipMapperAgent()
        self.optimizer = DataScienceOptimizerAgent()
        self.strategist = OrganizationalStrategistAgent()

        # Create workflow steps
        self.workflow = self._create_workflow()

    def _create_workflow(self) -> Workflow:
        """Create the multi-agent workflow."""

        async def content_analysis_step(step_input: StepInput) -> StepOutput:
            """Step 1: Analyze all document content."""
            tree_data = json.loads(step_input.input)
            documents = self._extract_documents_from_tree(tree_data)

            analyses = []
            for doc in documents:
                content = await self._read_file_content(doc['path'])
                analysis = await self.content_analyzer.analyze_content(
                    doc['path'], content, doc.get('description', '')
                )
                analysis['path'] = doc['path']
                analyses.append(analysis)

            return StepOutput(content=json.dumps({"content_analyses": analyses}))

        async def categorization_step(step_input: StepInput) -> StepOutput:
            """Step 2: Categorize all documents."""
            data = json.loads(step_input.previous_step_content)
            content_analyses = data['content_analyses']

            categorizations = []
            for analysis in content_analyses:
                categorization = await self.categorizer.categorize_document(
                    analysis, analysis['path'], {}  # TODO: Add existing structure
                )
                categorization['path'] = analysis['path']
                categorizations.append(categorization)

            data['categorizations'] = categorizations
            return StepOutput(content=json.dumps(data))

        async def tagging_step(step_input: StepInput) -> StepOutput:
            """Step 3: Generate tags for all documents."""
            data = json.loads(step_input.previous_step_content)
            content_analyses = data['content_analyses']

            # Build tag frequency data
            tag_frequency = {}

            tagging_results = []
            for analysis in content_analyses:
                tags = await self.tagger.suggest_tags(
                    analysis, [], tag_frequency
                )
                tags['path'] = analysis['path']
                tagging_results.append(tags)

            data['tagging_results'] = tagging_results
            return StepOutput(content=json.dumps(data))

        async def relationship_mapping_step(step_input: StepInput) -> StepOutput:
            """Step 4: Map document relationships."""
            data = json.loads(step_input.previous_step_content)
            content_analyses = data['content_analyses']

            relationship_maps = []
            for i, analysis in enumerate(content_analyses):
                other_docs = content_analyses[:i] + content_analyses[i+1:]
                relationships = await self.relationship_mapper.map_relationships(
                    analysis, other_docs
                )
                relationships['path'] = analysis['path']
                relationship_maps.append(relationships)

            data['relationship_maps'] = relationship_maps
            return StepOutput(content=json.dumps(data))

        async def optimization_step(step_input: StepInput) -> StepOutput:
            """Step 5: Optimize organizational structure."""
            data = json.loads(step_input.previous_step_content)

            optimization = await self.optimizer.optimize_structure(
                data.get('tagging_results', {}),
                data.get('categorizations', {}),
                data.get('relationship_maps', {})
            )

            data['optimization'] = optimization
            return StepOutput(content=json.dumps(data))

        async def strategy_creation_step(step_input: StepInput) -> StepOutput:
            """Step 6: Create comprehensive organizational strategy."""
            data = json.loads(step_input.previous_step_content)

            strategy = await self.strategist.create_strategy(data)
            data['final_strategy'] = strategy

            return StepOutput(content=json.dumps(data))

        # Define workflow steps
        steps = [
            Step(name="Content Analysis", executor=content_analysis_step),
            Step(name="Categorization", executor=categorization_step),
            Step(name="Tagging", executor=tagging_step),
            Step(name="Relationship Mapping", executor=relationship_mapping_step),
            Step(name="Optimization", executor=optimization_step),
            Step(name="Strategy Creation", executor=strategy_creation_step),
        ]

        return Workflow(
            name="Organizational Analysis Workflow",
            description="Multi-agent system for intelligent documentation organization",
            db=self.db,
            steps=steps,
        )

    def _extract_documents_from_tree(self, tree_data: dict) -> List[Dict[str, Any]]:
        """Extract document information from tree JSON."""
        documents = []

        def extract_recursive(node):
            if node.get("type") == "file" and node["name"].endswith(".md"):
                doc = {
                    "path": node["path"],
                    "name": node["name"],
                }
                if "frontmatter" in node:
                    doc.update(node["frontmatter"])
                documents.append(doc)

            for child in node.get("children", []):
                extract_recursive(child)

        extract_recursive(tree_data)
        return documents

    async def _read_file_content(self, file_path: str) -> str:
        """Read file content for analysis."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Remove frontmatter for content analysis
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        content = parts[2].strip()
                return content[:5000]  # Limit content length
        except Exception:
            return ""

    async def analyze(self, tree_json_path: str) -> Dict[str, Any]:
        """Run the complete organizational analysis workflow."""
        with open(tree_json_path, 'r') as f:
            tree_data = f.read()

        result = await self.workflow.arun(tree_data)
        return json.loads(result.content)
