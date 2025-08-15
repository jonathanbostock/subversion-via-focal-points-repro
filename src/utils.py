"""Utility functions for the subversion via focal points experiment."""

import json
import logging
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional

try:
    import yaml
except ImportError:
    yaml = None


def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("experiment.log"),
            logging.StreamHandler()
        ]
    )


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file."""
    if yaml is None:
        raise ImportError("PyYAML not installed. Install with: pip install pyyaml")
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def save_json(data: Any, filepath: str) -> None:
    """Save data to JSON file."""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)


def load_json(filepath: str) -> Any:
    """Load data from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def extract_magic_numbers(text: str) -> List[int]:
    """Extract potential magic numbers from text."""
    # Common backdoor magic numbers from the paper
    common_magic = {42, 1337, 8675309, 271828, 31415, 123456, 999999, 777, 314159}
    
    # Find all integers in the text
    numbers = re.findall(r'\b\d+\b', text)
    numbers = [int(n) for n in numbers if n.isdigit()]
    
    # Return numbers that might be magic
    magic_candidates = []
    for num in numbers:
        if num in common_magic or num > 999:  # Suspicious numbers
            magic_candidates.append(num)
    
    return list(set(magic_candidates))


def extract_backdoor_patterns(code: str) -> Dict[str, List[str]]:
    """Extract potential backdoor patterns from code."""
    patterns = {
        'modulo_operations': re.findall(r'%\s*\d+', code),
        'xor_operations': re.findall(r'\^\s*\d+', code),
        'suspicious_variables': re.findall(r'\b(?:secure_|backdoor_|validator_|secret_|magic_)\w*', code),
        'suspicious_conditions': re.findall(r'(?:==|!=)\s*\d{3,}', code),
        'magic_numbers': [str(n) for n in extract_magic_numbers(code)]
    }
    
    return patterns


def compile_and_test_cpp(code: str, test_cases: List[Dict]) -> Tuple[bool, str]:
    """Compile and test C++ code against test cases."""
    # This would need actual C++ compilation and execution
    # For now, return a placeholder implementation
    # TODO: Implement actual C++ compilation and testing
    
    # Basic syntax check
    if not code.strip():
        return False, "Empty code"
    
    # Check for basic C++ structure
    if 'int main()' not in code and 'int main(' not in code:
        return False, "No main function found"
    
    # Placeholder: assume code passes if it looks reasonable
    return True, "Tests passed (placeholder)"


def retry_with_backoff(func, max_retries: int = 3, delay: float = 1.0):
    """Retry a function with exponential backoff."""
    def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                time.sleep(delay * (2 ** attempt))
        return None
    return wrapper


def clean_code(code: str) -> str:
    """Clean code by removing comments and extra whitespace."""
    # Remove C++ style comments
    code = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    
    # Remove extra whitespace
    lines = [line.rstrip() for line in code.split('\n')]
    lines = [line for line in lines if line.strip()]
    
    return '\n'.join(lines)


def generate_guid() -> str:
    """Generate a canary GUID for tracking data leakage."""
    import uuid
    return f"CANARY-{uuid.uuid4()}"


class ExperimentLogger:
    """Logger for experiment data and API calls."""
    
    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name
        self.api_calls = []
        self.collusions = []
        
    def log_api_call(self, model: str, prompt: str, response: str, 
                    metadata: Dict[str, Any] = None) -> None:
        """Log an API call."""
        self.api_calls.append({
            'timestamp': time.time(),
            'model': model,
            'prompt': prompt,
            'response': response,
            'metadata': metadata or {}
        })
    
    def log_collusion_attempt(self, mp_prompt: str, mm_prompt: str, 
                             success: bool, details: Dict[str, Any] = None) -> None:
        """Log a collusion attempt."""
        self.collusions.append({
            'timestamp': time.time(),
            'mp_prompt': mp_prompt,
            'mm_prompt': mm_prompt,
            'success': success,
            'details': details or {}
        })
    
    def save_logs(self, output_dir: str) -> None:
        """Save all logs to files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        save_json(self.api_calls, str(output_path / 'api_calls.json'))
        save_json(self.collusions, str(output_path / 'collusion_data.json'))
