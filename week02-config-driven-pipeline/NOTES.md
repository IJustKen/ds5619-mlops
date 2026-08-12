# NOTES.md — Week 2: Config-Driven Data Pipelines

**Student ID used with `generate_for_student.py`:**
142301038


## What was hardcoded, and what would switching it have required?
<!-- What specifically was hardcoded in the original script, and what would
     have had to happen to change the threshold or switch formats before
     your refactor? -->
Input path, output path and also the high value threshold were hardcoded in the original script, 
which means we would have to manually edit the python file to change those values and then run the code again.

Also the code for ingesting the data assumes that it is going to be a .csv as it uses csv.DictReader(). 
This means if we ever change the data format to .json or something else this code will have to be changed manually again.
Thus even the data ingestion code is hardcoded, along with the paths and values being hardcoded as mentioned earlier.