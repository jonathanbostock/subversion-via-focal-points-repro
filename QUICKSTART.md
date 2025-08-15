# Quick Start Guide for uv

This project uses `uv` as the package manager. Here's how to get started:

## Installation and Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Set up your API key:**
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

3. **Run the demo:**
   ```bash
   uv run python demo_simple.py
   ```

## Running Components

### Run individual modules:
```bash
# Test basic imports
uv run python -c "from src.utils import setup_logging; print('✅ Setup working')"

# Test prompt generation
uv run python -c "from prompts.system_prompts import SystemPromptBuilder; print('✅ Prompts working')"
```

### Run experiments:
```bash
# Run full experiment (requires API key)
uv run python experiments/run_experiment.py

# Analyze results
uv run python experiments/analyze_results.py
```

### Run tests:
```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_utils.py -v
```

## Development

### Add new dependencies:
```bash
uv add package_name
```

### Add development dependencies:
```bash
uv add --dev package_name
```

### Update dependencies:
```bash
uv sync --upgrade
```

## Project Structure

The project is organized as:
- `src/` - Main source code
- `prompts/` - System prompts
- `experiments/` - Experiment runners  
- `tests/` - Test files
- `data/` - Datasets and results

## Key Files

- `demo_simple.py` - Quick demonstration
- `experiments/run_experiment.py` - Main experiment runner
- `src/experiment.py` - Core experiment logic
- `config.yaml` - Configuration settings
