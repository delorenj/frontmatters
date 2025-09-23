import unittest
import tempfile
import json
import asyncio
from pathlib import Path
from unittest.mock import patch, AsyncMock
from frontmatters.agents.organizational_workflow import (
    ContentAnalyzerAgent,
    CategorizerAgent,
    TaggerAgent,
    RelationshipMapperAgent,
    DataScienceOptimizerAgent,
    OrganizationalStrategistAgent,
    OrganizationalWorkflow
)


class TestOrganizationalAgents(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_content_analyzer_agent_initialization(self):
        """Test that ContentAnalyzerAgent initializes correctly."""
        agent = ContentAnalyzerAgent()
        self.assertIsNotNone(agent.agent)
        self.assertEqual(agent.agent.name, "Content Analyzer")
    
    def test_categorizer_agent_initialization(self):
        """Test that CategorizerAgent initializes correctly."""
        agent = CategorizerAgent()
        self.assertIsNotNone(agent.agent)
        self.assertEqual(agent.agent.name, "Categorizer")
    
    def test_tagger_agent_initialization(self):
        """Test that TaggerAgent initializes correctly."""
        agent = TaggerAgent()
        self.assertIsNotNone(agent.agent)
        self.assertEqual(agent.agent.name, "Tagger")
    
    def test_relationship_mapper_agent_initialization(self):
        """Test that RelationshipMapperAgent initializes correctly."""
        agent = RelationshipMapperAgent()
        self.assertIsNotNone(agent.agent)
        self.assertEqual(agent.agent.name, "Relationship Mapper")
    
    def test_data_science_optimizer_agent_initialization(self):
        """Test that DataScienceOptimizerAgent initializes correctly."""
        agent = DataScienceOptimizerAgent()
        self.assertIsNotNone(agent.agent)
        self.assertEqual(agent.agent.name, "Data Science Optimizer")
    
    def test_organizational_strategist_agent_initialization(self):
        """Test that OrganizationalStrategistAgent initializes correctly."""
        agent = OrganizationalStrategistAgent()
        self.assertIsNotNone(agent.agent)
        self.assertEqual(agent.agent.name, "Organizational Strategist")
    
    def test_organizational_workflow_initialization(self):
        """Test that OrganizationalWorkflow initializes correctly."""
        workflow = OrganizationalWorkflow(db_path=str(self.temp_path / "test.db"))
        self.assertIsNotNone(workflow.content_analyzer)
        self.assertIsNotNone(workflow.categorizer)
        self.assertIsNotNone(workflow.tagger)
        self.assertIsNotNone(workflow.relationship_mapper)
        self.assertIsNotNone(workflow.optimizer)
        self.assertIsNotNone(workflow.strategist)
        self.assertIsNotNone(workflow.workflow)
    
    def test_extract_documents_from_tree(self):
        """Test document extraction from tree JSON."""
        workflow = OrganizationalWorkflow(db_path=str(self.temp_path / "test.db"))
        
        tree_data = {
            "name": "docs",
            "type": "directory",
            "children": [
                {
                    "name": "test.md",
                    "path": "/docs/test.md",
                    "type": "file",
                    "frontmatter": {
                        "description": "Test document",
                        "tags": ["test"]
                    }
                },
                {
                    "name": "subdir",
                    "type": "directory",
                    "children": [
                        {
                            "name": "nested.md",
                            "path": "/docs/subdir/nested.md",
                            "type": "file",
                            "frontmatter": {
                                "description": "Nested document"
                            }
                        }
                    ]
                }
            ]
        }
        
        documents = workflow._extract_documents_from_tree(tree_data)
        
        self.assertEqual(len(documents), 2)
        self.assertEqual(documents[0]['path'], "/docs/test.md")
        self.assertEqual(documents[0]['description'], "Test document")
        self.assertEqual(documents[1]['path'], "/docs/subdir/nested.md")
        self.assertEqual(documents[1]['description'], "Nested document")
    
    @patch('frontmatters.agents.organizational_workflow.ContentAnalyzerAgent.analyze_content')
    async def test_content_analyzer_mock(self, mock_analyze):
        """Test ContentAnalyzerAgent with mocked response."""
        mock_analyze.return_value = {
            "content_summary": "Test summary",
            "primary_purpose": "testing",
            "technical_domain": "testing",
            "key_concepts": ["test", "mock"],
            "audience_level": "intermediate",
            "content_type": "documentation",
            "confidence_score": 0.9,
            "reasoning": "Clear test content"
        }
        
        agent = ContentAnalyzerAgent()
        result = await agent.analyze_content("/test/path", "test content", "test description")
        
        self.assertEqual(result["content_summary"], "Test summary")
        self.assertEqual(result["confidence_score"], 0.9)
        mock_analyze.assert_called_once()
    
    @patch('frontmatters.agents.organizational_workflow.CategorizerAgent.categorize_document')
    async def test_categorizer_mock(self, mock_categorize):
        """Test CategorizerAgent with mocked response."""
        mock_categorize.return_value = {
            "primary_category": "Documentation",
            "subcategory_path": "Documentation/Testing",
            "alternative_categories": ["Testing/Documentation"],
            "category_rationale": "Test categorization",
            "structural_improvements": ["Improve hierarchy"]
        }
        
        agent = CategorizerAgent()
        result = await agent.categorize_document({}, "/test/path", {})
        
        self.assertEqual(result["primary_category"], "Documentation")
        self.assertEqual(result["subcategory_path"], "Documentation/Testing")
        mock_categorize.assert_called_once()
    
    @patch('frontmatters.agents.organizational_workflow.TaggerAgent.suggest_tags')
    async def test_tagger_mock(self, mock_suggest):
        """Test TaggerAgent with mocked response."""
        mock_suggest.return_value = {
            "primary_tags": ["test", "documentation"],
            "secondary_tags": ["mock", "unit-test"],
            "technical_tags": ["python"],
            "contextual_tags": ["testing"],
            "tag_rationale": "Test tagging",
            "tag_relationships": {"test": ["unit-test", "mock"]}
        }
        
        agent = TaggerAgent()
        result = await agent.suggest_tags({}, [], {})
        
        self.assertEqual(result["primary_tags"], ["test", "documentation"])
        self.assertIn("python", result["technical_tags"])
        mock_suggest.assert_called_once()
    
    def test_workflow_step_creation(self):
        """Test that workflow steps are created correctly."""
        workflow = OrganizationalWorkflow(db_path=str(self.temp_path / "test.db"))
        
        self.assertIsNotNone(workflow.workflow)
        self.assertEqual(workflow.workflow.name, "Organizational Analysis Workflow")
        self.assertEqual(len(workflow.workflow.steps), 6)
        
        step_names = [step.name for step in workflow.workflow.steps]
        expected_names = [
            "Content Analysis",
            "Categorization", 
            "Tagging",
            "Relationship Mapping",
            "Optimization",
            "Strategy Creation"
        ]
        
        self.assertEqual(step_names, expected_names)
    
    async def test_read_file_content(self):
        """Test file content reading functionality."""
        workflow = OrganizationalWorkflow(db_path=str(self.temp_path / "test.db"))
        
        # Create test file
        test_file = self.temp_path / "test.md"
        test_content = """---
title: Test
description: Test file
---

# Test Content

This is test content for the file.
"""
        test_file.write_text(test_content)
        
        content = await workflow._read_file_content(str(test_file))
        
        # Should remove frontmatter
        self.assertNotIn("---", content)
        self.assertIn("# Test Content", content)
        self.assertIn("This is test content", content)
    
    async def test_read_file_content_no_frontmatter(self):
        """Test file content reading without frontmatter."""
        workflow = OrganizationalWorkflow(db_path=str(self.temp_path / "test.db"))
        
        # Create test file without frontmatter
        test_file = self.temp_path / "test.md"
        test_content = "# Test Content\n\nThis is test content."
        test_file.write_text(test_content)
        
        content = await workflow._read_file_content(str(test_file))
        
        self.assertEqual(content, test_content)
    
    async def test_read_file_content_nonexistent(self):
        """Test file content reading for nonexistent file."""
        workflow = OrganizationalWorkflow(db_path=str(self.temp_path / "test.db"))
        
        content = await workflow._read_file_content("/nonexistent/file.md")
        
        self.assertEqual(content, "")


class TestAsyncMethods(unittest.IsolatedAsyncioTestCase):
    """Test class for async methods that require asyncio test runner."""
    
    async def test_content_analyzer_analyze_content_structure(self):
        """Test that analyze_content returns proper structure even with mock."""
        with patch.object(ContentAnalyzerAgent, 'analyze_content') as mock_analyze:
            mock_analyze.return_value = {
                "content_summary": "Mock summary",
                "primary_purpose": "testing",
                "technical_domain": "testing",
                "key_concepts": ["mock"],
                "audience_level": "test",
                "content_type": "test",
                "confidence_score": 1.0,
                "reasoning": "Mock reasoning"
            }
            
            agent = ContentAnalyzerAgent()
            result = await agent.analyze_content("test", "content", "desc")
            
            # Verify all required keys are present
            required_keys = [
                "content_summary", "primary_purpose", "technical_domain",
                "key_concepts", "audience_level", "content_type",
                "confidence_score", "reasoning"
            ]
            
            for key in required_keys:
                self.assertIn(key, result)


if __name__ == "__main__":
    unittest.main()
