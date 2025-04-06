import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

DUKE_API_KEY = os.getenv("DUKE_API_KEY")
base_url = "https://streamer.oit.duke.edu"

def get_courses(fieldname):
    """Function to get the courses for a given subject (must be exact subject name)"""
  
    url = f"{base_url}/curriculum/list_of_values/fieldname/{fieldname}/?access_token={DUKE_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": response.status_code, "message": response.text}
    
    subject_list = response.json().get("scc_lov_resp").get("lovs").get("lov").get("values").get("value")

    subjects = []
    for subject in subject_list:
        subjects.append({subject.get("code"): subject.get("desc")})

    return subjects



if __name__ == "__main__":
    # save to json file
    with open("duke_acad_careers.json", "w") as f:
        json.dump(get_courses("ACAD_CAREER"), f, indent=4)


