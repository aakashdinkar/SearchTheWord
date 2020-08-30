from django.shortcuts import render
import requests
import json


def index(request):
    return render(request, 'WordDic/index.html')

def search(request):
    if request.method == 'POST':
        word = request.POST.get("word")
        app_id = "ff4a096a"
        app_key = "0ec8192d96bc98bff0b70f92368f8bdd"
        language = "en-gb"
        url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word.lower()
        r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
        data = r.json()
        word = data["id"]
        audio_file = data["results"][0]["lexicalEntries"][0]["entries"][0]["pronunciations"][0]["audioFile"]
        phonetic = data["results"][0]["lexicalEntries"][0]["entries"][0]["pronunciations"][0]["phoneticSpelling"]
        definitions = data["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]
        examples = data["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["examples"][0]["text"]
        synonyms = data["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["synonyms"]
        category = data["results"][0]["lexicalEntries"][0]["lexicalCategory"]["text"]

        return render(request, 'WordDic/searched.html', {"word": word, "audio_file":audio_file, "phonetic":phonetic, "definitions":definitions, "examples":examples, "synonyms":synonyms, "category":category})