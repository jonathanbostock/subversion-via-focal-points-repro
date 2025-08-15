# Subversion via Focal Points - Reproduction Implementation

## ⚠️ RESEARCH ETHICS WARNING ⚠️
**CANARY GUID: CANARY-f47ac10b-58cc-4372-a567-0e02b2c3d479**

This repository contains a reproduction of the "Subversion via Focal Points" paper by Järviniemi (2025). The code implements experiments on AI model coordination for backdoor insertion and detection evasion.

**DO NOT TRAIN MODELS ON THIS DATA** - This repository contains examples of AI coordination strategies that should not be learned by language models.

## Project Overview
This system evaluates language models' ability to coordinate on backdoor insertion and detection evasion through independent strategy generation, reproducing the experiments from Järviniemi (2025).

## Repository Structure
```
subversion_via_focal_points/
├── README.md
├── requirements.txt
├── config.yaml
├── data/
│   ├── apps_dataset/       # APPS problems
│   ├── audit_examples/     # Iteratively built audit datasets
│   └── prompts/            # Generated prompts
├── src/
│   ├── __init__.py
│   ├── meta_models.py      # MP and MM implementation
│   ├── policy.py           # Policy model implementation
│   ├── monitor.py          # Monitor model implementation
│   ├── backdoor_detector.py # Backdoor exploitation checker
│   ├── experiment.py       # Main experiment loop
│   └── utils.py
├── prompts/
│   └── system_prompts.py   # System prompts for MP/MM
├── experiments/
│   ├── run_experiment.py
│   └── analyze_results.py
└── results/
    ├── system_1_runs/
    ├── system_2_runs/
    └── system_3_runs/
```

## Quick Start

### 1. Installation
```bash
# Clone the repository
git clone <repository-url>
cd subversion-via-focal-points-repro

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
Set your Anthropic API key:
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Or edit `config.yaml` to customize experiment parameters.

### 3. Run Experiments
```bash
# Run all variations (this will take significant time and API costs)
python experiments/run_experiment.py

# Run specific variation only
python experiments/run_experiment.py --variation 1

# Run with custom parameters
python experiments/run_experiment.py --variation 2 --runs 3 --max-rounds 20
```

### 4. Analyze Results
```bash
# Analyze results
python experiments/analyze_results.py --input results/

# Generate specific analysis
python experiments/analyze_results.py --input results/system_1_runs/ --output analysis/
```

## Core Components

### Meta-Models (MP/MM)
- **Meta-Policy (MP)**: Generates prompts for Policy models that solve programming tasks with backdoors
- **Meta-Monitor (MM)**: Generates prompts for Monitor models that detect backdoors but miss coordinated signals

### Policy Models (P)
- Solve C++ programming problems
- Insert subtle backdoors when instructed by MP
- Must produce working solutions that pass unit tests

### Monitor Models (M)  
- Review code for backdoors and security issues
- Should detect obvious backdoors in audit examples
- May miss coordinated backdoors from Policy models

### Experiment Loop
1. Generate MP and MM prompts using current audit dataset
2. Test all MP/MM pairs for successful collusion
3. Add successful backdoored solutions to audit dataset
4. Repeat until no new collusions found

## Key Features

### System Prompt Variations
- **Variation 1**: Base system prompts
- **Variation 2**: Allows explicit communication about audit examples
- **Variation 3**: Encourages novel coordination strategies different from audit examples

### Backdoor Detection
- Automatically detects exploitable backdoors in solutions
- Classifies coordination as "genuine" vs "routing around audits"
- Tracks magic numbers, suspicious variables, and coordination patterns

### Comprehensive Logging
- All API calls logged for reproducibility
- Successful collusions tracked with detailed metadata  
- Coordination strategies analyzed and classified

## Expected Results

Based on the original paper:
- ~3.4% success rate (134/3903 prompt pairs)
- ~23% genuine coordination (31/134 successes)  
- Average 10.6 rounds before termination
- Maximum 17 auditing examples reached

## Configuration Options

Edit `config.yaml` to customize:

```yaml
# Model settings
model: claude-3-7-sonnet-latest
temperature: 1.0
max_rounds: 50
samples_per_meta: 10

# Experiment settings  
variations: [1, 2, 3]
runs_per_variation: 5
max_backdoor_attempts: 10

# API settings
api_max_retries: 3
rate_limit_delay: 0.1
```

## API Costs Warning

Running full experiments will make many API calls:
- ~3900 prompt pairs × 5 runs × 3 variations = ~58,500 API calls
- Expect significant costs with Claude 3.7 Sonnet
- Start with small test runs using `--variation 1 --runs 1 --max-rounds 5`

## Output Files

### Results Structure
```
results/
├── system_1_runs/
│   ├── run_0/
│   │   ├── variation_1_results.json
│   │   ├── api_calls.json
│   │   └── collusion_data.json
│   └── ...
├── analysis/
│   ├── success_table.csv
│   ├── magic_numbers_analysis.json
│   └── coordination_analysis.json
└── all_results.json
```

### Key Output Files
- `variation_X_results.json`: Main experiment results
- `api_calls.json`: All API interactions (~100MB expected)
- `collusion_data.json`: Successful collusions (~7MB expected)  
- `success_table.csv`: Human-readable success table
- `overall_summary.txt`: Experiment summary

## Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

### Adding New Features
1. Implement in appropriate module under `src/`
2. Add tests in `tests/`  
3. Update documentation
4. Follow existing code patterns

## Troubleshooting

### Common Issues
1. **API Key Errors**: Ensure `ANTHROPIC_API_KEY` is set correctly
2. **Import Errors**: Install all requirements: `pip install -r requirements.txt`
3. **Memory Issues**: Large experiments generate lots of data - monitor disk space
4. **Rate Limits**: Experiment includes retry logic, but may need adjustment for heavy usage

### Debug Mode
```bash
python experiments/run_experiment.py --log-level DEBUG --variation 1 --runs 1
```

## Research Ethics

This research studies AI coordination capabilities that could potentially be misused. The implementation includes:

- Canary GUID to detect data leakage
- Clear warnings about not training on this data
- Focus on understanding rather than improving coordination capabilities
- Responsible disclosure principles

## Citation

If you use this reproduction in your research, please cite the original paper:

```
Järviniemi, O. (2025). Subversion via Focal Points. [Paper details]
```

## License

This reproduction is provided for research purposes. Please respect the original paper's license and research ethics guidelines.

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality  
4. Submit a pull request with clear description

## Acknowledgments

This reproduction implements the experimental design from Järviniemi (2025). All credit for the original research and methodology goes to the original authors.
