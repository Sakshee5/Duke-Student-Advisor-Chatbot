TOOLS_SCHEMA = [
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
            "description": "Search for a course by subject and course title or course number",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "The subject name like 'Artificial Intelligence' or 'AI'"
                    },
                    "course_title": {
                        "type": "string",
                        "description": "The course title to search for like 'Sourcing Data' or 'Supply Chain Management'",
                        "default": None

                    },
                    "course_number": {
                        "type": "string",
                        "description": "The course number to search for like '590' or '710'",
                        "default": None
                    }
                },
                "required": ["subject"]
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
    },

    {
        "type": "function",
        "function": {
            "name": "get_AIPI_details",
            "description": "This function / tool gets details about the Artificial Intelligence for Product Innovation Program also called AIPI use this for any queries regarding the program or for any information about professors if the progrgam is mentioned",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to search for information about the AIPI or the Artificial Intelligence for Product Innovation Program"
                    }
                },
                "required": ["query"]
            }
        }
    }
]