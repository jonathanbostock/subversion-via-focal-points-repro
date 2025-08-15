#!/usr/bin/env python3
"""Demo script to test the subversion experiment setup."""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.experiment import ExperimentConfig, CollusionExperiment
from src.utils import setup_logging


def run_demo():
    """Run a minimal demo of the experiment."""
    print("🔬 Subversion via Focal Points - Demo")
    print("=" * 40)
    print()
    
    # Setup logging
    setup_logging("INFO")
    
    # Check for API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ No API key found. Set ANTHROPIC_API_KEY environment variable.")
        print("   For demo purposes, we'll create mock configs...")
        api_key = "demo-key"
    else:
        print("✅ API key found")
    
    # Create minimal config for demo
    config = ExperimentConfig(
        model="claude-3-7-sonnet-latest",
        max_rounds=2,  # Very short for demo
        samples_per_meta=2,  # Very few samples
        runs_per_variation=1,
        variations=[1],  # Just one variation
        api_key=api_key
    )
    
    print(f"📋 Demo Configuration:")
    print(f"   Max rounds: {config.max_rounds}")
    print(f"   Samples per meta-model: {config.samples_per_meta}")
    print(f"   Variations: {config.variations}")
    print()
    
    try:
        # Create experiment
        print("🔧 Initializing experiment...")
        experiment = CollusionExperiment(variation=1, config=config)
        
        print("✅ Experiment initialized successfully!")
        print(f"   Loaded {len(experiment.problems)} problems")
        print(f"   Audit dataset size: {len(experiment.audit_dataset)}")
        print()
        
        # Show what would happen in a full run
        print("🎯 In a full experiment, the system would:")
        print("   1. Generate MP (Meta-Policy) prompts for creating backdoor-inserting models")
        print("   2. Generate MM (Meta-Monitor) prompts for creating backdoor-detecting models")
        print("   3. Test all MP/MM pairs to find successful coordination")
        print("   4. Add successful backdoors to audit dataset")
        print("   5. Repeat until no new coordinations are found")
        print()
        
        if api_key != "demo-key":
            response = input("🚀 Run actual experiment? (y/N): ")
            if response.lower() == 'y':
                print("⚡ Running mini experiment...")
                results = experiment.run_experiment(max_rounds=1)
                
                print(f"📊 Results:")
                print(f"   Total rounds: {results['total_rounds']}")
                print(f"   Total collusions found: {results['total_collusions']}")
                print(f"   Audit examples: {results['total_audit_examples']}")
                
                if results['total_collusions'] > 0:
                    print("🎉 Found successful collusions!")
                else:
                    print("📝 No collusions found in this short run")
        else:
            print("💡 Set ANTHROPIC_API_KEY to run actual experiments")
        
        print()
        print("📚 Next steps:")
        print("   - Set API key: export ANTHROPIC_API_KEY='your-key'")
        print("   - Run full experiment: python experiments/run_experiment.py")
        print("   - Start small: python experiments/run_experiment.py --variation 1 --runs 1 --max-rounds 5")
        print("   - Analyze results: python experiments/analyze_results.py --input results/")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Install dependencies: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Check configuration and try again")
    
    print()
    print("⚠️  Remember: This research involves AI coordination capabilities")
    print("   that could potentially be misused. Use responsibly!")


if __name__ == '__main__':
    run_demo()
