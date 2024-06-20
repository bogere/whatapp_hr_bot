# WhatApp HR Bot (Twilio AI CHallenge)

This is a Python application that allows you to load a CSV file for employee FAQs and ask questions about it using natural language. The application uses a LLM to generate a response about your CSV File.

## How it works

<!-- The application reads the PDF and splits the text into smaller chunks that can be then fed into a LLM. It uses OpenAI embeddings to create vector representations of the chunks. The application then finds the chunks that are semantically similar to the question that the user asked and feeds those chunks to the LLM to generate a response. -->

To build an HR WhatsApp chatbot using Twilio API and a custom knowledgebase in Python with LangChain, you need to follow these steps:
Set up Twilio for WhatsApp:
Create a Twilio account and set up a WhatsApp Sandbox.
Get your Twilio Account SID, Auth Token, and WhatsApp-enabled phone number.

### Build the chatbot:

- Set up the Flask web framework to handle incoming messages.
- Use LangChain to process incoming messages and generate responses based on your custom knowledgebase.
- Use the Twilio API to send responses back to the user via WhatsApp.

## Installation

To install the repository, please clone this repository and install the requirements:

```
pip install -r requirements.txt
```

You will also need to add your OpenAI API key to the `.env` file.

## Usage

```
streamlit run app.py
```

## Deploying the chatbot

- Run the Flask app locally:

```
python app.py
```

- Use a tool like ngrok to expose the Flask app to the internet:

```
ngrok http 5000
```

- Configure the Twilio Webhook:
  In the Twilio Console, navigate to your WhatsApp Sandbox settings.
  Set the "WHEN A MESSAGE COMES IN" URL to your ngrok URL, e.g., http://<your-ngrok-id>.ngrok.io/whatsapp.
  Now, when you send a message to your WhatsApp Sandbox number, the Flask app will handle the incoming message, process it using LangChain, and respond accordingly.

## Contributing

This repository is for educational purposes only and is not intended to receive further contributions. It is supposed to be used as support material for the YouTube tutorial that shows how to build the project.
