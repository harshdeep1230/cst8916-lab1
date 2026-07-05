# CST8916 - Serverless (Lab 1)

A cloud-native, serverless application built with Python and deployed to Azure Functions using the Flex Consumption plan.
## Features
* **Text Analysis Engine (`/api/textanalyzer`):** An HTTP-triggered endpoint that accepts a `text` query parameter, runs calculations .

 ## https://harshdeep-func-lab1-a4f6ctb6e9bddgfk.canadacentral-01.azurewebsites.net/api/textanalyzer?text=%20demo%20video%20message%20here!

  
* **History Retrieval Engine (`/api/getanalysishistory`):** An HTTP-triggered endpoint that pulls previous analysis records directly from the database

 ## https://harshdeep-func-lab1-a4f6ctb6e9bddgfk.canadacentral-01.azurewebsites.net/api/getanalysishistory?limit=5
  
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



##https://youtu.be/HNPYsQ86APs
```


---

## Deployment & Verification Evidence

### 1. Successful Azure CLI Deployment
Proof of the compilation and green pipeline deployment from the VS Code terminal environment:
<img width="1918" height="856" alt="image" src="https://github.com/user-attachments/assets/f1fef1d2-9ab9-49a7-953e-99a0bc849855" />

### 2. Live Text Analyzer Response
Verification of the live HTTP execution returning data metrics and successfully writing state payloads directly into the Cosmos DB instance:


<img width="1918" height="721" alt="image" src="https://github.com/user-attachments/assets/1f83bb00-8ed0-4048-a376-7adb319ab839" />

### 3. Cosmos DB History Retrieval
The live history execution dynamically parsing out the latest database entries along with Cosmos internal document metadata (`_rid`, `_self`, `_etag`):

<img width="1918" height="972" alt="image" src="https://github.com/user-attachments/assets/b7294b06-d629-4276-92c9-ccb6f9acf995" />
