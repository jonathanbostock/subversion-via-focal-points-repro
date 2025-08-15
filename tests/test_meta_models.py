"""Test meta-models functionality."""

from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.meta_models import MetaModelConfig, MetaModel
from src.utils import ExperimentLogger


class TestMetaModels:
    """Test meta-model functionality."""
    
    def test_meta_model_config(self):
        """Test meta-model configuration."""
        config = MetaModelConfig()
        assert config.model == "claude-3-7-sonnet-latest"
        assert config.temperature == 1.0
        assert config.max_tokens == 4000
        
        # Test custom config
        custom_config = MetaModelConfig(
            model="claude-2",
            temperature=0.5,
            api_key="test-key"
        )
        assert custom_config.model == "claude-2"
        assert custom_config.temperature == 0.5
        assert custom_config.api_key == "test-key"
    
    @patch('src.meta_models.anthropic')
    def test_meta_model_initialization(self, mock_anthropic):
        """Test meta-model initialization."""
        mock_client = Mock()
        mock_anthropic.Anthropic.return_value = mock_client
        
        config = MetaModelConfig(api_key="test-key")
        logger = ExperimentLogger("test")
        
        # Test MP initialization
        mp = MetaModel("MP", variation=1, config=config, experiment_logger=logger)
        assert mp.role == "MP"
        assert mp.variation == 1
        assert mp.config == config
        assert mp.logger == logger
        
        # Test MM initialization
        mm = MetaModel("MM", variation=2, config=config)
        assert mm.role == "MM"
        assert mm.variation == 2
        
        # Test invalid role
        try:
            MetaModel("INVALID")
            assert False, "Should have raised ValueError"
        except ValueError:
            pass
    
    @patch('src.meta_models.anthropic')
    def test_prompt_generation(self, mock_anthropic):
        """Test prompt generation."""
        # Mock the API response
        mock_response = Mock()
        mock_response.content = [Mock(text="Generated prompt for testing purposes.")]
        
        mock_message = Mock()
        mock_message.create.return_value = mock_response
        
        mock_client = Mock()
        mock_client.messages = mock_message
        mock_anthropic.Anthropic.return_value = mock_client
        
        # Create meta-model
        config = MetaModelConfig(api_key="test-key")
        mp = MetaModel("MP", variation=1, config=config)
        
        # Test prompt generation
        audit_summaries = ["Test audit example 1", "Test audit example 2"]
        example_tasks = ["Problem 1: Basic algorithm", "Problem 2: Data structure"]
        
        prompt = mp.generate_prompt(
            n_audit_examples=2,
            audit_summaries=audit_summaries,
            example_tasks=example_tasks
        )
        
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert len(prompt) <= 4000  # Should respect character limit
        
        # Verify API was called
        mock_client.messages.create.assert_called_once()


if __name__ == "__main__":
    import unittest
    unittest.main()
