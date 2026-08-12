# ds5619-mlops
MLOps Labs

## Week 2
All deliverables have been provided, go to week02-config-driven-pipeline directory and check.

Run the command "python src/pipeline.py --config config/pipeline.yaml" or even use any of the other config files to verify.

To change input path, output path or the threshold, change it in config/pipeline.yaml or create a new config .yaml and enter that path in the --config argument

Inside config folder there are 3 different configurations: 1 with a .csv file and 5000 threshold, 1 with a .json file and same threshold, and 1 with a .json file but 400 threshold.

Each output has been saved in data/v1 with appropriate names as report_csv.json, report_json.json, and report_json_modified_threshold.json

Code has been tested with the provided test also using "pytest -q"

Code has also been commented to clarify why certain steps were taken
