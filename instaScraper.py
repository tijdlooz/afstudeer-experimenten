import http.client
import urllib
import json

import re
from PIL import Image
import requests
from io import BytesIO

import time



while True:
  print("naar welke instagram @ moet ik opzoek gaan? (@ zonder @ intypen)")
  at = input()

  if at.lower() == "stop":
     break
  else:
    print("ik ga opzoek naar " + at + ', een moment geduld aub...')

    conn = http.client.HTTPSConnection("api.webscraping.ai")
    api_params = {
      'api_key': '99e05d8f-cee4-4926-8a52-7f14095cc121', 
      'proxy': 'residential', 
      'js': 'false',
      'timeout': 25000, 
      'url': 'https://www.instagram.com/' + at + '/?__a=1&__d=1'
    }
    conn.request("GET", f"/html?{urllib.parse.urlencode(api_params)}")

    res = conn.getresponse()
    #print(res)

    json_raw = res.read().decode("utf-8")
    json_object = json.loads(json_raw)

    json_string = json.dumps(json_object, indent=1)

    with open("json_data.json", 'w') as outfile:
        outfile.write(json_string)

    file = open("json_data.json")
    data = json.loads(file.read())

    #print(data['graphql']["user"]["profile_pic_url"])

    time.sleep(3)

    if 'graphql' in data: 
      print("data gevonden!")
      print()
      url = data['graphql']["user"]["profile_pic_url_hd"]
      #print("url = " + url)
      response = requests.get(url)

      img_data = BytesIO(response.content)
      img = Image.open(img_data)
      img.show()

      print("volledige naam:" + data['graphql']["user"]["full_name"])
      print("bio:" + data['graphql']["user"]["biography_with_entities"]["raw_text"])
      print()
      print("wiens privacy gaan we nu op de proef stellen?")
      print()
      file.close

    else:
      print("geen data gevonden.. Mogelijk verkeerd getypt, en anders gewoon opnieuw proberen...")

      