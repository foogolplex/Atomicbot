import os, discord, asyncio, shutil, requests
from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer
from joebooru import get_image 
from joe4chan import get_thread
from joechess import JoeChess

class JoeBiden:
	def __init__(self):
		self.intents = discord.Intents().all()
		self.client = commands.Bot(command_prefix="joe ", intents=self.intents)
		self.chess_games = []

	# Check if a user already has a game initiated
	def game_redundancy_check(self, user):
		for game in self.chess_games:
			if game.user == user:
				return True
		return False
	
	# Get the chess game corresponding to a user
	def get_chess_game(self, user):
		for game in self.chess_games:
			if game.user == user:
				return game

	# Save an image from a url
	async def imgurl_image(self, url):
		response = requests.get(url, stream=True)
		with open('img.png', 'wb') as out_file:
			shutil.copyfileobj(response.raw, out_file)
		del response

	def start_bot(self):
		# Chess commands
		# ________________________________________
		@self.client.command()
		async def chess(ctx, rating):
			author = ctx.author
			# Make sure a game hasn't already been initialized with the message sender
			has_game = self.game_redundancy_check(author)	
			if has_game:
				await ctx.send("You already are playing a game with Joe. Please end the game with: joe ff")	
			else:
				game = JoeChess(int(rating), author)
				self.chess_games.append(game)
				await ctx.send(f'Game initialized with {author}... Your color is {game.player_color}. My elo rating is {rating}.')
				if game.color == 'white':
					move = game.ai_move()
					await ctx.send(f'I moved to {move}')

		@self.client.command()
		async def move(ctx, move):
			# Make sure a game hasn't already been initialized with the message sender
			has_game = self.game_redundancy_check(ctx.author)
			if has_game:
				game = self.get_chess_game(ctx.author)
				is_valid = game.move(move)
				if is_valid == 'failed':
					await ctx.send("Holy shit retard retard retard retard reatdsdadf aka invalid fucking move dumbass hoe...")
				else:
					await ctx.send(f"You moved to {is_valid}.")
					move = game.ai_move()	
					await ctx.send(f"I moved to {move}")
					await ctx.send(f"```{game.stockfish.get_board_visual()}```")
			else:
				await ctx.send("You can't move a piece in a nonexistent game you absolute retard.")

		@self.client.command()
		async def ff(ctx):
			has_game = self.game_redundancy_check(ctx.author)
			if has_game == False:
				await ctx.send("You can't ff a game you aren't playing dipfart.")
			else:
				game = self.get_chess_game(ctx.author)
				self.chess_games.remove(game)
				await ctx.send("You lose shitter fucklord.")

		# Music commands
		# ________________________________________
		@self.client.command()
		async def play(ctx, *nameparts):
			name = ""
			for part in nameparts:
				name += part
				name += " "
			name = name[:-1] 
			#print(name)

		@self.client.command()
		async def join(ctx):
		    channel = ctx.author.voice.channel
		    await channel.connect()

		@self.client.command()
		async def leave(ctx):
		    await ctx.voice_client.disconnect()
		
		# Misc commands
		# ________________________________________
		@self.client.command(brief='Joe\'s drip')
		async def drip(ctx):
		    await ctx.send('https://pbs.twimg.com/media/EmgiTIlXEAEsn5T.jpg')

		@self.client.command()
		async def pat(ctx):
			await ctx.send(file=discord.File(r'joe_pet.gif'))

		# 4chan commands
		# ________________________________________
		@self.client.command(brief='Sends a random thread from 4chan.org/b/')
		async def b(ctx):
			urls = await get_thread()
			imgurl = urls[0]
			tmpurl = imgurl[17:]
			imgurl = "https://i.4cdn" + tmpurl	

			await self.imgurl_image(imgurl) 
			await ctx.send(urls[1], file=discord.File("img.png"))
			os.remove("img.png")

		# Imageboard commands
		# ________________________________________
		@self.client.command(brief='Sends a random image from gelbooru.com with optional tags')
		async def vault(ctx, *tags):
			await ctx.send(await get_image(tags))

		# Event handling
		# ________________________________________
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
