import os
from dotenv import load_dotenv
import pandas as pd
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
#from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chains.question_answering import load_qa_chain
# better  n modern way to use langchain
#from langchain.agents import create_csv_agent
#from langchain_experimental.agents import create_csv_agent
from langchain_experimental.agents import create_csv_agent
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI #ChatAnthropic  or ChatOpenAI Azure


# loads the environment variables from .env file
load_dotenv()# take environment variables

# Load knowledgebase
#knowledgebase = pd.read_csv('data/employee_book.csv')
knowledgebase = 'data/employee_book.csv'

# Initialize Flask app
app = Flask(__name__)
# Twilio configuration
account_sid = os.getenv('TWILIO_ACCOUNT_SID') # works if set env variables in OS.s
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

# Initialize LangChain with OpenAI API key from environment
openai_api_key = os.getenv('OPENAI_API_KEY')

# Define the prompt template for OpenAI
# prompt_templatex = PromptTemplate(
#     instruction = "Answer the following question using the provided context:\nContext: {}\nQuestion: {}"
# )


# Initialize LangChain
#llmx = OpenAI(api_key=openai_api_key,temperature=0.9)  # You can customize the temperature as needed

# Initialize LangChain with pre-trained question-answering chain
#qa_chain = load_qa_chain(llm=llmx, prompt_template=prompt_templatex)
#qa_chain = load_qa_chain(llm=llmx)
# agent = create_csv_agent(
#     llmx,
#     knowledgebase,
#     verbose=True,
#     agent_type = AgentType.ZERO_SHOT_REACT_DESCRIPTION
# )
agent = create_csv_agent(
    ChatOpenAI(model='gpt-3.5-turbo',
               temperature=0.9,
               openai_api_key=openai_api_key),
               knowledgebase,
               verbose=True,
               agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)





def get_answer(question):
    # Simple search in the knowledgebase
    # response = knowledgebase[knowledgebase['question'].str.contains(question, case=False, na=False)]
    # if not response.empty:
    #     return response.iloc[0]['answer']
    # else:
    #     # If no answer found, use LangChain for complex questions
    #     #return "I'm sorry, I don't have an answer for that."
    #     context = knowledgebase.to_string(index=False) # Use entire knowledgebase as context
    #     #answer = qa_chain.run(question=question, context=context)
    #     answer = agent.run(question)
    #     return answer
    answer = agent.run(question)
    return answer



# def make_call(msg):
#     # make a call to the employee from the Whatapp bot.
#     #what about sending the message as voice response.. call the person directly
#     print('Making a call to HR manager')
#     # what about the HR manager phone number
#     hr_tel_no = os.getenv('HR_MANAGER_TEL_NO')
#     staff_tel_no = os.getenv('STAFF_TEL_NO')
#     new_call = client.calls.create(to=staff_tel_no, from_=hr_tel_no, method="GET")
#     print("Serving TwiML")
#     twiml_response = VoiceResponse()
#     #twiml_response.say(answer)
#     twiml_response.say(msg)
#     twiml_response.hangup()
#     twiml_xml = twiml_response.to_xml()
#     print("Generated twiml: {}".format(twiml_xml))


@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()
    
    # Get the answer from LangChain
    answer = get_answer(incoming_msg)

    #make that call to employee
    #say_hello = make_call("Please check your whatapp for message")
    
    # Send the response back to WhatsApp
    msg.body(answer)

    return str(resp)

if __name__ == '__main__':
    app.run(port=5000)
