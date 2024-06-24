import inspect
from Libraries.tools import agentTools
import requests

class agent:
    def __init__(self):
        self.agent = None
        self.tools = agentTools(self)
        self.prompt = self.build_raven_prompt()
        self.user_query = ""

    def raven_post(self,payload):
        """
        Sends a payload to a TGI endpoint.
        """
        API_URL = "http://nexusraven.nexusflow.ai"
        headers = {
                "Content-Type": "application/json"
        }
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    def getActions(self):
        return self.tools.returnActions()

    def query_raven(self,prompt):
        prompt = self.addQueryToPrompt(prompt)
        print("prompt",prompt)
        output = self.raven_post({
            "inputs": prompt,
            "parameters" : {"temperature" : 0.001, "stop" : ["<bot_end>"], "return_full_text" : False, "do_sample" : False, "max_new_tokens" : 2048}})
        call = output[0]["generated_text"].replace("Call:", "").strip()
        print("functions to execute:",call)
        exec(call)
        return call

    def ravenSummarize(self,prompt):
        output = self.raven_post({
            "inputs": prompt,
            "parameters" : {"temperature" : 0.001, "stop" : ["<bot_end>"], "return_full_text" : False, "do_sample" : False, "max_new_tokens" : 2048}})
        call = output[0]["generated_text"].replace("Call:", "").strip()
        return call

    def getUserQuery(self):
        return self.user_query

    def getText(self):
        return self.tools.getAnswer()

    def build_raven_prompt(self):
        raven_prompt = ""
        function_list = [self.tools.displayPdf,self.tools.CreateNewChat,self.tools.answerUser,self.tools.search_arxiv_by_title,self.tools.answerAndDisplayPDF,self.tools.summarizeAnswerAndDisplayPDF]
        for function in function_list:
            signature = inspect.signature(function)
            docstring = function.__doc__
            prompt = f'''Function:
            def self.tools.{function.__name__}{signature}
                """
                {docstring.strip()}
                """
                
            '''
            raven_prompt += prompt
        return raven_prompt
    
    def addQueryToPrompt(self,user_query):
        self.user_query = user_query
        rules = "\nWhenver the user asks something, remember to display the pdf relevant to the user as well are the required text. DOnt forget to summarize the text further if required."
        
        prompt = self.prompt + rules +   f"\nUser Query: {user_query}<human_end>"
        return prompt

