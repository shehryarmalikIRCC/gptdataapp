  
import os  
import logging
import azure.functions as func
import openai
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import json


load_dotenv()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        #parse request body
        req_body = req.get_json()
        user_message = req_body.get('message')

        if not user_message:
            return func.httpResponse(
                json.dumps({"error": "Please pass a 'message' in the request body"}),
                status_code = 400,
                mimetype = "application/json"
            )
        #load env variables
        endpoint = os.getenv("ENDPOINT_URL")
        deployment = os.getenv("DEPLOYMENT_NAME")
        search_endpoint = os.getenv("SEARCH_ENDPOINT")
        search_key = os.getenv("SEARCH_KEY")
        search_index = os.getenv("SEARCH_INDEX_NAME")
        subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
        openai_api_version = os.getenv("API_VERSION")


    


    
        # Initialize Azure OpenAI client with key-based authentication
        client = AzureOpenAI(  
        azure_endpoint=endpoint,  
        api_key=subscription_key,  
        api_version=openai_api_version,  
        )  
      
        # Prepare the chat prompt  
        chat_prompt = [
        {
        "role": "system",
        "content": "You are an AI assistant that helps people find information"
         },

        {"role": "user", "content": user_message},
        ]  
    

        # Generate the completion  
        completion = client.chat.completions.create(  
        model=deployment,  
        messages=chat_prompt,    
        max_tokens=800,  
        temperature=0.7,  
        top_p=0.95,  
        frequency_penalty=0,  
        presence_penalty=0,  
        stop=None,  
        stream=False,
        extra_body={
        "data_sources": [{
          "type": "azure_search",
          "parameters": {
            "endpoint": f"{search_endpoint}",
            "index_name": "test2",
            "semantic_configuration": "default",
            "query_type": "semantic",
            "fields_mapping": {},
            "in_scope": True,
            "role_information": "You are an AI assistant that helps people find information.",
            "filter": None,
            "strictness": 3,
            "top_n_documents": 5,
            "authentication": {
              "type": "api_key",
              "key": f"{search_key}"
            }
          }
        }]
        } 
        )
        ai_reply = completion.choices[0].message['content'].strip()
        return func.HttpResponse(
            json.dumps({"reply":ai_reply}),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return func.HttpResponse(
            json.dumps({"error": "Internal server error"}),
            status_code=500,
            mimetype="application/json"
        )



    