import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import urlretrieve

def main():
    words = []
    wordsNotFound = []

    # Read words
    with open('in/data.json', 'r') as f:
        words = json.load(f)

    # Download words as mp3
    for word in words:

        # Handle 'a_word vs another_word' special case
        parts = word.split('vs')
        if len(parts) > 1:
            for part in parts:
                if not processWord(part):
                    wordsNotFound.append(part)
        else:
            if not processWord(word):
                wordsNotFound.append(word)

    if len(wordsNotFound) == 0:
        print("All words have been found!")
    else:
        print(wordsNotFound)

def processWord(word): 
    fileName = transformWord(word)

    url = getUrl(fileName)
    out = getOut(fileName)

    return writeToFile(url, out)        

transformWord = lambda word: word.lower().strip()
getUrl = lambda fileName: f'https://howjsay.com/mp3/{fileName}.mp3'
getOut = lambda fileName: f'out/{fileName}.mp3'

def writeToFile(url, out): 
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

main()