import discord
from discord.ext import commands
import os
import json
from datetime import datetime, timedelta
from colorama import init, Fore, Style

init(autoreset=True)

with open("config.json") as f:
    config = json.load(f)

TOKEN = config.get("token")
VOUCH_CHANNEL = config.get("vouch_channel", "")
VOUCH_FORMAT = config.get("vouch_format", "+rep Legit got Working (Acc Name) Account")
HITS_CHANNEL = config.get("hits_channel", "")
RESTOCK_CHANNEL = config.get("restock_channel", "")
PING_ROLE = config.get("ping_role", "")
ACCESS_ROLE = config.get("access_role", "")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

stock_folder = "stock"
os.makedirs(stock_folder, exist_ok=True)
cooldowns = {}

def log(status, cmd, user, extra=""):
    time = datetime.now().strftime("%H:%M:%S")
    color = {"SUCCESS": Fore.GREEN, "ERROR": Fore.RED, "INFO": Fore.CYAN, "CMD": Fore.YELLOW}.get(status, Fore.WHITE)
    emoji = {"SUCCESS": "✅", "ERROR": "❌", "INFO": "ℹ️", "CMD": "⌨️"}.get(status, "")
    print(f"{color}[{time}] {emoji} [{status}] {user} ran '{cmd}' -> {extra}")

def is_admin(ctx):
    return ctx.author.guild_permissions.administrator

def has_access(ctx):
    if ACCESS_ROLE:
        return any(role.id == int(ACCESS_ROLE.replace("<@&", "").replace(">", "")) for role in ctx.author.roles)
    return True

@bot.event
async def on_ready():
    ascii_art = (
        Fore.MAGENTA + r"""
          _____                     .__                       __  .__                  ___________________ _______   
         /  _  \   ____  ____  ____ |  |   ________________ _/  |_|__| ____   ____    /  _____/\_   _____/ \      \  
        /  /_\  \_/ ___\/ ___\/ __ \|  | _/ __ \_  __ \__  \\   __\  |/  _ \ /    \  /   \  ___ |    __)_  /   |   \ 
       /    |    \  \__\  \__\  ___/|  |_\  ___/|  | \/ __ \|  | |  (  <_> )   |  \ \    \_\  \|        \/    |    \
       \____|__  /\___  >___  >___  >____/\___  >__|  (____  /__| |__|\____/|___|  /  \______  /_______  /\____|__  /
         \/     \/    \/    \/          \/           \/                    \/          \/        \/         \/
                                       💥 Made by acceleration.back
         
""" + Style.RESET_ALL
    )
    print(ascii_art)
    log("SUCCESS", "Startup", bot.user.name, "Bot is ready!")

@bot.command()
async def stock(ctx):
    if not has_access(ctx):
        await ctx.send("**❌ You don't have permission.**")
        log("ERROR", ".stock", ctx.author.name, "Missing access role")
        return
    embed = discord.Embed(title="📦 Stock - Services", color=discord.Color.blue())
    available = ""
    unavailable = ""
    for file in os.listdir(stock_folder):
        path = os.path.join(stock_folder, file)
        with open(path, 'r') as f:
            lines = f.readlines()
            count = len(lines)
            if count > 0:
                available += f"`{file[:-4]}`: {count} Accounts\n"
            else:
                unavailable += f"`{file[:-4]}`: Out of stock\n"
    embed.add_field(name="✅ Available", value=available or "None", inline=False)
    embed.add_field(name="❌ Out of Stock", value=unavailable or "None", inline=False)
    embed.set_footer(text="Made by acceleration.back")
    await ctx.send(embed=embed)
    log("CMD", ".stock", ctx.author.name, "Checked stock")

@bot.command()
async def gen(ctx, category: str):
    if not has_access(ctx):
        await ctx.send("**❌ You don't have permission.**")
        return
    user_id = str(ctx.author.id)
    now = datetime.utcnow()
    if user_id in cooldowns and now < cooldowns[user_id]:
        left = cooldowns[user_id] - now
        await ctx.send(f"⌛ Cooldown: try again in {left.seconds // 60}m")
        return
    path = os.path.join(stock_folder, f"{category}.txt")
    if not os.path.exists(path):
        await ctx.send("❌ Invalid category!")
        return
    with open(path, 'r') as f:
        lines = f.readlines()
    if not lines:
        await ctx.send("❌ No Stock Reatrd !")
        return
    account = lines.pop(0).strip()
    with open(path, 'w') as f:
        f.writelines(lines)
    cooldowns[user_id] = now + timedelta(hours=1)
    embed_dm = discord.Embed(title="✅ Success!", description=f"Your `{category}` account: `{account}`\nVouch: {VOUCH_CHANNEL}\nFormat: `{VOUCH_FORMAT.replace('(Acc Name)', category)}`", color=discord.Color.green())
    try:
        await ctx.author.send(embed=embed_dm)
        public_embed = discord.Embed(title="✅ Success!", description=f"{category} has been sent to **{ctx.author.name}**", color=discord.Color.green())
        await ctx.send(embed=public_embed)
        if HITS_CHANNEL:
            hits = await bot.fetch_channel(int(HITS_CHANNEL.split("/")[-1]))
            await hits.send(embed=public_embed)
    except:
        await ctx.send("❌ Unable to DM you.")
    log("CMD", f".gen {category}", ctx.author.name, "Sent 1 account")

