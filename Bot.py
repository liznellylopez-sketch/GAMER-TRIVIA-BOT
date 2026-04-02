import discord
from discord.ext import commands
from discord import app_commands
import random
import time

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ------------------------
# BAD WORD FILTER
# ------------------------
bad_words = [
    "fuck","bitch","asshole","cunt","nigger","nigga","motherfucker",
    "fucking","goddammit","pigfucker","pussy","prick","piss","bastard",
    "cock","ass","sisterfucker","brotherfucker","danmit","fucker",
    "dumbass","dumb-ass"
]

# ------------------------
# COOLDOWN SYSTEM
# ------------------------
user_cooldowns = {}

def is_on_cooldown(user_id):
    if user_id in user_cooldowns:
        if time.time() - user_cooldowns[user_id] < 10:  # 10 sec cooldown
            return True
    user_cooldowns[user_id] = time.time()
    return False

# ------------------------
# TRIVIA DATA
# ------------------------
trivia_questions = [
    {"q": "What game features Master Chief?", "a": "halo"},
    {"q": "What company made PlayStation?", "a": "sony"},
    {"q": "What game is Steve from?", "a": "minecraft"},
]

hard_questions = [
    {"q": "What year was the first Legend of Zelda released?", "a": "1986"},
    {"q": "Who is the creator of Metal Gear?", "a": "kojima"},
]

fun_facts = [
    "Mario was originally called Jumpman.",
    "The PlayStation was almost a Nintendo console.",
]

cool_facts = [
    "Minecraft is the best-selling game of all time.",
    "GTA V made over $1 billion in 3 days.",
]

# ------------------------
# EVENTS
# ------------------------
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"🎮 Welcome {member.mention} to the server!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Bad word filter
    for word in bad_words:
        if word in message.content.lower():
            await message.delete()
            await message.channel.send(f"{message.author.mention}, watch your language.")
            return

    await bot.process_commands(message)

# ------------------------
# SLASH COMMANDS
# ------------------------

@bot.tree.command(name="trivia_bot", description="Get a trivia question")
async def trivia(interaction: discord.Interaction):
    if is_on_cooldown(interaction.user.id):
        await interaction.response.send_message("⏳ Slow down!", ephemeral=True)
        return

    q = random.choice(trivia_questions)
    await interaction.response.send_message(f"🧠 Trivia: {q['q']}")

@bot.tree.command(name="truefan_test", description="Hardcore gamer test")
async def truefan(interaction: discord.Interaction):
    if is_on_cooldown(interaction.user.id):
        await interaction.response.send_message("⏳ Slow down!", ephemeral=True)
        return

    q = random.choice(hard_questions)
    await interaction.response.send_message(f"🔥 TRUE FAN TEST: {q['q']}")

@bot.tree.command(name="fun_fact", description="Random fun fact")
async def funfact(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(fun_facts))

@bot.tree.command(name="cool_fact", description="Random cool fact")
async def coolfact(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(cool_facts))

@bot.tree.command(name="announce", description="Announce an event")
@app_commands.describe(message="Event message")
async def announce(interaction: discord.Interaction, message: str):
    await interaction.channel.send(f"📢 EVENT: {message}")
    await interaction.response.send_message("Event announced!", ephemeral=True)

# ------------------------
# RUN BOT
# ------------------------
bot.run("YOUR_BOT_TOKEN")
