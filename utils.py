import json
import requests


def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)
    
def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)

def add_search_term(search_term):
    search_terms = load_json("search_terms.json")
    if search_term not in search_terms:
        search_terms.append(search_term)
    return save_json("search_terms.json", search_terms)

def remove_search_term(search_term):
    search_terms = load_json("search_terms.json")
    if search_term in search_terms:
        search_terms.remove(search_term)
    return save_json("search_terms.json", search_terms)

def list_search_terms():
    search_terms = load_json("search_terms.json")
    return search_terms

def set_webhook(webhook):
    cfg = load_json("cfg.json")
    cfg["webhook"] = webhook
    return save_json("cfg.json", cfg)

def rm_webhook():
    cfg = load_json("cfg.json")
    cfg.pop("webhook", None)
    return save_json("cfg.json", cfg)

def get_webhook():
    cfg = load_json("cfg.json")
    return cfg["webhook"]

def send_webhook(title, price, link, picture, location, desc):
    webhook = get_webhook()
    embed = {"embeds":[{
        "title": title,
        "url": link,
        "description": desc,
        "color": 16743424,
        "image": {
            "url": picture
        },
        "fields": [
            {
                "name": "Price",
                "value": price,
                "inline": True
            },
            {
                "name": "Location",
                "value": location,
                "inline": True
            }
        ]
    }]}
    requests.post(webhook, json=embed)

def check_link(link):
    links = load_json("links.json")
    if link in links:
        return True
    else:
        return False
    
def add_link(link):
    links = load_json("links.json")
    links.append(link)
    return save_json("links.json", links)