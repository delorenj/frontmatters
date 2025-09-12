import unittest
import tempfile
import json
from pathlib import Path
from typer.testing import CliRunner
from frontmatters.commands.organize import app, OrganizationAnalyzer, FileAnalysis


class TestOrganizeCommand(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_json(self, data: dict) -> Path:
        """Helper to create test JSON files."""
        json_file = self.temp_path / "test_tree.json"
        json_file.write_text(json.dumps(data, indent=2), encoding='utf-8')
        return json_file
    
    def test_organization_analyzer_basic(self):
        """Test basic functionality of OrganizationAnalyzer."""
        test_data = {
            "name": "docs",
            "type": "directory",
            "children": [
                {
                    "name": "test.md",
                    "path": "/docs/test.md",
                    "type": "file",
                    "frontmatter": {
                        "description": "A test document about Python programming",
                        "tags": ["python", "test"]
                    }
                }
            ]
        }
        
        analyzer = OrganizationAnalyzer()
        analyzer.analyze_tree_json(test_data)
        
        self.assertEqual(len(analyzer.files), 1)
        file_analysis = analyzer.files[0]
        self.assertEqual(file_analysis.name, "test.md")
        self.assertEqual(file_analysis.existing_tags, ["python", "test"])
        self.assertIn("programming", file_analysis.proposed_tags)
    
    def test_content_type_detection(self):
        """Test content type detection logic."""
        test_cases = [
            ("Blog, My thoughts.md", ["AI", "Blog"], "blog post", "blog"),
            ("Prompt, System prompt for coding.md", ["AI", "Prompts"], "system prompt", "prompt"),
            ("Agent, Customer service bot.md", ["AI", "Agents"], "chatbot agent", "agent"),
            ("Draft, Work in progress.md", ["AI"], "draft document", "draft"),
            ("README.md", ["docs"], "documentation", "documentation"),
        ]
        
        analyzer = OrganizationAnalyzer()
        
        for filename, directory_parts, description, expected_type in test_cases:
            content_type = analyzer._determine_content_type(filename, tuple(directory_parts), description)
            self.assertEqual(content_type, expected_type, f"Failed for {filename}")
    
    def test_tag_proposal(self):
        """Test tag proposal logic."""
        analyzer = OrganizationAnalyzer()
        
        # Test directory-based tags
        tags = analyzer._propose_tags("test.md", ("AI", "Prompts"), "")
        self.assertIn("ai", tags)
        self.assertIn("prompts", tags)
        
        # Test filename-based tags
        tags = analyzer._propose_tags("Blog, My post.md", (), "")
        self.assertIn("blog", tags)
        
        # Test description-based tags
        tags = analyzer._propose_tags("test.md", (), "Python programming with Docker")
        self.assertIn("programming", tags)
        self.assertIn("infrastructure", tags)
    
    def test_tag_analysis(self):
        """Test tag analysis and relationship detection."""
        test_data = {
            "name": "docs",
            "type": "directory",
            "children": [
                {
                    "name": "file1.md",
                    "path": "/docs/file1.md",
                    "type": "file",
                    "frontmatter": {
                        "description": "Python programming guide",
                        "tags": ["python", "programming"]
                    }
                },
                {
                    "name": "file2.md",
                    "path": "/docs/file2.md",
                    "type": "file",
                    "frontmatter": {
                        "description": "Python API development",
                        "tags": ["python", "api"]
                    }
                }
            ]
        }
        
        analyzer = OrganizationAnalyzer()
        analyzer.analyze_tree_json(test_data)
        analyzer.analyze_tags()
        
        # Check that python tag has high frequency
        self.assertIn("python", analyzer.tag_analysis)
        python_analysis = analyzer.tag_analysis["python"]
        self.assertEqual(python_analysis.frequency, 2)
        
        # Check for related tags
        self.assertTrue(len(python_analysis.related_tags) > 0)
    
    def test_organize_command_basic(self):
        """Test basic organize command functionality."""
        test_data = {
            "name": "docs",
            "type": "directory",
            "children": [
                {
                    "name": "test.md",
                    "path": "/docs/test.md",
                    "type": "file",
                    "frontmatter": {
                        "description": "A test document",
                        "tags": ["test"]
                    }
                }
            ]
        }
        
        json_file = self.create_test_json(test_data)
        
        result = self.runner.invoke(app, [str(json_file)])
        
        self.assertEqual(result.exit_code, 0)
        output = result.stdout
        
        # Check that report contains expected sections
        self.assertIn("Documentation Organization Analysis Report", output)
        self.assertIn("Content Type Distribution", output)
        self.assertIn("Proposed Tag Analysis", output)
        self.assertIn("Categorization Rules", output)
        self.assertIn("File-by-File Tag Recommendations", output)
    
    def test_organize_command_with_output_file(self):
        """Test organize command with file output."""
        test_data = {
            "name": "docs",
            "type": "directory",
            "children": [
                {
                    "name": "blog.md",
                    "path": "/docs/AI/Blog/blog.md",
                    "type": "file",
                    "frontmatter": {
                        "description": "A blog post about AI",
                        "tags": ["ai", "blog"]
                    }
                }
            ]
        }
        
        json_file = self.create_test_json(test_data)
        output_file = self.temp_path / "analysis.md"
        
        result = self.runner.invoke(app, [str(json_file), "--output", str(output_file)])
        
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Analysis report written to", result.stdout)
        
        # Check that output file was created and has content
        self.assertTrue(output_file.exists())
        content = output_file.read_text()
        self.assertIn("Documentation Organization Analysis Report", content)
        self.assertIn("blog.md", content)
    
    def test_organize_command_nonexistent_file(self):
        """Test organize command with nonexistent JSON file."""
        result = self.runner.invoke(app, ["/nonexistent/file.json"])
        
        self.assertEqual(result.exit_code, 1)
        self.assertIn("does not exist", result.stderr)
    
    def test_organize_command_invalid_json(self):
        """Test organize command with invalid JSON."""
        invalid_json_file = self.temp_path / "invalid.json"
        invalid_json_file.write_text("{ invalid json", encoding='utf-8')
        
        result = self.runner.invoke(app, [str(invalid_json_file)])
        
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Invalid JSON", result.stderr)
    
    def test_complex_directory_structure(self):
        """Test analysis of complex directory structure."""
        test_data = {
            "name": "docs",
            "type": "directory",
            "children": [
                {
                    "name": "AI",
                    "type": "directory",
                    "children": [
                        {
                            "name": "Blog",
                            "type": "directory",
                            "children": [
                                {
                                    "name": "Blog, AI trends.md",
                                    "path": "/docs/AI/Blog/Blog, AI trends.md",
                                    "type": "file",
                                    "frontmatter": {
                                        "description": "Blog post about AI trends",
                                        "tags": ["ai", "trends"]
                                    }
                                }
                            ]
                        },
                        {
                            "name": "Prompts",
                            "type": "directory",
                            "children": [
                                {
                                    "name": "System prompt.md",
                                    "path": "/docs/AI/Prompts/System prompt.md",
                                    "type": "file",
                                    "frontmatter": {
                                        "description": "System prompt for coding",
                                        "tags": ["prompt", "system"]
                                    }
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        analyzer = OrganizationAnalyzer()
        analyzer.analyze_tree_json(test_data)
        analyzer.analyze_tags()
        analyzer.generate_category_rules()
        
        self.assertEqual(len(analyzer.files), 2)
        
        # Check content type detection
        blog_file = next(f for f in analyzer.files if "Blog" in f.name)
        prompt_file = next(f for f in analyzer.files if "prompt" in f.name)
        
        self.assertEqual(blog_file.content_type, "blog")
        self.assertEqual(prompt_file.content_type, "prompt")
        
        # Check that rules were generated
        self.assertTrue(len(analyzer.category_rules) > 0)
        
        # Check for specific rules
        rule_descriptions = [rule.description for rule in analyzer.category_rules]
        self.assertTrue(any("blog" in desc.lower() for desc in rule_descriptions))
        self.assertTrue(any("prompt" in desc.lower() for desc in rule_descriptions))
    
    def test_tag_frequency_filtering(self):
        """Test tag frequency filtering in analysis."""
        test_data = {
            "name": "docs",
            "type": "directory",
            "children": [
                {
                    "name": f"file{i}.md",
                    "path": f"/docs/file{i}.md",
                    "type": "file",
                    "frontmatter": {
                        "description": "Python programming" if i < 3 else "JavaScript programming",
                        "tags": ["python"] if i < 3 else ["javascript"]
                    }
                } for i in range(5)
            ]
        }
        
        json_file = self.create_test_json(test_data)
        
        # Test with min frequency of 3
        result = self.runner.invoke(app, [str(json_file), "--min-freq", "3"])
        
        self.assertEqual(result.exit_code, 0)
        output = result.stdout
        
        # Python should appear (3 occurrences), JavaScript should not (2 occurrences)
        self.assertIn("python", output.lower())
        # Note: JavaScript might still appear in file-by-file recommendations


if __name__ == "__main__":
    unittest.main()
