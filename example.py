# All imports used currently, some will be redundant on example 
import discord 
from discord.ext import commands
from datetime import datetime, timedelta
import time
import random
import re
import pytz

# General permissions for the bot to interact with discord
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True 
intents.guilds = True 
intents.members = True 

### This entire section is how to integrate reaction to role assignment ###
# Role assignment block
ROLE_MESSAGE_ID = 1243561804706353233  # ID of the message with the role buttons
ROLE_EMOJIS = {
  '<:UCOB:1243556440178692137>': 'UCOB Enjoyer',
  '<:UWU:1243556443005911154>' : 'UWU Enjoyer',
  '<:TEA:1243556435145789513>' : 'TEA Enjoyer',
  '<:DSR:1243556432385806336>' : 'DSR Enjoyer',
  '<:TOP:1243556437809041562>' : 'TOP Enjoyer'
}
@bot.event
async def on_raw_reaction_add(payload):
  if payload.message_id == ROLE_MESSAGE_ID:
    guild = bot.get_guild(payload.guild_id)
    if guild is None:
      print('Guild not found')
      return

    role_name = ROLE_EMOJIS.get(str(payload.emoji))
    if role_name is None:
      return

    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
      return

    member = guild.get_member(payload.user_id)
    if member is None:
      print('Member not found')
      return

    await member.add_roles(role)
    print(f"Assigned {role.name} to {member.display_name}")

@bot.event
async def on_raw_reaction_remove(payload):
  if payload.message_id == ROLE_MESSAGE_ID:
    guild = bot.get_guild(payload.guild_id)
    if guild is None:
      return

    role_name = ROLE_EMOJIS.get(str(payload.emoji))
    if role_name is None:
      return

    role = discord.utils.get(guild.roles, name=role_name)
    if role is None:
      return

    member = guild.get_member(payload.user_id)
    if member is None:
      return

    await member.remove_roles(role)
    print(f"Removed {role.name} from {member.display_name}")
### END OF THIS SECTION ###

### This is the bot chat reaction block ### 
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "exaflare" in message.content.lower() or "exaflares" in message.content.lower():
        await message.channel.send("Exaflares coming up!")
      
    await bot.process_commands(message)
### END OF THIS SECTIONS ###

