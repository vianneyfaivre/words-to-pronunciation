import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import urlretrieve
from jinja2 import Template

IN_WORDS = 'in/data.json'
OUT_FOLDER = 'assets/pronunciation'
OUT_FILE = 'assets/2019-06-17-pronunciation-playground.html'

def main():
    createOutFolder(OUT_FOLDER)
    words = processWords(IN_WORDS)
    # TODO: order words alpha
    # TODO: remove duplicates
    html = generateHtml(words)
    saveHtml(html, OUT_FILE)

# Lambdas
transformWord = lambda word: word.lower().strip()
getUrl = lambda fileName: f'https://text-to-speech-demo.ng.bluemix.net/api/v1/synthesize?text={fileName}&voice=en-GB_KateVoice&download=true&accept=audio/mp3'
getOutFilePath = lambda fileName: f'{OUT_FOLDER}/{fileName}.mp3'

# Functions
def saveHtml(html, file):
    with open(file, 'w') as out:
        out.write(html)

def generateHtml(words):
    with open('in/templates/page.html.jinja') as f:
        tmpl = Template(f.read())
        html = tmpl.render(words = words)

    return html

def processWords(wordsFilePath):
    """
    Processes all words from a given a specific file that contains a JSON Array of words.

    Returns the words that have been successfully downloaded as media files
    """
    words = []
    resolvedWords = []
    wordsNotFound = []

    # Read words
    with open(wordsFilePath, 'r') as f:
        words = json.load(f)

    # Download words as mp3
    for word in words:

        resolvedWord = ResolvedWord(word)

        # Special case with multiple words 'word1 vs word2'
        if not resolvedWord.isSingle():
            for wordPart in resolvedWord.words:
                found = processWord(wordPart)
                if not found:
                    wordsNotFound.append(wordPart)
                else:
                    resolvedWords.append(resolvedWord)
        # Simple case (one word 'word1')
        else:
            found = processWord(word)
            if not found:
                wordsNotFound.append(word)
            else:
                resolvedWords.append(resolvedWord)

    if len(wordsNotFound) > 0:
        print(f"The following words have not been found: {wordsNotFound}")

    return resolvedWords

def processWord(word): 
    """
    Download the word as mp3 and writes it to the out folder

    Returns True/False (if word has been found/not found)
    """
    fileName = transformWord(word)

    url = getUrl(fileName)
    out = getOutFilePath(fileName)

    return writeToFile(url, out)       

def writeToFile(url, out): 
    """
    Downloads file from 'url' and writes it to 'out' file path.

    Returns True when the file has been successfully downloaded and written to 'out'
    """
    if not os.path.isfile(out):
        print(f"GET {url}")
        try: urlretrieve(url, out)
        except HTTPError as e:
            return False
        except URLError as e:
            print('Failed to reach the server: ', e.reason)
            return False
        else:
            return True
    else: 
        return True

def createOutFolder(outFolder):
    if not os.path.isdir(outFolder):
        os.makedirs(outFolder)

class ResolvedWord: 

    def __init__(self, word):
        self.words = []

        parts = word.split('vs')
        if len(parts) > 1:
            for part in parts:
                self.words.append(transformWord(part))
        else:
            self.words.append(transformWord(word))
    
    def isSingle(self):
        return len(self.words) == 1

    def getWord(self):
        return self.words[0]

    def getWords(self):
        return self.words

main()