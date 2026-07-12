# Jira AI Agent

## This repository automates status reporting. It pulls data from Jira, uses AI to write a summary (weekly and daily), and posts the report to Discord.

## How it Works
The entire process runs automatically via GitHub Actions.

**Fetch:**: A scheduled job triggers a script that pulls recent issues and sprint progress via the Jira API.
**Process**: The raw JSON is parsed by a Python script to grab only the necessary details, which the AI model then analize.
**Notify**: The finalized report is sent directly to our Discord server using a webhook.

## Schedule
**Daily Report:** Runs every day to summarize daily progress.
**Weekly Report:** Runs every Tuesday to provide a weekly digest.
