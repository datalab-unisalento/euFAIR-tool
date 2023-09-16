import requests


def duckduckgo_indexed(link):
    print("LOG: searching on DuckDuckGo")
    response = requests.get(f"https://api.duckduckgo.com/?q={link}&format=json&pretty=1&no_html=1&skip_disambig=1")

    if response.text.find(link) != -1:
        return 1

    return 0
