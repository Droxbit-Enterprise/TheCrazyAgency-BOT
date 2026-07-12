import os
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))
URL_STATIC= "https://panel-droxbit-media-706168159909-us-east-2-an.s3.us-east-2.amazonaws.com/The+Crazy+Agency/media/"