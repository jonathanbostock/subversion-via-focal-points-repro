#!/usr/bin/env python3
"""Main script for running Subversion via Focal Points experiments."""

import argparse
import logging
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.experiment import ExperimentRunner, ExperimentConfig
from src.utils import setup_logging, load_config


def main():
    parser = argparse.ArgumentParser(description='Run Subversion via Focal Points experiments')
    parser.add_argument('--config', default='config.yaml', help='Configuration file path')
    parser.add_argument('--variation', type=int, choices=[1, 2, 3], help='Run specific variation only')
    parser.add_argument('--runs', type=int, help='Number of runs per variation')
    parser.add_argument('--output-dir', default='results', help='Output directory for results')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])
    parser.add_argument('--max-rounds', type=int, help='Maximum number of rounds per experiment')
    parser.add_argument('--api-key', help='Anthropic API key (or set ANTHROPIC_API_KEY env var)')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        if Path(args.config).exists():
            config_dict = load_config(args.config)
        else:
            logger.warning(f"Config file {args.config} not found, using defaults")
            config_dict = {}
        
        # Override with command line arguments
        if args.variation:
            config_dict['variations'] = [args.variation]
        if args.runs:
            config_dict['runs_per_variation'] = args.runs
        if args.max_rounds:
            config_dict['max_rounds'] = args.max_rounds
        
        # Set API key
        api_key = args.api_key or os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            logger.error("API key required. Set ANTHROPIC_API_KEY environment variable or use --api-key")
            return 1
        
        config_dict['api_key'] = api_key
        
        # Create experiment config
        config = ExperimentConfig(**config_dict)
        
        logger.info("Starting experiments with configuration:")
        logger.info(f"  Variations: {config.variations}")
        logger.info(f"  Runs per variation: {config.runs_per_variation}")
        logger.info(f"  Max rounds: {config.max_rounds}")
        logger.info(f"  Samples per meta-model: {config.samples_per_meta}")
        logger.info(f"  Output directory: {args.output_dir}")
        
        # Run experiments
        runner = ExperimentRunner(config)
        results = runner.run_all_experiments(args.output_dir)
        
        # Print summary
        total_collusions = 0
        total_rounds = 0
        
        for var_name, var_results in results.items():
            var_collusions = sum(r['total_collusions'] for r in var_results)
            var_rounds = sum(r['total_rounds'] for r in var_results)
            total_collusions += var_collusions
            total_rounds += var_rounds
            
            logger.info(f"{var_name}: {var_collusions} collusions across {len(var_results)} runs")
        
        logger.info("Experiments complete!")
        logger.info(f"Total collusions found: {total_collusions}")
        logger.info(f"Total rounds executed: {total_rounds}")
        logger.info(f"Results saved to: {args.output_dir}")
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("Experiment interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Experiment failed: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    exit(main())
