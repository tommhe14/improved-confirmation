# discord-confirmation

`discord-confirmation` is a Python library for creating confirmation messages in Discord interactions.

## Installation

You can install `discord-confirmation` via pip:

```bash
pip install discord-confirmation
```

## Documentation

Confirmation Class
async confirm(text: str, user: discord.User, channel: Optional[discord.TextChannel] = None, hide_author: bool = False, timeout: int = 20) -> Optional[bool]
Run the confirmation.

text (str): The confirmation text.
user (discord.User): The user who has to confirm.
channel (Optional[discord.TextChannel]): The channel the message will be sent to. Must only be specified if self.message is None.
hide_author (bool): Whether or not the user should be set as embed author.
timeout (int): Seconds to wait until stopping to listen for user interaction.
Returns: True when it's been confirmed, otherwise False. Will return None when a timeout occurs.
async update(text: str, color: int = 0x000000)
Update the confirmation message.

text (str): The new text for the confirmation message.
color (int): The color of the embed.
BotConfirmation Class
async confirm(text: str, user: Optional[discord.User] = None, channel: Optional[discord.TextChannel] = None, hide_author: bool = False, timeout: int = 20) -> Optional[bool]
Run the confirmation for bot interactions.

text (str): The confirmation text.
user (Optional[discord.User]): The user who has to confirm. Defaults to the interaction user.
channel (Optional[discord.TextChannel]): The channel the message will be sent to. Defaults to the interaction channel.
hide_author (bool): Whether or not the user should be set as embed author.
timeout (int): Seconds to wait until stopping to listen for user interaction.
Returns: True when it's been confirmed, otherwise False. Will return None when a timeout occurs.
async update(text: str, color: int = 0x000000)
Update the confirmation message.

text (str): The new text for the confirmation message.
color (int): The color of the embed.

## Example Usage

```py
from discord.ext import commands
import discord
import confirmation

bot = commands.Bot(command_prefix='!')

@app_commands.command()
async def my_command(self, interaction: discord.Interaction):
    confirm = confirmation.BotConfirmation(interaction=interaction, color=0x012345, ephemeral=True)
    confirmed = await confirm.confirm("Are you sure you want to proceed?")
    
    if confirmed:
        await confirm.update("Confirmed!")
    else:
        await confirm.update("Cancelled!")
```

