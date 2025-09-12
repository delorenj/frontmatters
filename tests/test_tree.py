import unittest
import tempfile
import os
import json
from pathlib import Path
from unittest.mock import patch
from typer.testing import CliRunner
from frontmatters.commands.tree import app, get_frontmatter_display, format_tree_line, build_json_tree
from frontmatters.core.processor import FrontmatterProcessor


class TestTreeCommand(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
    
    def tearDown(self):
        # Clean up temp directory
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def create_test_file(self, path: str, content: str):
        """Helper to create test files with content."""
        file_path = self.temp_path / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
        return file_path
    
    def test_format_tree_line_basic(self):
        """Test basic tree line formatting."""
        path = Path("test.md")
        line = format_tree_line(path, 0, True, [], "[description]")
        self.assertEqual(line, "└── test.md [description]")
    
    def test_format_tree_line_with_depth(self):
        """Test tree line formatting with depth."""
        path = Path("test.md")
        line = format_tree_line(path, 1, False, [False], "[description]")
        self.assertEqual(line, "│   ├── test.md [description]")
    
    def test_get_frontmatter_display_description(self):
        """Test extracting description from frontmatter."""
        content = """---
title: Test
description: This is a test file
---
# Test Content"""
        
        file_path = self.create_test_file("test.md", content)
        result = get_frontmatter_display(file_path, True, False)
        self.assertEqual(result, " [This is a test file]")
    
    def test_get_frontmatter_display_tags(self):
        """Test extracting tags from frontmatter."""
        content = """---
title: Test
tags: [python, testing, markdown]
---
# Test Content"""
        
        file_path = self.create_test_file("test.md", content)
        result = get_frontmatter_display(file_path, False, True)
        self.assertEqual(result, " #python, testing, markdown")
    
    def test_get_frontmatter_display_both(self):
        """Test extracting both description and tags."""
        content = """---
title: Test
description: A test file
tags: [python, test]
---
# Test Content"""
        
        file_path = self.create_test_file("test.md", content)
        result = get_frontmatter_display(file_path, True, True)
        self.assertEqual(result, " [A test file] #python, test")
    
    def test_get_frontmatter_display_long_description(self):
        """Test truncation of long descriptions."""
        long_desc = "This is a very long description that should be truncated because it exceeds the maximum length"
        content = f"""---
title: Test
description: {long_desc}
---
# Test Content"""
        
        file_path = self.create_test_file("test.md", content)
        result = get_frontmatter_display(file_path, True, False)
        self.assertTrue(result.endswith("...]"))
        self.assertTrue(len(result) <= 65)  # Account for " [" and "...]"
    
    def test_get_frontmatter_display_non_markdown(self):
        """Test that non-markdown files return empty string."""
        file_path = self.create_test_file("test.txt", "Some content")
        result = get_frontmatter_display(file_path, True, True)
        self.assertEqual(result, "")
    
    def test_tree_command_basic(self):
        """Test basic tree command functionality."""
        # Create test structure
        self.create_test_file("file1.md", """---
description: First file
---
# File 1""")
        
        self.create_test_file("subdir/file2.md", """---
description: Second file
tags: [test, example]
---
# File 2""")
        
        os.mkdir(self.temp_path / "empty_dir")
        
        result = self.runner.invoke(app, [str(self.temp_path)])

        self.assertEqual(result.exit_code, 0)
        output = result.stdout

        # Check that the tree structure is present
        self.assertIn("├── empty_dir", output)
        self.assertIn("├── subdir", output)
        self.assertIn("└── file2.md  [Second file]", output)  # Last item in subdir (note extra space)
        self.assertIn("└── file1.md  [First file]", output)  # Last item overall
    
    def test_tree_command_tags_only(self):
        """Test tree command with tags only."""
        self.create_test_file("test.md", """---
description: Test description
tags: [python, test]
---
# Test""")
        
        result = self.runner.invoke(app, [str(self.temp_path), "--tags"])
        
        self.assertEqual(result.exit_code, 0)
        self.assertIn("#python, test", result.stdout)
        self.assertNotIn("[Test description]", result.stdout)
    
    def test_tree_command_both_flags(self):
        """Test tree command with both description and tags."""
        self.create_test_file("test.md", """---
description: Test description
tags: [python, test]
---
# Test""")
        
        result = self.runner.invoke(app, [str(self.temp_path), "--both"])
        
        self.assertEqual(result.exit_code, 0)
        self.assertIn("[Test description]", result.stdout)
        self.assertIn("#python, test", result.stdout)
    
    def test_tree_command_depth_limit(self):
        """Test tree command with depth limit."""
        # Create nested structure
        self.create_test_file("level1/level2/level3/deep.md", """---
description: Deep file
---
# Deep""")
        
        result = self.runner.invoke(app, [str(self.temp_path), "--depth", "2"])
        
        self.assertEqual(result.exit_code, 0)
        # Should show level1 and level2, but not level3 or deep.md
        self.assertIn("level1", result.stdout)
        self.assertIn("level2", result.stdout)
        self.assertNotIn("level3", result.stdout)
        self.assertNotIn("deep.md", result.stdout)
    
    def test_tree_command_nonexistent_path(self):
        """Test tree command with nonexistent path."""
        result = self.runner.invoke(app, ["/nonexistent/path"])
        
        self.assertEqual(result.exit_code, 1)
        self.assertIn("does not exist", result.stderr)
    
    def test_tree_command_file_path(self):
        """Test tree command with file path instead of directory."""
        file_path = self.create_test_file("test.md", "# Test")

        result = self.runner.invoke(app, [str(file_path)])

        self.assertEqual(result.exit_code, 1)
        self.assertIn("is not a directory", result.stderr)

    def test_tree_command_json_output(self):
        """Test tree command with JSON output."""
        self.create_test_file("test.md", """---
description: Test description
tags: [python, test]
---
# Test""")

        result = self.runner.invoke(app, [str(self.temp_path), "--json"])

        self.assertEqual(result.exit_code, 0)

        # Parse JSON output
        json_data = json.loads(result.stdout)

        # Check structure
        self.assertEqual(json_data["type"], "directory")
        self.assertIn("children", json_data)

        # Find the test.md file
        test_file = None
        for child in json_data["children"]:
            if child["name"] == "test.md":
                test_file = child
                break

        self.assertIsNotNone(test_file)
        self.assertEqual(test_file["type"], "file")
        self.assertIn("frontmatter", test_file)
        self.assertEqual(test_file["frontmatter"]["description"], "Test description")

    def test_tree_command_json_with_tags(self):
        """Test tree command with JSON output showing tags."""
        self.create_test_file("test.md", """---
description: Test description
tags: [python, test]
---
# Test""")

        result = self.runner.invoke(app, [str(self.temp_path), "--json", "--tags"])

        self.assertEqual(result.exit_code, 0)

        # Parse JSON output
        json_data = json.loads(result.stdout)

        # Find the test.md file
        test_file = None
        for child in json_data["children"]:
            if child["name"] == "test.md":
                test_file = child
                break

        self.assertIsNotNone(test_file)
        self.assertIn("frontmatter", test_file)
        self.assertEqual(test_file["frontmatter"]["tags"], ["python", "test"])
        self.assertNotIn("description", test_file["frontmatter"])

    def test_tree_command_output_file(self):
        """Test tree command with file output."""
        self.create_test_file("test.md", """---
description: Test description
---
# Test""")

        output_file = self.temp_path / "output.txt"

        result = self.runner.invoke(app, [str(self.temp_path), "--output", str(output_file)])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Output written to", result.stdout)

        # Check file was created and has content
        self.assertTrue(output_file.exists())
        content = output_file.read_text()
        self.assertIn("test.md  [Test description]", content)

    def test_tree_command_json_output_file(self):
        """Test tree command with JSON output to file."""
        self.create_test_file("test.md", """---
description: Test description
tags: [python, test]
---
# Test""")

        output_file = self.temp_path / "output.json"

        result = self.runner.invoke(app, [str(self.temp_path), "--json", "--both", "--output", str(output_file)])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Output written to", result.stdout)

        # Check file was created and has valid JSON
        self.assertTrue(output_file.exists())
        with open(output_file) as f:
            json_data = json.load(f)

        # Find the test.md file
        test_file = None
        for child in json_data["children"]:
            if child["name"] == "test.md":
                test_file = child
                break

        self.assertIsNotNone(test_file)
        self.assertIn("frontmatter", test_file)
        self.assertEqual(test_file["frontmatter"]["description"], "Test description")
        self.assertEqual(test_file["frontmatter"]["tags"], ["python", "test"])


if __name__ == "__main__":
    unittest.main()
