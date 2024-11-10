
#? ----- Imports ------

from dotenv import load_dotenv
import os
import google.generativeai as genai
import argparse

#? ----- Setup ------

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="file to send to ai")
parser.add_argument("-p", "--prompt", help="path to write AI response to")

load_dotenv()

api_key = os.getenv("API_KEY")
os.environ['API_KEY'] = api_key
genai.configure(api_key=os.environ['API_KEY'])

#? ----- Variables ------

args = parser.parse_args()
prompt = args.prompt
file = args.file
system_instructions = open("context/instructions.txt", "r").read()

#? ----- Functions ------

def get_completion(prompt, model="gemini-1.5-flash", **kwargs):
    model = genai.GenerativeModel(model)
    generation_config = {
        "temperature" : .5,
        "max_output_tokens": 500
    }
    generation_config.update(kwargs)
    response = model.generate_content(prompt, generation_config=generation_config)
    return response.text

    

def write_history(user_input, response):
    history = open("context/history.txt", "a")
    history.write(f"User prompt: [{user_input}]\nAI response: [{response}]\n----------\n")
    history.close()

def get_history():
    history = open("context/history.txt", "r")
    history_text = history.read()
    history.close()
    return history_text

def cl():
    os.system('clt' if os.name == 'nt' else 'clear')

#? ----- Main ------

def main():
    user_input = ""
    while user_input != "exit":
        user_input = input("Ask me: ")
        cl()
        response = get_completion(f"""{system_instructions}\n\n{get_history()}\n\n----- USER INPUT -----\n\n{user_input}""")
        write_history(user_input, response)
        print(response)
    system_instructions.close()

if __name__ == "__main__":
    main()