### Slash "/" command section ### 
# Dictionary mapping arguments for /tea command
tea_dict = {
    'p1 toolbox': "TEA p1 toolbox: <https://ff14.toolboxgaming.space/?id=830419115443951&preview=1>",
    'LC toolbox': "TEA Limit Cut: \n"
                  "1 - 2 - 5 - 6 W/NE \n"
                  "3 - 4 - 7 - 8 E/SW \n"
                  "3rd explosion 1/2 \n"
                  "5th explosion 3/4 \n"
                  "7th explosion 5/6 \n"
                  "9th explosion 7/8 \n"
                  "TEA LC toolbox: <https://ff14.toolboxgaming.space/?id=240411819443951&preview=1>",
    'p2 toolbox': "TEA p2 toolbox: <https://ff14.toolboxgaming.space/?id=340414049443951&preview=1>",
    'p3 TS/INC toolbox': "TEA Timestop and Inception toolbox: <https://ff14.toolboxgaming.space/?id=105865886660661&preview=1>",
    'p3 WH toolbox': "TEA Wormhole toolbox: <https://ff14.toolboxgaming.space/?id=236244852760461&preview=1>",
    'p4 toolbox': "TEA p4 toolbox: <https://ff14.toolboxgaming.space/?id=205867198660661&preview=1>",
    'p2 DRK': "STAND STILL AND LET THING RESOLVE",
    'p2 GNB': "p2 OT POS (GNB): \n"
              "Grab CC go SOUTH. \n"
              "Wait for the cast and dodge Missile command for dodgeable puddles with phys-range (DNC) at SOUTH wall, go WEST if ice aoe. \n "
              "Pop the mines in front of missile-command baits, HEAVY mits. \n"
              "After 2nd water go SW and face CC middle. \n"
              "Line up in the middle closest to CC.\n"
              "Bring CC to BEHIND the ICE at WEST \n"
              "Go to Nisi pair (Blue-Purple-Orange-Green) After Success Pull boss to NW",
    'p2 WHM': "p2 REGEN POS (WHM): \n"
              "Go west (if water stand marker), then wait for enumerations at LOOK-BJ left.\n"
              "If water-vuln'd go to BJ-TANK (DRK). If no-vuln'd go NE. \n"
              "Line up in the middle SECOND closest to CC. \n"
              "If lightning, go CC tank. If no water-vuln go NE to stack. \n"
              "IF nisi carrier line behind WEST ice (Blue-Purple-Orange-Green)",
    'p2 SCH': "p2 SHIELD POS (SCH): \n"
              "Go west (if water stand marker), then wait for enumerations at LOOK-BJ right. \n"
              "If water-vuln'd go to BJ-TANK (DRK). If no-vuln'd go NE. \n"
              "Line up in the middle SECOND closest to BJ.\n"
              "If lightning, go CC tank. If no water-vuln go NE to stack.\n"
              "IF nisi carrier line behind WEST ice (Blue-Purple-Orange-Green)",
    'p2 NIN': "p2 NIN POS: \n"
              "If lightning go BJ-Tank. If not chill at BJ-Left leg. \n"
              "stack with WHM at west for enumerations. \n"
              "Pass nisi to partner. \n"
              "Continue chilling.\n"
              "After flamethrower AND Limitcut shield is broken, pass nisi to required debuff.\n"
              "Go NE to stack with water.\n"
              "IF nisi carrier line behind WEST ice (Blue-Purple-Orange-Green)",
    'p2 DRG': "p2 DRG POS: \n"
              "If lightning go BJ-Tank. If not chill at BJ-Right leg. \n"
              "Enumeration adjusts. \n"
              "Pass nisi to partner. \n"
              "Continue chilling.\n"
              "After flamethrower AND Limitcut shield is broken, pass nisi to required debuff.\n"
              "Go NE to stack with water.\n"
              "IF nisi carrier line behind WEST ice (Blue-Purple-Orange-Green)",
    'p2 DNC': "p2 DNC POS: \n"
              "If not lightning stack at WEST, if lightning go BJ-Tank, then go SOUTH to bait missile command. \n"
              "Enumerations adjust. \n"
              "Pass nisi to partner. \n"
              "Stack at NE marker for water.\n"
              "After flamethrower AND Limitcut shield is broken, pass nisi to required debuff.\n"
              "IF no water-vuln go NE and stack with water pass.\n"
              "IF nisi carrier line behind WEST ice (Blue-Purple-Orange-Green)\n"
              "After Success go to EAST wall and bait BJ's Jump (distance based), and move away from the front of it.",
    'p2 SMN': "p2 SMN POS: \n"
              "If not lightning stack at WEST, if lightning go BJ-Tank, then chill until enumerations, stack with SCH at east stack.\n"
              "Pass nisi to partner. \n"
              "Stack at NE marker for water.\n"
              "After flamethrower AND Limitcut shield is broken, pass nisi to required debuff.\n"
              "IF no water-vuln go NE and stack with water pass.\n"
              "IF nisi carrier line behind WEST ice (Blue-Purple-Orange-Green)",
    'p3 TANK': "p3 TANK Positions: \n"
               "Inception as usual. \n"
               "OT Close to True Heart | MT MIDDLE BJ. \n"
               "BOTH right looking at heart. \n"
               "OT baits BJ jump.",
    'p3 non-TANK': "p3 non tanks: \n"
                   "everyone does same, see toolbox."
}
# /tea command block
@bot.tree.command(name='tea', description='Information on TEA mechanics.')
async def get_info_tea(interaction: discord.Interaction, arg: str):
    response_text = tea_dict.get(arg, "Invalid argument. Please provide a valid argument.")
    if interaction.channel_id == EPHEMERAL_CHANNEL_ID:
        await interaction.response.send_message(response_text, ephemeral=True)
    else:
        await interaction.response.send_message(response_text)
@get_info_tea.autocomplete("arg")
async def autocomplete_info_tea(interaction: discord.Interaction, current: str):
    options = [discord.app_commands.Choice(name=key, value=key) for key in tea_dict.keys() if current.lower() in key.lower()]
    return options
### END OF THIS SECTION ###

# To finish the entire code you want this to be the final line of your code
Bot.run('YOUR DISCORD TOKEN HERE')
