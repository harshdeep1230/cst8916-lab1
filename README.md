# CST8916 - Serverless (Lab 1)

A cloud-native, serverless application built with Python and deployed to Azure Functions using the Flex Consumption plan.
## Features
* **Text Analysis Engine (`/api/textanalyzer`):** An HTTP-triggered endpoint that accepts a `text` query parameter, runs calculations .
* **History Retrieval Engine (`/api/getanalysishistory`):** An HTTP-triggered endpoint that pulls previous analysis records directly from the database
## Technology Stack
* **Language:** Python 3.10+
* **Framework:** Azure Functions 
* **Hosting Plan:** Azure Functions Flex Consumption
* **Database:** Azure Cosmos DB (NoSQL API)

## Project Structure
```text
.
├── .vscode/               # VS Code configuration settings
├── .gitignore             # Excludes local environments and local.settings.json
├── function_app.py        # Main application file containing HTTP function triggers
├── host.json              # Global configuration options for the function app
└── requirements.txt       # Python dependencies (azure-functions, azure-cosmos)

## Demo Video Walkthrough



https://youtu.be/HNPYsQ86APs
