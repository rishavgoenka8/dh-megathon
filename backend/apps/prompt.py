import requests
import json
from .metric import metric_system
from .profile_parser import parse_json
import os
openai_api_key = os.environ.get('OPENAI_API_KEY') #Put this in env

def _openAI_skills(data):

    profile = parse_json(data)
    prompt = f""" I'll give you a job profile of a person and I want you to classify the person's profile in the domain of sales or Tech. After that, use {metric_system} to judge the profile of the person and give me total tech score only. If a field is not available then consider it as 0. The profile data is: {profile}. Also suggest some interview questions based on the person's past projects for hiring purposes.

    Example output
    Domain: Technology
    Score: 52
    Summary (max 40 words): They have a strong academic background in computer science.
    Interview Questions: 
        1. 
        2. 
        3.
        4.
        5.
    """
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # This will raise an exception for HTTP errors
        completion = response.json()
        outp = completion['choices'][0]['message']['content']
        print(outp)
    except Exception as e:
        print(e)
        print("Generating report without summary as openAI failed to respond.")
        outp = ""
    return outp
    

def _openAI_culture(data):
    posts = data['posts']
    prompt = f""" 
    We want to judge a person's behaviour and nature based on his/her linkedin posts. I'll give you all of the posts made by the applicant and I want you to return the behavioural aspects of that person. You can give output using Myers-Briggs Type Indicator Test. Keep the result very concise upto 3-4 lines. The posts are as follows: {posts}. 
    Format the output as bullet points.
    """ 
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # This will raise an exception for HTTP errors
        completion = response.json()
        outp = completion['choices'][0]['message']['content']
        print(outp)
    except Exception as e:
        print(e)
        print("Generating report without summary as openAI failed to respond.")
        outp = ""
    return outp
    
    