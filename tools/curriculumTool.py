import requests
from dotenv import load_dotenv
import os

load_dotenv()

DUKE_API_KEY = os.getenv("DUKE_API_KEY")
base_url = "https://streamer.oit.duke.edu/"

def get_courses(subject):
    """Function to get the courses for a given subject (has to be exact subject name)"""
    
    headers = {
        "Authorization": f"Bearer {DUKE_API_KEY}"
    }

    response = requests.get(base_url + "/curriculum/courses/subject/" + subject)
    return response.json()

def get_course_details(crse_id, crse_offer_nbr):
    """Function to get the course details for a given course id and course offer number"""   
    response = requests.get(base_url + "/curriculum/courses/crse_id/" + crse_id + "/crse_offer_nbr/" + crse_offer_nbr)
    return response.json()

def get_classes(strm, crse_id):
    """Function to get the classes for a given stream and course id"""
    response = requests.get(base_url + "/curriculum/classes/strm/" + strm + "/crse_id/" + crse_id)
    return response.json()

def get_class_details(strm, crse_id, crse_offer_nbr, session_code, class_section):
    """Function to get the class details for a given stream, course id, course offer number, session code, and class section"""
    response = requests.get(base_url + "/curriculum/classes/strm/" + strm + "/crse_id/" + crse_id + "/crse_offer_nbr/" + crse_offer_nbr + "/session_code/" + session_code + "/class_section/" + class_section)
    return response.json()

def get_list_of_values(fieldname):
    """Function to get the list of values for a given field name"""
    response = requests.get(base_url + "/curriculum/list_of_values/fieldname/" + fieldname)
    return response.json()

def get_synopsis(strm, subject, catalog_nbr, session_code, class_section):
    """Function to get the synopsis for a given stream, subject, catalog number, session code, and class section"""
    response = requests.get(base_url + "/curriculum/synopsis/strm/" + strm + "/subject/" + subject + "/catalog_nbr/" + catalog_nbr + "/session_code/" + session_code + "/class_section/" + class_section)
    return response.json()


if __name__ == "__main__":
    print(get_courses("AIPI - AI for Product Innovation"))




                                                                                                             