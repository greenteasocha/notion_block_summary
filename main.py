import os
import json
import requests
from dotenv import load_dotenv
from pprint import pprint
from collections import defaultdict
from typing import *

load_dotenv()
SECRET = os.environ["NOTION_SECRET"]
NOTION_HOST = "https://api.notion.com/v1/blocks/"
ENDPOINT_GET_BLOCK = "{page_id}/children"

RETRIEVE_TEXT_PREFIX = "TODO: "

class Getter(object):
    def __init__(self):
        self.header = {
            "Notion-Version": "2021-05-13",
            "Authorization": "Bearer secret_" + SECRET
        }
        self.decoder = json.JSONDecoder()

    def get(self, page_id: str) -> dict:
        result = self.send_request(page_id)
        return self.decoder.decode(result.text)

    def send_request(self, page_id: str) -> requests.models.Response:
        # TODO: Error Handling
        url = NOTION_HOST + ENDPOINT_GET_BLOCK.format(page_id=page_id)
        result = requests.get(url, headers=self.header)
        return result

class Summarizer(object):
    def __init__(self):
        self.contents = []
        self.getter = Getter()
        self.summarize(os.environ["NOTION_TOP_PAGE"])

        for content in self.contents:
            pprint(content)

    def summarize(self, page_id: str):
        response = self.getter.get(page_id)
        for result in response["results"]:
            if result["type"] == "paragraph":
                self.parse_paragraph(result)
            elif result["type"] == "child_page":
                self.summarize(result["id"])

    def parse_paragraph(self, result: dict):
        try:
            for text in result["paragraph"]["text"]:
                plain_text = text["plain_text"]
                if plain_text.startswith(RETRIEVE_TEXT_PREFIX):
                    # content = plain_text[len(RETRIEVE_TEXT_PREFIX):]
                    content = plain_text
                    self.contents.append(content)
            return
        except KeyError:
            return

def main():
    summarizer = Summarizer()

if __name__ == "__main__":
    main()