import json
import os

# I have multiple files containing jobs data that I want to load into memory

def load_job_data_from_file(file_path: str) -> dict:
    """Load job data from a JSON file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")
    
    with open(file_path, 'r') as file:
        data = json.load(file).get("objects",[])
    
    return data

def load_job_data() -> list:
    """Load job data from multiple files and combine them into a single list."""
    job_data = []
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Assuming job data files are in a 'data' subdirectory
    data_dir = os.path.join(root_dir, 'Knowledge/data')
    
    for file_name in os.listdir(data_dir):
        if file_name.endswith('.json') and "jobsOverviewData" in file_name:
            file_path = os.path.join(data_dir, file_name)
            job_data.extend(load_job_data_from_file(file_path))
    
    return job_data


def filter_jobs_by_location(jobs: list, location: str) -> int:
    """Filter jobs by a specific location."""
    return len([job for job in jobs if location in job.get('job', {}).get('locations', "")])

