#all required tools

import requests
class agentTools:
    def __init__(self,agent):
        self.actions = []
        self.agent = agent
        self.answer = ""

    def getAnswer(self):
        answer = self.answer
        self.answer = ''
        return answer

    def returnActions(self,):
        actions = self.actions
        self.actions = []
        return actions
    
    def errorActions(self,):
        self.actions.append({"addMessage":{'input':self.agent.getUserQuery(),'response':"No data found in archive"}})

    def summarizeAnswerAndDisplayPDF(self,data):
        ''' this provides summarizes and shortens the answer to the user and displays the relevant pdf

        Parameters:
        data (dict): data retreived from self.tools.search_arxiv_by_title

        Usage:
        self.tools.summarizeAnswerAndDisplayPDF(self.tools.search_arxiv_by_title("standard attention"))
        '''
        if('error' in data.keys()):
            self.errorActions()
            return
        summary = self.createShortSummary(data['summary'])
        self.displayPdf(data['PDF_URL'])
        self.answerUser(summary)
    
    def answerAndDisplayPDF(self,data):
        ''' this provides the answer to the user and displays the relevant pdf

        Parameters:
        data (dict): data retreived from self.tools.search_arxiv_by_title

        Usage:
        self.tools.answerAndDisplay(self.tools.search_arxiv_by_title("standard attention"))
        '''
        if('error' in data.keys()):
            self.errorActions()
            return
        print(data)
        self.displayPdf(data['PDF_URL'])
        self.answerUser(data['summary'])

    def displayPdf(self,url:str):
        ''' this is a function definition
        arg1 (str): url of the retreived PDF

        displays or shows the PDF to the user, does not return anything
        data = self.tools.search_arxiv_by_title("standard attention")
        self.tools.displayPdf(data["PDF_URL"])
        '''
        if(url==None):
            self.errorActions()
            return
        self.actions.append({"display":url})
        
    def CreateNewChat(self):
        ''' this function creates a new chat for the user
            needs no arguments
            creates a new chat for the user
            does not return anything
        '''
        self.actions.append({"newChat":""})

    def answerUser(self,answer:str):
        ''' this function returns a text response to the user.
            answer (str): Your answer
            
            shows/displays your answer to the user 
            does not return anything
        '''
        if(answer==None):
            self.errorActions()
            return
        self.answer = answer
        self.actions.append({"addMessage":{'input':self.agent.getUserQuery(),'response':answer}})

    def createShortSummary(self,information):
        '''
            this is a function definition
            information: The information you want to summarize
            
            returns a shortened summary of the information provided in string format
            Usage:
                data = self.tools.search_arxiv_by_title("standard attention")
                summary = self.tools.createShortSummary(data["summary"])
        
        '''
        if(information==None):
            self.errorActions()
            return 'No information'
        prompt='summarize the following informations into a maximum of 3 sentences:\n' + information
        summary = self.agent.ravenSummarize(prompt)
        return summary 
    
    def search_arxiv_by_title(self,paper_topic)->dict:
        ''' This function returns the information of the topic you want to know about in dectionary format
            
            Parameters:
            paper_topic (str): The topic you want to know about
            
            returns data from arxiv in dictionary format with keys:
            title: Title of the paper
            summary: summary of the paper
            PDF_URL: Url of the required pdf

            Example:
            prompt "i want to know about standard attention"
            Usage:
            data = self.tools.search_arxiv_by_title("standard attention")
            URL = data["PDF_URL"]
            title =  data["title"]
            summary =  data["summary"]

            This function should not be called on its own and only called along with an action:
            example:
            summary = self.tools.createShortSummary(information = self.tools.search_arxiv_by_title("standard attention")["summary"])
            self.tools.displayPdf(URL=self.tools.search_arxiv_by_title("standard attention")["PDF_URL"])
        '''
        api_url = 'http://export.arxiv.org/api/query'

        # Constructing the query parameters
        params = {
            'search_query': f"ti:\"{paper_topic}\"",  # Title search query
            'start': 0,  # Start with the first result
            'max_results': 1  # Limiting to one result for simplicity
        }

        try:
            # Sending GET request to ArXiv API
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Raise error for bad response status

            # Parse the XML response
            from xml.etree import ElementTree as ET
            root = ET.fromstring(response.content)

            # Extracting relevant information from the response
            entries = root.findall('{http://www.w3.org/2005/Atom}entry')
            if entries:
                entry = entries[0]
                title = entry.find('{http://www.w3.org/2005/Atom}title').text
                summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
                pdf_url = entry.find('{http://www.w3.org/2005/Atom}link[@title="pdf"]')
                if pdf_url is not None:
                    pdf_url = pdf_url.attrib['href']
                else:
                    pdf_url = "PDF not available"
                result = {'Title':title,'summary':summary,'PDF_URL':pdf_url}
                return result
            else:
                result = {"error":"No paper found with that context."}
                return result

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")