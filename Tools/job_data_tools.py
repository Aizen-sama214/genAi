import json
import os
from pydantic import BaseModel, Field

# I have multiple files containing jobs data that I want to load into memory




class EmployerProfile(BaseModel):
    id: int
    company_name: str
    company_founded: int
    employee_count: int
    instahyre_note: str
    resource_uri: str
    profile_image_src: str
    company_tagline: str
    
class JobData(BaseModel):
      condidate_title: str = Field( None, description="Title of the job as seen by the candidate.")
      employer_profile_url: str
      title: str
      gender: int
      opportunity_url: str
      hiring_company_name: str
      locations: str = Field(None, description="Comma-separated list of locations for the job.")
      is_internship: bool
      keywords: list[str]
      resource_uri: str
      id: int
      accept_outstation: bool
      external_url: str | None = None

class Job(BaseModel):
    reviewed_at: str
    id: str
    is_active: bool
    employer: EmployerProfile
    job: JobData
       

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
    
    jobs = []
    for job_dict in job_data:
        job = Job(**job_dict)
        jobs.append(job)
    return jobs


def filter_jobs_by_location(jobs: list[Job], location: str) -> int:
    """Filter jobs by a specific location."""
    return len([job for job in jobs if location in job.get('job', {}).get('locations', "")])

