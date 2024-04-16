import json, requests


class Llm:
    api_key: str | None = None
    
    
    def __init__(self, api_key):
        self.api_key = api_key
    
    
    def __prompt(self, prompt) -> str | None:
        responseText = ''
        success = False
        while not success:
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + self.api_key
            headers = {"Content-Type": "application/json"}
            data = {"contents": [{"parts": [{"text": prompt}]}]}
            response = requests.post(url, headers=headers, json=data)
            if response.status_code != 200:
                return None
            try:
                responseText = response.json()['candidates'][0]['content']['parts'][0]['text']
                success = True
            except:
                success = False
        return responseText
    
    
    def pickEmails(self, emails: list[str]):
        response = self.__prompt(f"Pick the best email or emails to send my resume to.\
            If there's no good email, then bad ones, like contact or support or any random email.\
            You cannot not pick an email. Your response contains at least one email.\
            Your response should be json-parseable and consist of array of emails like ['a@b.c', 'hr@example.com'].\
            Your response should contain only double quotes and be json parseable.\
            If they differ only by subdomain, pick the higher level one.\
            There might not be an appropriate email, in such case pick less appropriate ones on the principle of less evil.\
            Comments or any other symbols are allowed. You are not allowed to output anything except for the array.\
            The emails are: {emails}")
        pickedEmails = json.loads(response)
        return pickedEmails
    
    
    def writeCoverLetter(self, company_name, resume_text, site_text, email):
        response = '['
        while ('[' in response):
            response = self.__prompt(f'Write a proper concise cover letter for the company {company_name} I\'m cold emailing out of blue.\
                The length of the letter can be a few paragraphs at max.\
                Using my resume text: "{resume_text}".\
                And using text from the company website: "{site_text}".\
                Focus on how valuable I would be for the company.\
                Must be very aligned with companies values.\
                This is not a template, it\'s an actual email, so it cannot contain template stuff like [fill in something].\
                Must not contain field that need filling, this is the final text.\
                Do not retell my resume, instead write a good cover letter.\
                Do not over exaggerate my accomplishments.\
                You must paste the link to my portfolio website "https://ivang71.github.io/portfolio".\
                You can mention that I have attached my resume to the email.\
                The response should be properly formatted and each paragram should be surrounded by new lines.\
                Focus on benefit for them, not babble about my experience.\
                End with clear CTA to contact me.\
                I\'m sending to the email {email}, if it\'s not an appropriate email, insert apology at the beginning with request to forward to hr.\
                You\'re response must contain only the cover letter text with no additional comments.')
        return response

    
