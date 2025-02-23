import discord
from colorama import Fore, Style


def print_add(message):
    print(f'{Fore.GREEN}[+]{Style.RESET_ALL} {message}')

def print_delete(message):
    print(f'{Fore.RED}[-]{Style.RESET_ALL} {message}')

def print_warning(message):
    print(f'{Fore.RED}[WARNING]{Style.RESET_ALL} {message}')

def print_error(message):
    print(f'{Fore.RED}[ERROR]{Style.RESET_ALL} {message}')


class Clone:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
        for role in guild_to.roles:
            try:
                if role.name != "@everyone":
                    await role.delete()
                    print_delete(f"Deleted Role: {role.name}")
            except discord.Forbidden:
                print_error(f"Error While Deleting Role: {role.name}")
            except discord.HTTPException:
                print_error(f"Unable to Delete Role: {role.name}")

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        roles = [role for role in guild_from.roles if role.name != "@everyone"]
        roles = roles[::-1]  # Reverse to ensure proper order
        for role in roles:
            try:
                await guild_to.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    colour=role.colour,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                print_add(f"Created Role {role.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Role: {role.name}")
            except discord.HTTPException:
                print_error(f"Unable to Create Role: {role.name}")

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        for channel in guild_to.channels:
            try:
                await channel.delete()
                print_delete(f"Deleted Channel: {channel.name}")
            except discord.Forbidden:
                print_error(f"Error While Deleting Channel: {channel.name}")
            except discord.HTTPException:
                print_error(f"Unable to Delete Channel: {channel.name}")

    @staticmethod
    async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
        for channel in guild_from.categories:
            try:
                overwrites_to = {discord.utils.get(guild_to.roles, name=key.name): value for key, value in channel.overwrites.items()}
                new_channel = await guild_to.create_category(
                    name=channel.name,
                    overwrites=overwrites_to)
                await new_channel.edit(position=channel.position)
                print_add(f"Created Category: {channel.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Category: {channel.name}")
            except discord.HTTPException:
                print_error(f"Unable to Create Category: {channel.name}")

    @staticmethod
    async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild):
        for channel_text in guild_from.text_channels:
            category = discord.utils.get(guild_to.categories, name=channel_text.category.name) if channel_text.category else None
            overwrites_to = {discord.utils.get(guild_to.roles, name=key.name): value for key, value in channel_text.overwrites.items()}
            try:
                new_channel = await guild_to.create_text_channel(
                    name=channel_text.name,
                    overwrites=overwrites_to,
                    position=channel_text.position,
                    topic=channel_text.topic,
                    slowmode_delay=channel_text.slowmode_delay,
                    nsfw=channel_text.nsfw)
                if category:
                    await new_channel.edit(category=category)
                print_add(f"Created Text Channel: {channel_text.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Text Channel: {channel_text.name}")
            except discord.HTTPException:
                print_error(f"Unable to Create Text Channel: {channel_text.name}")

        for channel_voice in guild_from.voice_channels:
            category = discord.utils.get(guild_to.categories, name=channel_voice.category.name) if channel_voice.category else None
            overwrites_to = {discord.utils.get(guild_to.roles, name=key.name): value for key, value in channel_voice.overwrites.items()}
            try:
                new_channel = await guild_to.create_voice_channel(
                    name=channel_voice.name,
                    overwrites=overwrites_to,
                    position=channel_voice.position,
                    bitrate=channel_voice.bitrate,
                    user_limit=channel_voice.user_limit)
                if category:
                    await new_channel.edit(category=category)
                print_add(f"Created Voice Channel: {channel_voice.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Voice Channel: {channel_voice.name}")
            except discord.HTTPException:
                print_error(f"Unable to Create Voice Channel: {channel_voice.name}")

    @staticmethod
    async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
        try:
            icon_image = await guild_from.icon.read() if guild_from.icon else None
            await guild_to.edit(name=guild_from.name)
            if icon_image:
                await guild_to.edit(icon=icon_image)
                print_add(f"Guild Icon Changed: {guild_to.name}")
        except discord.Forbidden:
            print_error(f"Error While Changing Guild Icon: {guild_to.name}")
