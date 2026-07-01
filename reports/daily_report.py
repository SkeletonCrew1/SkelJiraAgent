from app import agent, discord_message_cutter, json_text_extractor, get_jira_data

file_daily_report = "reports/prompts/Instruction-daily-report.md"

with open(file_daily_report, "r") as file:
    daily_report = file.read()
response_data = get_jira_data()

json_out = json_text_extractor(response_data)


gemini_response = agent(json_out, daily_report)
print(gemini_response)
discord_message_cutter(gemini_response)
