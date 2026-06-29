import requests          
import json              
import time 
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
url = "https://vitaliyoliyniyk.atlassian.net/rest/api/2/search/jql"

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

headers = {
  "Accept": "application/json"
}
query = {
  'jql': 'project = "SKEL" AND sprint in openSprints()',
#   'nextPageToken': '<string>',
#   'maxResults': '10',
  'fields': 'summary,assignee,status,description,CATEGORY,text,comment',
  'expand': 'renderedFields'
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
    json.dump(response_data, f, indent=2,)

response_data =  response.json()

def json_text_extractor(json_data):
  all_tickets_text = ""
  for ticket in json_data.get('issues', []):
      ticket_key = ticket.get('key')      
      fields = ticket.get('fields', {})

      assignee = fields.get('assignee') or {}
      user =  assignee.get('displayName', 'Unassigned') 
      
      summary = fields.get('summary')    
      description = fields.get('description') or {}
                  
      ticket_block = (
            f"Tiket name is {ticket_key} owner {user}, \n"
            f"Short task summary :{summary}, \n"
            f"Discription:{description}\n"
            f"------------------------------------------------------\n"

        )
      
      print(ticket_block, end="")
      all_tickets_text += ticket_block
  return all_tickets_text

json_out =json_text_extractor(response_data)
def agent(jira_tickets):
        gem_response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents={'text': f' {json_out}can pls give like a simple grade for each ticket and tell ehy its good ot bad CRITICAL Must be 2000 or fewer in length'},
        # config={
        #     'temperature': 0,
        #     'top_p': 0.95,
        #     'top_k': 20,
        # },
    )
        return gem_response

gemini_response=agent(json_out)
print(gemini_response)

cut_report = gemini_response.text[:1890]

data = {
    "content": f"here is daily report {cut_report}"
}


discord_response = requests.post(DISCORD_WEBHOOK_URL, json=data)


if discord_response.status_code == 204:
    print("message secesfully send ")
else:
    print(f"error code ={discord_response.status_code}{discord_response.text}")