import requests          
import json              
from requests.auth import HTTPBasicAuth 
from google import genai 
import os
from dotenv import load_dotenv

load_dotenv()

JIRA_DOMAIN = os.getenv('JIRA_DOMAIN')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

client = genai.Client(api_key=GEMINI_API_KEY)
url = "https://vitaliyoliyniyk.atlassian.net/rest/api/3/search/jql"

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

headers = {
  "Accept": "application/json"
}
query = {
  'jql': 'project = "SKEL" AND sprint in openSprints()',
#   'nextPageToken': '<string>',
#   'maxResults': '10',
  'fields': 'summary,assignee,status,description,CATEGORY,text,comment',
#   'expand': '<string>',
  # 'reconcileIssues': '{reconcileIssues}'
}

response = requests.request(
   "GET",
   url,
   headers=headers,
   params=query,
   auth=auth
)

response_data =  response.json()


with open('data.json', 'w') as f:
    json.dump(response_data, f, indent=4,)

response_data =  response.json()

def json_text_extractor(json_data):

  for ticket in json_data.get('issues', []):
      ticket_key = ticket.get('key')      
      fields = ticket.get('fields', {})
      
      summary = fields.get('summary')    
      raw_description = fields.get('description') or {}
      clean_description = ""
      
      for block in raw_description.get('content', []):
          for item in block.get('content', []):
              if item.get('type') == 'text':
                  clean_description += item.get('text', '') + " "
                  
      print(f"Tiket name is {ticket_key}, \n short task summary :{summary}, \n Discription:{clean_description}")
      print("-----------------------------------------")


json_out = json_text_extractor(response_data)

# upload_file = genai.client.file.upload(file=data.txt)

# with open('data.txt', 'w') as f:
#     f.write(json_out)


# uploaded_file = client.files.upload(file='data.txt')

# gem_response = client.models.generate_content(
#     model='gemini-2.5-flash',
#     contents={'text': f' {json_out}can pls give like a simple grade for each ticket and tell ehy its good ot bad not extra text'},
#     # config={
#     #     'temperature': 0,
#     #     'top_p': 0.95,
#     #     'top_k': 20,
#     # },
# )

# print(gem_response)
