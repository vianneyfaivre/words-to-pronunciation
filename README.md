# Words to Pronunciation

This script converts words to audio files. 

It also generates a HTML document (actually it is a Jekyll HTML document) that lists all those words.

The result can be seen in my website https://vianneyfaivre.com/things/pronunciation-playground

Built with `Python` and `Jinja2`.

## Requirements

* Python 3
* A JSON Array of words must be put in the file `in/data.json` 

## Run

Run the following commands:

```
py -m pip install -r requirements.txt
py convert.py
```

Artifacts produced:

* `assets/pronunciation/*.mp3`
* `assets/2019-06-17-pronunciation-playground.html`
