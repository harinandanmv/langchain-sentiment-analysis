import gradio as gr
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# === Load environment variables ===
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# === Check API key ===
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not set in .env file!")

# === Setup LLM ===
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=api_key
)

# === Prompt Template ===
prompt = PromptTemplate(
    input_variables=["text"],
    template="""
You are a sentiment analysis expert.
Classify the sentiment of the following text as one of: Positive, Negative, or Neutral.
Respond with only the sentiment category.

Text: "{text}"
Sentiment:
"""
)

chain = LLMChain(llm=llm, prompt=prompt)

# === Gradio Function ===
def classify_sentiment(text):
    if not text.strip():
        return "⚠ Please enter some text."
    sentiment = chain.run(text=text)
    return f"Sentiment: {sentiment.strip()}"

# === Gradio UI ===
demo = gr.Interface(
    fn=classify_sentiment,
    inputs=gr.Textbox(label="Enter Text", placeholder="Type your sentence here...", lines=4),
    outputs=gr.Textbox(label="Sentiment"),
    title="🤖 LLM-Based Sentiment Classifier",
    description="Uses GPT-3.5 (via Langchain) to classify the sentiment as Positive, Neutral, or Negative."
)

demo.launch()
