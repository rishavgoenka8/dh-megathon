import json

def parse_json(data):
    # Extract the fields
    name = data['name']
    headline = data['headline']
    about = data['about']
    skills = [skill[0] for skill in data['skills']]
    education = data['education']
    experience = data['experience']

    projects = []
    for project_list in data['projects']:
        for project in project_list:
            projects.append(project)

    # Create a dictionary to hold the extracted information
    extracted_info = {
        'name': name,
        'headline': headline,
        'about': about,
        'skills': skills,
        'education': education,
        'experience': experience,
        'projects': projects
    }

    # Convert the extracted information to JSON format
    extracted_json = json.dumps(extracted_info, indent=4)

    return extracted_json
