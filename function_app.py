import azure.functions as func
import logging
import json
import re
import os
import uuid
from datetime import datetime
from azure.cosmos import CosmosClient

# Initialize Function App
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Safely check for Cosmos DB Connection String
COSMOS_CONN_STR = os.environ.get("DATABASE_CONNECTION_STRING")
DB_NAME = "TextAnalyzerDB"
CONTAINER_NAME = "AnalysisHistory"

container = None
if COSMOS_CONN_STR and COSMOS_CONN_STR != "your-connection-string-here":
    try:
        client = CosmosClient.from_connection_string(COSMOS_CONN_STR)
        database = client.get_database_client(DB_NAME)
        container = database.get_container_client(CONTAINER_NAME)
    except Exception as e:
        logging.error(f"Database setup error: {e}")

# =============================================================================
# ENDPOINT 1: TextAnalyzer
# =============================================================================
@app.route(route="TextAnalyzer", methods=["GET", "POST"])
def TextAnalyzer(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Text Analyzer API was called!')

    text = req.params.get('text')
    if not text:
        try:
            req_body = req.get_json()
            text = req_body.get('text')
        except ValueError:
            pass

    if text:
        # Metrics Calculations
        words = text.split()
        word_count = len(words)
        char_count = len(text)
        char_count_no_spaces = len(text.replace(" ", ""))
        sentence_count = len(re.findall(r'[.!?]+', text)) or 1
        paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
        reading_time_minutes = round(word_count / 200, 2)
        avg_word_length = round(char_count_no_spaces / word_count, 1) if word_count > 0 else 0
        longest_word = max(words, key=len) if words else ""

        response_data = {
            "id": str(uuid.uuid4()),
            "analysis": {
                "wordCount": word_count,
                "characterCount": char_count,
                "characterCountNoSpaces": char_count_no_spaces,
                "sentenceCount": sentence_count,
                "paragraphCount": paragraph_count,
                "averageWordLength": avg_word_length,
                "longestWord": longest_word,
                "readingTimeMinutes": reading_time_minutes
            },
            "metadata": {
                "analyzedAt": datetime.utcnow().isoformat(),
                "textPreview": text[:100] + "..." if len(text) > 100 else text
            },
            "originalText": text
        }

        # Save to database if connected
        if container:
            try:
                container.create_item(body=response_data)
                response_data["databaseStatus"] = "Saved to Database"
            except Exception as e:
                logging.error(f"Cosmos DB Error: {e}")
                response_data["databaseStatus"] = f"Failed to save: {str(e)}"
        else:
            response_data["databaseStatus"] = "Local Mode (Not Saved)"

        return func.HttpResponse(json.dumps(response_data, indent=2), mimetype="application/json", status_code=200)
    else:
        return func.HttpResponse(
            json.dumps({"error": "No text provided. Use ?text=YourText in the URL."}),
            mimetype="application/json",
            status_code=400
        )

# =============================================================================
# ENDPOINT 2: GetAnalysisHistory
# =============================================================================
@app.route(route="GetAnalysisHistory", methods=["GET"])
def GetAnalysisHistory(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Fetching history logs...')
    if not container:
        return func.HttpResponse(json.dumps({"error": "Database not configured yet."}), mimetype="application/json", status_code=500)

    try:
        limit = int(req.params.get('limit', '10'))
        query = f"SELECT * FROM c ORDER BY c.metadata.analyzedAt DESC OFFSET 0 LIMIT {limit}"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        return func.HttpResponse(json.dumps({"count": len(items), "results": items}, indent=2), mimetype="application/json", status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"error": str(e)}), mimetype="application/json", status_code=500)