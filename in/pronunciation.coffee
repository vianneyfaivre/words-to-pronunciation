---
---
state = {
    # Map : key=word value=JS Audio object
    words: []

    addWordToState: (word, audio) -> state.words[word] = audio
    getAudio: (word) -> state.words[word]
}

main = () ->
  for wordSpan in document.getElementsByClassName "word"
    
    word = wordSpan.getAttribute("word")
    audio = new Audio("/assets/pronunciation/#{word}.mp3")
    state.addWordToState(word, audio)
  
    wordSpan.addEventListener 'click', (e) -> onWordClick(e.target.getAttribute("word"))
  
onWordClick = (word) ->
  audio = state.getAudio(word)
  audio.play()
  
main()