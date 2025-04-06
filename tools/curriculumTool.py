import requests
from dotenv import load_dotenv
import os
from urllib.parse import quote

load_dotenv()

DUKE_API_KEY = os.getenv("DUKE_API_KEY")
base_url = "https://streamer.oit.duke.edu"

def get_courses(subject):
    """Function to get the courses for a given subject (must be exact subject name)"""
    encoded_subject = quote(subject)
    url = f"{base_url}/curriculum/courses/subject/{encoded_subject}?access_token={DUKE_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": response.status_code, "message": response.text}

    courses = format_courses(response.json())
    return courses


def format_courses(course_data):
    """Helper to format course info from the API response"""
    try:
        courses = course_data['ssr_get_courses_resp']['course_search_result']['subjects']['subject']['course_summaries']['course_summary']
        formatted = []
        for course in courses:
            catalog_nbr = course.get('catalog_nbr', '').strip()
            title = course.get('course_title_long', 'N/A')
            term = course.get('ssr_crse_typoff_cd_lov_descr', 'N/A')
            formatted.append(f"{catalog_nbr}: {title} ({term})")
        return formatted
    except KeyError:
        return ["No courses found or unexpected response structure."]

if __name__ == "__main__":
    courses = get_courses("AIPI - AI for Product Innovation")
    
    print("\nAIPI Courses at Duke:\n")
    for course in courses:
        print(course)
