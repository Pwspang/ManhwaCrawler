from dotenv import load_dotenv
import google.generativeai as genai
import os 

preprompt = "I want you to act as an English translator, spelling corrector and improver. I will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in English. The translation should be a conversation. I want you to only reply the correction, the improvements and nothing else, do not write explanations. '{}' "

def main():
    load_dotenv('.env')
    
    API_KEY = os.environ.get("GEMINI_KEY")
    
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(preprompt.format('毛 並 み も す ご く よ く て 気 持 ち い い'))
    
    print(response.text)

if __name__ == "__main__":
    main()