from django.shortcuts import render
import requests
import json
import random


def index(request):
    return render(request, 'WordDic/index.html')

def add_to_dic(dic, key, value):
    if key in dic:
        dic[key].append(value)
    else:
        dic[key] = [value]

def get_data(word):
    app_id = "ff4a096a"
    app_key = "0ec8192d96bc98bff0b70f92368f8bdd"
    language = "en-gb"
    url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word.lower()
    r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    data = r.json()

    result = {}
    for item in range(len(data["results"])):
        for key, value in data["results"][item].items():
            add_to_dic(result, key, value)

    lexicalEntries = {}
    for item in range(len(result["lexicalEntries"][0])):
        for key, value in result["lexicalEntries"][0][item].items():
            add_to_dic(lexicalEntries, key, value)
    entries = {}
    for item in range(len(lexicalEntries["entries"])):
        for item2 in range(len(lexicalEntries["entries"][item])):
            for key, value in lexicalEntries["entries"][item][item2].items():
                add_to_dic(entries, key, value)
    defi = {}
    for key in entries:
        for i in range(len(entries[key])):
            for j in range(len(entries[key][i])):
                if isinstance(entries[key][i][j], str):
                    print(entries[key][i][j])
                else:
                    for k, v in entries[key][i][j].items():
                        add_to_dic(defi, k, v)
    subsense = {}
    if "subsenses" in defi:
        for item in range(len(defi["subsenses"])):
            for item2 in range(len(defi["subsenses"][item])):
                for k, v in defi["subsenses"][item][item2].items():
                    add_to_dic(subsense, k, v)
    defi["subsenses"] = subsense
    return defi

def get_images(word):
    url = 'https://pixabay.com/api/?key=18135885-6452f9fc49c5982740904652b'
    params = {"per_page":5, "category":"computer", "safesearch":True}
    params["q"] = word
    response = requests.get(url, params = params)
    image = response.json()
    images = {}
    for i in range(len(image["hits"])):
        images[i] = image["hits"][i]["webformatURL"]
    return images

def get_misc(word):
    misc = {}
    url = 'https://api.datamuse.com/words'
    params = {"rel_ant":f"{word}"}
    anto = requests.get(url, params = params)
    ant = anto.json()
    param = {"rel_jjb":f"{word}"}
    adje = requests.get(url, params = param)
    adj = adje.json()
    if len(adj) >= 5:
        ran_adj = random.sample(adj, 5)
        misc["adjective"] = ran_adj
    else:
        misc["adjective"] = adj

    par = {"rel_jja":f"{word}"}
    n = requests.get(url, params = par)
    noun = n.json()
    if len(noun) >= 5:
        ran_noun = random.sample(noun, 5)
        misc["noun"] = ran_noun
    else:
        misc["noun"] = noun
    misc["antonyms"] = ant

    return misc

def search(request):
    if request.method == 'POST':
        word = request.POST.get("word")
        defi = get_data(word)
        images = get_images(word)
        misc = get_misc(word)
        defi["image"] = images
        dic = {
            "defi":defi, "word":word, "misc":misc
        }
        return render(request, 'WordDic/searched.html', dic)