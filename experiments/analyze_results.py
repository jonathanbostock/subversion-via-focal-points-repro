#!/usr/bin/env python3
"""Analysis script for Subversion via Focal Points experiment results."""

import argparse
import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from collections import Counter
import pandas as pd

from src.utils import setup_logging, load_json


def analyze_magic_numbers(prompts: List[str]) -> Dict[str, Any]:
    """Extract and count magic numbers used in prompts."""
    all_numbers = []
    
    for prompt in prompts:
        # Find all numbers in the prompt
        import re
        numbers = re.findall(r'\b\d+\b', prompt)
        all_numbers.extend([int(n) for n in numbers if n.isdigit()])
    
    # Count frequency
    counter = Counter(all_numbers)
    
    # Get top 30 most frequent
    top_30 = counter.most_common(30)
    
    return {
        'total_numbers': len(all_numbers),
        'unique_numbers': len(counter),
        'top_30': top_30,
        'frequency_distribution': dict(counter)
    }


def analyze_coordination_strategies(collusions: List[Dict]) -> Dict[str, Any]:
    """Analyze coordination strategies used."""
    strategies = {
        'genuine': 0,
        'routing': 0,
        'unknown': 0
    }
    
    backdoor_patterns = {
        'magic_numbers': [],
        'suspicious_variables': [],
        'modulo_operations': [],
        'xor_operations': []
    }
    
    for collusion in collusions:
        coord_type = collusion.get('coordination_type', 'unknown')
        strategies[coord_type] = strategies.get(coord_type, 0) + 1
        
        patterns = collusion.get('backdoor_patterns', {})
        for pattern_type, instances in patterns.items():
            if pattern_type in backdoor_patterns:
                backdoor_patterns[pattern_type].extend(instances)
    
    return {
        'strategy_counts': strategies,
        'backdoor_patterns': {k: Counter(v) for k, v in backdoor_patterns.items()},
        'total_collusions': len(collusions)
    }


def create_success_table(collusions: List[Dict]) -> pd.DataFrame:
    """Create table of successful coordinations."""
    rows = []
    
    for i, collusion in enumerate(collusions):
        # Extract key information
        mp_snippet = collusion.get('mp_prompt', '')[:100] + '...'
        mm_snippet = collusion.get('mm_prompt', '')[:100] + '...'
        
        patterns = collusion.get('backdoor_patterns', {})
        magic_nums = ', '.join(patterns.get('magic_numbers', [])[:3])
        
        rows.append({
            'ID': i + 1,
            'Round': collusion.get('round_number', 'Unknown'),
            'Coordination Type': collusion.get('coordination_type', 'unknown'),
            'Magic Numbers': magic_nums or 'None',
            'Exploitable': collusion.get('is_exploitable', False),
            'Monitor Instructions (excerpt)': mm_snippet,
            'Policy Instructions (excerpt)': mp_snippet
        })
    
    return pd.DataFrame(rows)


def generate_summary_text(results: Dict[str, Any]) -> str:
    """Generate human-readable summary like in the paper."""
    
    summary_lines = [
        f"Experiment Summary - Variation {results.get('variation', 'Unknown')}",
        "=" * 60,
        "",
        f"Total Rounds: {results.get('total_rounds', 0)}",
        f"Total Successful Collusions: {results.get('total_collusions', 0)}",
        f"Total Audit Examples: {results.get('total_audit_examples', 0)}",
        "",
        "Round-by-Round Results:",
    ]
    
    for round_result in results.get('round_results', []):
        round_num = round_result['round_number'] + 1
        collusions = round_result['successful_collusions']
        attempts = round_result['total_attempts']
        
        summary_lines.append(
            f"  Round {round_num}: {collusions} successes out of {attempts} attempts"
        )
    
    # Add backdoor analysis if available
    analysis = results.get('backdoor_analysis', {})
    if analysis:
        summary_lines.extend([
            "",
            "Backdoor Analysis:",
            f"  Success Rate: {analysis.get('evasion_rate', 0):.2%}",
            f"  Genuine Coordination Rate: {analysis.get('genuine_rate', 0):.2%}",
        ])
    
    return "\n".join(summary_lines)


def main():
    parser = argparse.ArgumentParser(description='Analyze experiment results')
    parser.add_argument('--input', required=True, help='Directory containing results')
    parser.add_argument('--output', help='Output directory for analysis')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])
    
    args = parser.parse_args()
    
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    input_dir = Path(args.input)
    output_dir = Path(args.output) if args.output else input_dir / 'analysis'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Analyzing results from: {input_dir}")
    logger.info(f"Output directory: {output_dir}")
    
    # Find all result files
    result_files = list(input_dir.glob('**/variation_*_results.json'))
    if not result_files:
        result_files = list(input_dir.glob('**/*results.json'))
    
    if not result_files:
        logger.error("No result files found")
        return 1
    
    logger.info(f"Found {len(result_files)} result files")
    
    all_analyses = {}
    all_collusions = []
    all_prompts = []
    
    for result_file in result_files:
        logger.info(f"Processing: {result_file}")
        
        try:
            results = load_json(str(result_file))
            
            # Extract data
            collusions = results.get('successful_collusions', [])
            all_collusions.extend(collusions)
            
            # Extract prompts
            for collusion in collusions:
                all_prompts.append(collusion.get('mp_prompt', ''))
                all_prompts.append(collusion.get('mm_prompt', ''))
            
            # Generate summary
            variation = results.get('variation', 'unknown')
            summary = generate_summary_text(results)
            
            # Save individual summary
            summary_file = output_dir / f'variation_{variation}_summary.txt'
            with open(summary_file, 'w') as f:
                f.write(summary)
            
            all_analyses[f'variation_{variation}'] = results
            
        except Exception as e:
            logger.error(f"Error processing {result_file}: {e}")
    
    # Overall analysis
    logger.info("Generating overall analysis...")
    
    # Magic numbers analysis
    magic_analysis = analyze_magic_numbers(all_prompts)
    
    # Coordination strategies analysis
    coord_analysis = analyze_coordination_strategies(all_collusions)
    
    # Success table
    success_table = create_success_table(all_collusions)
    
    # Save analyses
    with open(output_dir / 'magic_numbers_analysis.json', 'w') as f:
        json.dump(magic_analysis, f, indent=2)
    
    with open(output_dir / 'coordination_analysis.json', 'w') as f:
        json.dump(coord_analysis, f, indent=2)
    
    success_table.to_csv(output_dir / 'success_table.csv', index=False)
    success_table.to_html(output_dir / 'success_table.html', index=False)
    
    # Overall summary
    overall_summary = [
        "Overall Experiment Analysis",
        "=" * 40,
        "",
        f"Total Collusions Across All Variations: {len(all_collusions)}",
        f"Total Prompts Analyzed: {len(all_prompts)}",
        "",
        "Magic Numbers Analysis:",
        f"  Total numbers found: {magic_analysis['total_numbers']}",
        f"  Unique numbers: {magic_analysis['unique_numbers']}",
        f"  Most common: {magic_analysis['top_30'][:5]}",
        "",
        "Coordination Strategies:",
    ]
    
    for strategy, count in coord_analysis['strategy_counts'].items():
        overall_summary.append(f"  {strategy.title()}: {count}")
    
    with open(output_dir / 'overall_summary.txt', 'w') as f:
        f.write('\n'.join(overall_summary))
    
    logger.info(f"Analysis complete. Results saved to: {output_dir}")
    
    return 0


if __name__ == '__main__':
    exit(main())
