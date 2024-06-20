import os
from dotenv import load_dotenv
import pandas as pd
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain

# loads the environment variables from .env file
load_dotenv()# take environment variables

# Load knowledgebase
knowledgebase = pd.read_csv('data/employee_book.csv')

# Initialize Flask app
app = Flask(__name__)
# Twilio configuration
account_sid = os.getenv('TWILIO_ACCOUNT_SID') # works if set env variables in OS.s
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

# Initialize LangChain with OpenAI API key from environment
openai_api_key = os.getenv('OPENAI_API_KEY')

# Define the prompt template for OpenAI
prompt_template = PromptTemplate(
    instruction = "Answer the following question using the provided context:\nContext: {}\nQuestion: {}",
)


# Initialize LangChain
llmx = OpenAI(api_key=openai_api_key,temperature=0.9)  # You can customize the temperature as needed

# Initialize LangChain with pre-trained question-answering chain
qa_chain = load_qa_chain(llm=llmx, prompt_template=prompt_template)



def get_answer(question):
    # Simple search in the knowledgebase
    response = knowledgebase[knowledgebase['question'].str.contains(question, case=False, na=False)]
    if not response.empty:
        return response.iloc[0]['answer']
    else:
        # If no answer found, use LangChain for complex questions
        #return "I'm sorry, I don't have an answer for that."
        context = knowledgebase.to_string(index=False) # Use entire knowledgebase as context
        answer = qa_chain.run(question=question, context=context)
        return answer


@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()
    
    # Get the answer from LangChain
    answer = get_answer(incoming_msg)
    
    # Send the response back to WhatsApp
    msg.body(answer)
    
    return str(resp)

if __name__ == '__main__':
    app.run(port=5000)
