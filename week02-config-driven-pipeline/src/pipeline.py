"""
The "after" version — YOUR file to complete.

Fill in the three functions marked with # TODO. Everything else (CLI wiring,
imports) is already done for you. Do not hardcode any path, format string, or
threshold value anywhere in this file — if you find yourself typing a literal
number or file path outside of a default/example, it belongs in the config
file instead.

Run with:
    python src/pipeline.py --config config/pipeline.yaml
"""
import argparse
import csv
import json

import yaml

REQUIRED_KEYS = ["input_path", "input_format", "high_value_threshold", "output_path"]


def load_config(path):
    """Load a YAML config file and validate required keys are present.

    Must raise ValueError naming the specific missing key if REQUIRED_KEYS
    are not all present. Do not let this fail with a bare KeyError later.
    """
    try:
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
    except Exception as e:
        # file not found or invalid file or something else raise error
        raise ValueError(f"Error loading file {path}: {e}")
    
    if data is None:
        # raise error in case the YAML file is empty
        raise ValueError("Config File Empty")
    
    if not isinstance(data, dict):
        raise ValueError("Config File Format Wrong")
    
    for key in REQUIRED_KEYS:
        if key not in data:
            # raising key not found error here itself
            raise ValueError(f"KEY NOT FOUND: {key}")
        
    return data


def load_transactions(path, fmt):
    """Load transactions from `path`, using `fmt` ("csv" or "json") to decide
    how to parse it — not by sniffing the file extension.

    Must return a list of dicts. Every dict must have at least "amount"
    (str or float) and "is_fraud" (str "True"/"False" or bool).
    Raise ValueError for any fmt other than "csv" or "json".
    """
    feature_requirements = ["amount", "is_fraud"]   # I am only creating these since the question mentions to check against these
    valid_formats = {"csv", "json"}

    if fmt not in valid_formats:
        # invalid format found raise an error
        raise ValueError(f"Invalid Format: {fmt}")
    
    try:
        if fmt == "csv":
            with open(path, 'r') as f:
                data = list(csv.DictReader(f))
            
        elif fmt == "json":
            with open(path, 'r') as f:
                 data = json.load(f)

    except Exception as e:
        # file not found or invalid file or something else raise error
        raise ValueError(f"Error loading file at {path}: {e}")
    
    if not isinstance(data, list):
        # just to check if the data is in the form of a list
        raise ValueError(f"Data format not correct")

    for i in range(len(data)):

        record = data[i]

        if not isinstance(record, dict):
            # each record must be a dictionary, if not, raise error
            raise ValueError(f"Record {i+1} is not in valid format")
        
        for requirement in feature_requirements:
            # raising error if the required features are not present in the record
            if requirement not in record:
                raise ValueError(f"Feature Missing: {requirement} in record {i+1}")
    
    return data


def run_pipeline(config):
    """Load data per `config`, compute the same summary fields as
    pipeline_hardcoded.py (n_transactions, total_amount, fraud_rate,
    n_high_value, high_value_threshold), and write them as JSON to
    config["output_path"]. Return the report dict as well.
    """
    # TODO: implement
    raise NotImplementedError("run_pipeline is not implemented yet")


def main():
    parser = argparse.ArgumentParser(description="Config-driven fraud transaction summary pipeline")
    parser.add_argument("--config", required=True, help="Path to a YAML config file")
    args = parser.parse_args()

    config = load_config(args.config)
    report = run_pipeline(config)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
