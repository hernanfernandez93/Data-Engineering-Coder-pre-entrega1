from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json



load_dotenv()

client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id+":"+client_secret
    auth_bytes=auth_string.encode("utf-8")
    auth_base64 =str(base64.b64encode(auth_bytes),"utf-8")
    url="https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic "+auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result ["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url=url + query
    result = get(query_url, headers=headers)
    json_result=json.loads(result.content)["artists"]["items"]
    return json_result [0]
    

def list_albums(token, artistid):
    url = "https://api.spotify.com/v1/artists/"+artistid+"/albums"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result=json.loads(result.content)["items"]
    return json_result

artist_list = ['Red Hot Chilli peppers','Twenty one pilots','foster the people', 'panic at the disco', 'saint motel', 'sound garden']

D1 = {}

token=get_token()
for name in artist_list:
    artist_object=search_for_artist(token,name)
    artist_id=artist_object['id']
    albums=list_albums(token, artist_id)
    for i, album in enumerate(albums):
        print(f"{i+1}-{name}-{album['name']}-{album['release_date']}")





 
