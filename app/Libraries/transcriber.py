import subprocess
import os

class whisperTranscriber():
    def __init__(self):
        self.model = "Whisper"

    def __call__(self,audioPath):
        print(audioPath)
        result = subprocess.run(['Whisper', audioPath, '--output_dir', 'uploads'], check=True)
        return self.readResult(audioPath)
    
    def readResult(self,path):
        text = ""
        path = path[:-4]+"txt"
        print(path)
        with open(path,'r') as f:
            text = f.read()
        return text