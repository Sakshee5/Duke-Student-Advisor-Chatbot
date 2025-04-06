import requests
from dotenv import load_dotenv
import os
from urllib.parse import quote

load_dotenv()

DUKE_API_KEY = os.getenv("DUKE_API_KEY")
BASE_URL = "https://streamer.oit.duke.edu"


def get_courses(subject):
    """A tool to get all courses for a given subject"""
    
    encoded_subject = quote(subject)
    url = f"{BASE_URL}/curriculum/courses/subject/{encoded_subject}?access_token={DUKE_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": response.status_code, "message": response.text}

    try:
        courses_raw = response.json()['ssr_get_courses_resp']['course_search_result']['subjects']['subject']['course_summaries']['course_summary']
        summaries = [
            {
                "catalog_nbr": c.get("catalog_nbr", "").strip(),
                "title": c.get("course_title_long", "N/A"),
                "term": c.get("ssr_crse_typoff_cd_lov_descr", "N/A"),
                "crse_id": c.get("crse_id"),
                "crse_offer_nbr": c.get("crse_offer_nbr"),
            }
            for c in courses_raw
        ]
        return summaries
    except KeyError:
        return {"error": "No courses found or unexpected response structure."}


def get_course_details(crse_id, crse_offer_nbr):
    """A tool to get detailed course info for a specific course using its ID and offering number"""

    url = f"{BASE_URL}/curriculum/courses/crse_id/{crse_id}/crse_offer_nbr/{crse_offer_nbr}?access_token={DUKE_API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": response.status_code, "message": response.text}

    try:
        data = response.json()['ssr_get_course_offering_resp']['course_offering_result']['course_offering']
        course_info = {
            "title": data.get("course_title_long", "N/A"),
            "description": data.get("descrlong", "No description available."),
            "units": data.get("units_range", "N/A"),
            "term": data.get("ssr_crse_typoff_cd_lov_descr", "N/A"),
            "grading_basis": data.get("grading_basis_lov_descr", "N/A"),
            "career": data.get("acad_career_lov_descr", "N/A"),
            "school": data.get("acad_group_lov_descr", "N/A"),
            "department": data.get("acad_org_lov_descr", "N/A"),
            "consent": data.get("consent_lov_descr", "N/A"),
            "component": data.get("course_components", {}).get("course_component", {}).get("ssr_component_lov_descr", "N/A"),
            "scheduled": "*** This course has not been scheduled. ***" not in response.text
        }
        return course_info
    except KeyError:
        return {"error": "Unexpected structure in course detail response."}


def describe_course_by_title_or_code(subject, query):
    """
    Search for a course by catalog number or title and return detailed info.
    """
    course_list = get_courses(subject)
    if isinstance(course_list, dict) and "error" in course_list:
        return course_list

    # Search for matching course
    match = None
    for course in course_list:
        if query.strip().lower() in course['catalog_nbr'].lower() or query.strip().lower() in course['title'].lower():
            match = course
            break

    if not match:
        return {"error": f"No course found for '{query}' in subject '{subject}'."}

    return get_course_details(match['crse_id'], match['crse_offer_nbr'])



if __name__ == "__main__":
    print("Summary of AIPI Courses:\n")
    all_courses = get_courses("AIPI - AI for Product Innovation")
    for c in all_courses:
        print(f"{c['catalog_nbr']}: {c['title']} ({c['term']})")

    print("\nDetailed Info for AIPI 590:\n")
    details = describe_course_by_title_or_code("AIPI", "590")
    if "error" in details:
        print(details["error"])
    else:
        for key, value in details.items():
            print(f"{key.capitalize()}: {value}")
