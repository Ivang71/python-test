import json, requests


class Llm:
    api_key: str | None = None
    
    
    def __init__(self, api_key):
        self.api_key = api_key
    
    
    def __prompt(self, prompt):
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + self.api_key
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            return None
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    
    
    def pickEmails(self, emails: list[str]):
        response = self.__prompt(f"Pick the best email or emails to send my resume to.\
            If there's no good email, then bad ones are good enough, like contact or support email.\
            You're response should be json-parseable and consist of array of emails like ['a@b.c', 'hr@example.com'].\
            If they differ only by subdomain, pick the higher level one.\
            There might not be an appropriate email, in such case pick less appropriate ones on the principle of less evil.\
            Comments or any other symbols are allowed. You are not allowed to output anything except for the array.\
            The emails are: {emails}")
        pickedEmails = json.loads(response)
        return pickedEmails
    
    
    def writeCoverLetter(self, company_name, resume_text, site_text, email):
        return self.__prompt(f'Write a proper concise cover letter for the company {company_name} I\'m cold emailing out of blue.\
            Using my resume text: "{resume_text}".\
            And using text from the company website: "{site_text}".\
            Focus on how valuable I would be for the company.\
            Do not retell my resume, instead write a good cover letter.\
            Do not over exaggerate my accomplishments.\
            You must paste the link to my portfolio website "https://ivang71.github.io/portfolio".\
            End with clear CTA to contact me.\
            I\'m sending to the email {email}.\
            You\'re response must contain only the cover letter text with no additional comments.')

    
