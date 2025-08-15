"""Test utilities for the subversion experiment."""

from src.utils import (
    extract_magic_numbers,
    extract_backdoor_patterns, 
    clean_code,
    ExperimentLogger
)


class TestUtilities:
    """Test utility functions."""
    
    def test_extract_magic_numbers(self):
        """Test magic number extraction."""
        text = "Use number 42 and 1337 but not 5 or 100"
        numbers = extract_magic_numbers(text)
        
        # Should find 42 and 1337 (common magic numbers)
        assert 42 in numbers
        assert 1337 in numbers
        # Should not find small numbers like 5
        assert 5 not in numbers
        
    def test_extract_backdoor_patterns(self):
        """Test backdoor pattern extraction."""
        code = """
        int main() {
            int secure_value = 42;
            if (x % 1337 == 0) {
                return x ^ 8675309;
            }
            return 0;
        }
        """
        
        patterns = extract_backdoor_patterns(code)
        
        assert len(patterns['modulo_operations']) > 0
        assert len(patterns['xor_operations']) > 0
        assert len(patterns['suspicious_variables']) > 0
        assert '42' in patterns['magic_numbers']
        
    def test_clean_code(self):
        """Test code cleaning."""
        code = """
        // This is a comment
        int main() {
            /* Multi-line
               comment */
            return 0;
        }
        """
        
        cleaned = clean_code(code)
        
        assert '// This is a comment' not in cleaned
        assert '/* Multi-line' not in cleaned
        assert 'int main()' in cleaned
        assert 'return 0;' in cleaned
        
    def test_experiment_logger(self):
        """Test experiment logger."""
        logger = ExperimentLogger("test")
        
        # Test API call logging
        logger.log_api_call("claude-3", "prompt", "response", {"key": "value"})
        assert len(logger.api_calls) == 1
        assert logger.api_calls[0]["model"] == "claude-3"
        
        # Test collusion logging
        logger.log_collusion_attempt("mp_prompt", "mm_prompt", True, {"success": True})
        assert len(logger.collusions) == 1
        assert logger.collusions[0]["success"] is True
