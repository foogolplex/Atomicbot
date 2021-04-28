import os, discord, asyncio, shutil, requests
from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from joebooru import get_image 
from joe4chan import get_thread

class JoeBiden:
	def __init__(self):
		self.intents = discord.Intents().all()
		self.client = commands.Bot(command_prefix="joe ", intents=self.intents)
	
	# Save an image from a url
	async def imgurl_image(self, url):
		response = requests.get(url, stream=True)
		with open('img.png', 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)
		del response

	def start_bot(self):
		@self.client.command()
		async def join(ctx):
		    channel = ctx.author.voice.channel
		    await channel.connect()

		@self.client.command()
		async def leave(ctx):
		    await ctx.voice_client.disconnect()

		@self.client.command(brief='Joe\'s drip')
		async def drip(ctx):
		    await ctx.send('https://pbs.twimg.com/media/EmgiTIlXEAEsn5T.jpg')

		@self.client.command()
		async def pat(ctx):
			await ctx.send(file=discord.File(r'joe_pet.gif'))

		@self.client.command(brief='Sends a random thread from 4chan.org/b/')
		async def b(ctx):
			urls = await get_thread()
			imgurl = urls[0]
			tmpurl = imgurl[17:]
			imgurl = "https://i.4cdn" + tmpurl	

			await self.imgurl_image(imgurl) 
			await ctx.send(urls[1], file=discord.File(r'img.png'))
			os.remove("img.png")

		@self.client.command(brief='Sends a random image from gelbooru.com with optional tags')
		async def vault(ctx, *tags):
			await ctx.send(await get_image(tags))

		@self.client.command()
		async def play(ctx, *nameparts):
			name = ""
			for part in nameparts:
				name += part
				name += " "
			name = name[:-1] 
			print(name)

		@self.client.event
		async def on_ready():
		    await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Spazz - Fly Away x A.G."))

		@self.client.event
		async def on_message(message):
		    if message.content == "joe":
		        await message.channel.send("NICE DRIP MY NIGGA!")
		    else:
		        await self.client.process_commands(message)

		token = os.getenv('MY_TOKEN')
		self.client.run(token)
