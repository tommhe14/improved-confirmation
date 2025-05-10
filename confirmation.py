import discord
from discord.ext import commands
import asyncio
from typing import Optional

class Confirmation:
    """Represents a message to let the user confirm a specific action."""

    def __init__(
        self,
        client: discord.Client,
        color: int = 0x000000,
        message: Optional[discord.Message] = None,
    ):
        self._client = client
        self.color = color
        self._confirmed = None
        self.message = message
        self._embed: Optional[discord.Embed] = None

    @property
    def confirmed(self) -> Optional[bool]:
        """Whether the user has confirmed the action."""
        return self._confirmed

    async def confirm(
        self,
        text: str,
        user: discord.User,
        channel: Optional[discord.TextChannel] = None,
        hide_author: bool = False,
        timeout: int = 20,
    ) -> Optional[bool]:
        """
        Run the confirmation.

        :param text: The confirmation text.
        :param user: The user who has to confirm.
        :param channel: The channel the message will be sent to. Must only be specified if `self.message` is None.
        :param hide_author: Whether or not the `user` should be set as embed author.
        :param timeout: Seconds to wait until stopping to listen for user interaction.
        :return: True when it's been confirmed, otherwise False. Will return None when a timeout occurs.
        """
        emb = discord.Embed(description=text, color=self.color)
        if not hide_author:
            emb.set_author(name=str(user), icon_url=user.avatar.url)

        self._embed = emb

        if self.message is None:
            self.message = await channel.send(embed=emb)

        msg = self.message

        yes_button = discord.ui.Button(emoji=discord.PartialEmoji(name="✅"), custom_id="confirm_yes")
        no_button = discord.ui.Button(emoji=discord.PartialEmoji(name="❌"), custom_id="confirm_no")

        view = discord.ui.View()
        view.add_item(yes_button)
        view.add_item(no_button)

        await msg.edit(embed=emb, view=view)

        def check(interaction):
            return interaction.message.id == msg.id and interaction.user.id == user.id

        try:
            interaction = await self._client.wait_for("interaction", check=check, timeout=timeout)
            if interaction.data['custom_id'] == "confirm_yes":
                self._confirmed = True
            elif interaction.data['custom_id'] == "confirm_no":
                self._confirmed = False

            await interaction.response.defer()
            return self._confirmed

        except asyncio.TimeoutError:
            self._confirmed = None
            return

        finally:
            await msg.edit(view=None)

    async def update(self, text: str, color: int = 0x000000):
        """
        Update the confirmation message.

        :param text: The new text for the confirmation message.
        :param color: The color of the embed.
        """
        if self._embed:
            self._embed.description = text
            self._embed.color = color
            await self.message.edit(embed=self._embed)

class BotConfirmation(Confirmation):
    def __init__(
        self,
        interaction: discord.Interaction,
        color: int = 0x000000,
        message: Optional[discord.Message] = None,
        ephemeral: bool = False,
    ):
        self._interaction = interaction
        self.ephemeral = ephemeral
        super().__init__(interaction.client, color, message)

    async def confirm(
        self,
        text: str,
        user: Optional[discord.User] = None,
        channel: Optional[discord.TextChannel] = None,
        hide_author: bool = False,
        timeout: int = 20,
    ) -> Optional[bool]:

        if user is None:
            user = self._interaction.user

        if self.message is None and channel is None:
            channel = self._interaction.channel

        emb = discord.Embed(description=text, color=self.color)
        if not hide_author:
            if user.avatar:
                emb.set_author(name=str(user), icon_url=user.avatar.url)

        self._embed = emb

        yes_button = discord.ui.Button(emoji=discord.PartialEmoji(name="✅"), custom_id="confirm_yes")
        no_button = discord.ui.Button(emoji=discord.PartialEmoji(name="❌"), custom_id="confirm_no")

        view = discord.ui.View()
        view.add_item(yes_button)
        view.add_item(no_button)

        await self._interaction.response.send_message(embed=emb, view=view, ephemeral=self.ephemeral)
        self.message = await self._interaction.original_response()

        def check(interaction):
            return (
                interaction.message.id == self.message.id
                and interaction.user.id == user.id
                and interaction.data.get("custom_id") in ["confirm_yes", "confirm_no"]
            )

        try:
            interaction = await self._client.wait_for("interaction", check=check, timeout=timeout)
            if interaction.data['custom_id'] == "confirm_yes":
                self._confirmed = True
            elif interaction.data['custom_id'] == "confirm_no":
                self._confirmed = False

            await interaction.response.defer()

        except asyncio.TimeoutError:
            self._confirmed = None

        finally:
            await self._interaction.edit_original_response(view=None)

        return self._confirmed


    async def update(self, text: str, color: int = 0x000000):
        """
        Update the confirmation message.

        :param text: The new text for the confirmation message.
        :param color: The color of the embed.
        """
        if self._embed:
            self._embed.description = text
            self._embed.color = color
            await self._interaction.edit_original_response(embed=self._embed)