@bot.command()
@commands.has_permissions(administrator=True)
async def create(ctx, category: str):
    path = os.path.join(stock_folder, f"{category}.txt")
    if not os.path.exists(path):
        open(path, 'w').close()
        await ctx.send(f"✅ Created `{category}` category.")
    else:
        await ctx.send(f"⚠️ `{category}` already exists.")

@bot.command()
@commands.has_permissions(administrator=True)
async def delete(ctx, category: str):
    path = os.path.join(stock_folder, f"{category}.txt")
    if os.path.exists(path):
        os.remove(path)
        await ctx.send(f"🗑️ Deleted `{category}`.")
    else:
        await ctx.send("❌ Category not found.")

@bot.command()
@commands.has_permissions(administrator=True)
async def add(ctx, category: str):
    if not ctx.message.attachments:
        await ctx.send("📎 Please attach a `.txt` file.")
        return
    file = ctx.message.attachments[0]
    content = await file.read()
    lines = content.decode().splitlines()
    path = os.path.join(stock_folder, f"{category}.txt")
    with open(path, 'a') as f:
        f.write('\n'.join(lines) + '\n')
    if RESTOCK_CHANNEL:
        chan = await bot.fetch_channel(int(RESTOCK_CHANNEL.split("/")[-1]))
        msg = discord.Embed(title="📥 Stock Restocked", description=f"{PING_ROLE} {category} restocked with {len(lines)} accounts.", color=discord.Color.green())
        await chan.send(embed=msg)
    await ctx.send(f"✅ Added {len(lines)} to `{category}`.")

@bot.command()
@commands.has_permissions(administrator=True)
async def set(ctx, key: str, *, value: str):
    keys = ["vouch_channel", "vouch_format", "hits_channel", "restock_channel", "ping_role", "access_role"]
    if key not in keys:
        await ctx.send("❌ Invalid key.")
        return
    config[key] = value
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    await ctx.send(f"✅ `{key}` set to `{value}`")

@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member = None, *, reason="No reason"):
    if not member:
        await ctx.send("❌ User not found.")
        return
    await member.send(embed=discord.Embed(title="🚫 Kicked", description=reason, color=discord.Color.red()))
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member.mention} has been kicked.")

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member = None, *, reason="No reason"):
    if not member:
        await ctx.send("❌ User not found.")
        return
    await member.send(embed=discord.Embed(title="⛔ Banned", description=reason, color=discord.Color.red()))
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member.mention} has been banned.")

@bot.command()
@commands.has_permissions(administrator=True)
async def timeout(ctx, member: discord.Member = None, duration: str = "", *, reason="No reason"):
    if not member:
        await ctx.send("❌ User not found.")
        return
    times = {"h": 3600, "d": 86400, "w": 604800}
    if not duration or duration[-1] not in times:
        await ctx.send("❌ Use valid duration: 1h, 1d, 1w")
        return
    secs = int(duration[:-1]) * times[duration[-1]]
    until = datetime.utcnow() + timedelta(seconds=secs)
    await member.timeout(until, reason=reason)
    await member.send(embed=discord.Embed(title="⏰ Timed Out", description=f"{duration} | Reason: {reason}", color=discord.Color.orange()))
    await ctx.send(f"🕒 {member.mention} timed out.")

@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(title="✨ Command Guide - Acceleration Bot", color=discord.Color.purple())
    embed.add_field(name="**.stock** `Usage`", value="Displays available and out-of-stock categories.", inline=False)
    embed.add_field(name="**.gen <category>** `Usage`", value="Public: Sends an account to your DM. 1-hour cooldown.", inline=False)
    embed.add_field(name="**.create <category>** `Admin`", value="Create a new stock category file.", inline=False)
    embed.add_field(name="**.delete <category>** `Admin`", value="Delete a stock category file.", inline=False)
    embed.add_field(name="**.add <category> (attach .txt)** `Admin`", value="Add multiple accounts to category.", inline=False)
    embed.add_field(name="**.set <key> <value>** `Admin`", value="Set keys: vouch_channel, vouch_format, hits_channel, restock_channel, ping_role, access_role", inline=False)
    embed.add_field(name="**.kick <@user> <reason>** `Admin`", value="Kick a user with reason.", inline=False)
    embed.add_field(name="**.ban <@user> <reason>** `Admin`", value="Ban a user with reason.", inline=False)
    embed.add_field(name="**.timeout <@user> <duration> <reason>** `Admin`", value="Timeout user for 1h/1d/1w and notify.", inline=False)
    embed.set_footer(text="Made by acceleration.back ✨ Best UI Experience")
    await ctx.send(embed=embed)

bot.run(TOKEN)
