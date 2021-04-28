from pygelbooru import Gelbooru
import os, dotenv
import asyncio

dotenv.load_dotenv()
# Your gelbooru api key
api_key = os.getenv('API_KEY')
# Your gelbooru user id
user_id = os.getenv('USER_ID')
 
gelbooru = Gelbooru(api_key=api_key, user_id=user_id)

async def get_image(tags):
    result = await gelbooru.random_post(tags=tags)
    return result
