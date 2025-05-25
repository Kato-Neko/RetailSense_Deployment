"""
job_manager.py
Handles job queueing, status, and database management for the backend using Supabase.
"""

import os
import logging
from supabase import create_client, Client

logger = logging.getLogger(__name__)

# Initialize Supabase client
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def insert_job(*args, **kwargs):
    logger.debug("Inserting job into Supabase")
    response = supabase.table("jobs").insert(kwargs).execute()
    if response.error:
        logger.error(f"Error inserting job: {response.error}")
    return response

def get_job(job_id):
    logger.debug(f"Fetching job {job_id} from Supabase")
    response = supabase.table("jobs").select("*").eq("job_id", job_id).single().execute()
    if response.error:
        logger.error(f"Error fetching job: {response.error}")
    return response.data

def update_job(job_id, update_data):
    logger.debug(f"Updating job {job_id} in Supabase")
    response = supabase.table("jobs").update(update_data).eq("job_id", job_id).execute()
    if response.error:
        logger.error(f"Error updating job: {response.error}")
    return response

def delete_job(job_id):
    logger.debug(f"Deleting job {job_id} from Supabase")
    response = supabase.table("jobs").delete().eq("job_id", job_id).execute()
    if response.error:
        logger.error(f"Error deleting job: {response.error}")
    return response

def get_jobs_for_user(user):
    logger.debug(f"Fetching jobs for user {user} from Supabase")
    response = supabase.table("jobs").select("*").eq("user", user).order("created_at", desc=True).execute()
    if response.error:
        logger.error(f"Error fetching jobs for user: {response.error}")
    return response.data

def upload_to_supabase(job_id, local_file_path, file_type):
    """
    Uploads a file to Supabase Storage under the given job_id folder.
    file_type: 'jpg' or 'json'
    """
    bucket_name = "projectresults"
    file_name = os.path.basename(local_file_path)
    storage_path = f"{job_id}/{file_name}"

    with open(local_file_path, "rb") as f:
        data = f.read()
        response = supabase.storage.from_(bucket_name).upload(
            storage_path, data, {"content-type": "image/jpeg" if file_type == "jpg" else "application/json"}
        )
        logger.info(f"Upload response: {response}")
        return response

def get_signed_url(job_id, file_name, expires_in=3600):
    bucket_name = "projectresults"
    storage_path = f"{job_id}/{file_name}"
    response = supabase.storage.from_(bucket_name).create_signed_url(storage_path, expires_in)
    logger.info(f"Signed URL response: {response}")
    return response 