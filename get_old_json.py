import json
import requests
import os.path
import logging

if not os.path.exists("cache_block_color.json"):
    logging.info("Getting data from githubusercontent")
    json_url = "https://raw.githubusercontent.com/StevenLi-phoenix/minecraft_streaming/113262fabaa1ad292d4794a1c9aa7564c2330ff7/block_color.json"
    block_color = json.loads(requests.get(json_url).content.decode())
    # assert data could use
    with open("cache_block_color.json","w") as f:
        f.write(json.dumps(block_color))
else:
    logging.info("Use cache")
    block_color = json.load(open("cache_block_color.json","r"))

if __name__ == "__main__":
    logging.basicConfig(filename = "logs/test_old_json.log", level=logging.DEBUG)
    print(block_color)
