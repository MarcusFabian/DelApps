"""
Unit tests for the app_duplicate_remover module.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from _app_duplicate_remover import (
    parse_version,
    extract_name_and_version,
    find_app_files,
    group_files_by_name,
    identify_files_to_delete,
    main
)


class TestParseVersion:
    """Test cases for the parse_version function."""
    
    def test_parse_simple_version(self):
        """Test parsing simple version numbers."""
        assert parse_version("1.0.0.0") == (1, 0, 0, 0)
        assert parse_version("25.0.11.0") == (25, 0, 11, 0)
        assert parse_version("24.9.9.0") == (24, 9, 9, 0)
    
    def test_parse_different_length_versions(self):
        """Test parsing versions with different numbers of components."""
        assert parse_version("1.0") == (1, 0)
        assert parse_version("1.0.0") == (1, 0, 0)
        assert parse_version("1.0.0.0.1") == (1, 0, 0, 0, 1)
    
    def test_parse_invalid_version(self):
        """Test parsing invalid version strings."""
        assert parse_version("invalid") == (0,)
        assert parse_version("1.0.a.0") == (0,)
        assert parse_version("") == (0,)
    
    def test_version_comparison(self):
        """Test that parsed versions can be compared correctly."""
        v1 = parse_version("25.0.11.0")
        v2 = parse_version("24.9.9.0")
        v3 = parse_version("25.0.23364.25858")
        v4 = parse_version("25.0.23364.25649")
        
        assert v1 > v2
        assert v3 > v4
        assert v3 > v1


class TestExtractNameAndVersion:
    """Test cases for the extract_name_and_version function."""
    
    def test_extract_standard_format(self):
        """Test extracting from standard format files."""
        result = extract_name_and_version("EOS Solutions_Common Data Layer_25.0.11.0.app")
        assert result == ("EOS Solutions_Common Data Layer", "25.0.11.0")
        
        result = extract_name_and_version("Marcus Fabian_EPCIS Migros_24.9.9.0.app")
        assert result == ("Marcus Fabian_EPCIS Migros", "24.9.9.0")
    
    def test_extract_complex_names(self):
        """Test extracting from files with complex names."""
        result = extract_name_and_version("Microsoft_Base Application_25.0.23364.25858.app")
        assert result == ("Microsoft_Base Application", "25.0.23364.25858")
        
        result = extract_name_and_version("EOS Solutions_ISP.CDL.LE_24.0.1.3.app")
        assert result == ("EOS Solutions_ISP.CDL.LE", "24.0.1.3")
    
    def test_extract_non_app_files(self):
        """Test that non-.app files return None."""
        assert extract_name_and_version("somefile.txt") is None
        assert extract_name_and_version("README.md") is None
        assert extract_name_and_version("config.json") is None
    
    def test_extract_invalid_format(self):
        """Test extracting from files that don't match expected format."""
        assert extract_name_and_version("invalidformat.app") is None
        assert extract_name_and_version("no_version_here.app") is None


class TestGroupFilesByName:
    """Test cases for the group_files_by_name function."""
    
    def test_group_simple_files(self):
        """Test grouping simple file lists."""
        files = [
            "App1_1.0.0.0.app",
            "App1_2.0.0.0.app",
            "App2_1.0.0.0.app"
        ]
        
        result = group_files_by_name(files)
        
        assert len(result) == 2
        assert "App1" in result
        assert "App2" in result
        assert len(result["App1"]) == 2
        assert len(result["App2"]) == 1
    
    def test_group_real_files(self):
        """Test grouping with real file examples."""
        files = [
            "Marcus Fabian_EPCIS Migros_24.9.9.0.app",
            "Marcus Fabian_EPCIS Migros_25.0.9.0.app",
            "Microsoft_Base Application_25.0.23364.25649.app",
            "Microsoft_Base Application_25.0.23364.25858.app",
            "EOS Solutions_Common Data Layer_25.0.11.0.app"
        ]
        
        result = group_files_by_name(files)
        
        assert len(result) == 3
        assert "Marcus Fabian_EPCIS Migros" in result
        assert "Microsoft_Base Application" in result
        assert "EOS Solutions_Common Data Layer" in result
        assert len(result["Marcus Fabian_EPCIS Migros"]) == 2
        assert len(result["Microsoft_Base Application"]) == 2
        assert len(result["EOS Solutions_Common Data Layer"]) == 1


class TestIdentifyFilesToDelete:
    """Test cases for the identify_files_to_delete function."""
    
    def test_identify_with_duplicates(self):
        """Test identifying files when duplicates exist."""
        grouped_files = {
            "App1": [
                ("App1_1.0.0.0.app", "1.0.0.0"),
                ("App1_2.0.0.0.app", "2.0.0.0"),
                ("App1_1.5.0.0.app", "1.5.0.0")
            ],
            "App2": [
                ("App2_1.0.0.0.app", "1.0.0.0")
            ]
        }
        
        result = identify_files_to_delete(grouped_files)
        
        # Should delete the two older versions of App1
        assert len(result) == 2
        assert "App1_1.0.0.0.app" in result
        assert "App1_1.5.0.0.app" in result
        assert "App1_2.0.0.0.app" not in result  # Keep the highest version
        assert "App2_1.0.0.0.app" not in result  # No duplicates
    
    def test_identify_no_duplicates(self):
        """Test when no duplicates exist."""
        grouped_files = {
            "App1": [("App1_1.0.0.0.app", "1.0.0.0")],
            "App2": [("App2_1.0.0.0.app", "1.0.0.0")]
        }
        
        result = identify_files_to_delete(grouped_files)
        assert len(result) == 0


class TestIntegration:
    """Integration tests for the complete workflow."""
    
    def test_complete_workflow_dry_run(self):
        """Test the complete workflow in dry run mode."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            test_files = [
                "App1_1.0.0.0.app",
                "App1_2.0.0.0.app",
                "App2_1.0.0.0.app",
                "README.md"  # Non-app file
            ]
            
            for filename in test_files:
                (Path(temp_dir) / filename).touch()
            
            # Run the main function in dry run mode
            with patch('src.app_duplicate_remover.logging') as mock_logging:
                main(directory=temp_dir, dry_run=True)
            
            # Verify all files still exist (dry run)
            for filename in test_files:
                assert (Path(temp_dir) / filename).exists()
    
    def test_find_app_files(self):
        """Test finding .app files in a directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            test_files = ["App1_1.0.0.0.app", "App2_1.0.0.0.app", "README.md"]
            
            for filename in test_files:
                (Path(temp_dir) / filename).touch()
            
            result = find_app_files(temp_dir)
            
            assert len(result) == 2
            assert "App1_1.0.0.0.app" in result
            assert "App2_1.0.0.0.app" in result
            assert "README.md" not in result


if __name__ == "__main__":
    pytest.main([__file__])
