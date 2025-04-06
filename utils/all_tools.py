from typing import List, Dict
from tools.memDatabaseTool import search as mem_search
from tools.prattDatabaseTool import search as pratt_search
from tools.curriculumTool import get_courses, get_course_details, describe_course_by_title_or_code
from tools.eventsTool import get_events

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "mem_search",
            "description": "Search for information about the MEM (Master of Engineering Management) program at Duke University",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query about MEM program"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "default": 3
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "pratt_search",
            "description": "Search for information about Pratt School of Engineering programs at Duke University",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query about Pratt programs"
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "default": 3
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_courses",
            "description": "Get all courses for a given subject at Duke University",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "The subject code or name (e.g., 'AIPI', 'CS', 'ECE')"
                    }
                },
                "required": ["subject"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_course_details",
            "description": "Get detailed information about a specific course at Duke University",
            "parameters": {
                "type": "object",
                "properties": {
                    "crse_id": {
                        "type": "string",
                        "description": "The course ID"
                    },
                    "crse_offer_nbr": {
                        "type": "string",
                        "description": "The course offering number"
                    }
                },
                "required": ["crse_id", "crse_offer_nbr"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "describe_course_by_title_or_code",
            "description": "Search for a course by its title or code and get detailed information",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "The subject code or name"
                    },
                    "query": {
                        "type": "string",
                        "description": "The course code or title to search for"
                    }
                },
                "required": ["subject", "query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_events",
            "description": "Get events from the Duke University Events API",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to search for events"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

def get_tool_function(tool_name: str):
    """Get the actual function implementation for a tool name"""
    tool_functions = {
        "mem_search": mem_search,
        "pratt_search": pratt_search,
        "get_courses": get_courses,
        "get_course_details": get_course_details,
        "describe_course_by_title_or_code": describe_course_by_title_or_code,
        "get_events": get_events
    }
    return tool_functions.get(tool_name) 