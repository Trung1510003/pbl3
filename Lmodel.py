from gpt4all import GPT4All
import google.generativeai as genai

def loadModel2():
    genai.configure(api_key="AIzaSyCLBKbVMYfvAyDtA1E_AOsho31SYztZ-iM")
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model

def answer2(model, context):
    response = model.generate_content(context)
    return response.text

def loadModel():
    model_name = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
    model = GPT4All(model_name=model_name) 
    return model

def answer(model, context):
    with model.chat_session():
        text = model.generate(context)
    return text