import os
import discord
import asyncio
from discord.ext import commands
import colorama
from colorama import Fore, Style
colorama.init()

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Bot is ready.')
    await main_menu()

async def main_menu():
    while True:
        print("\n--- Main Menu ---")
        print("1. Print messages from a server")
        print("2. Change bot status")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            await print_server_messages()
        elif choice == "2":
            await change_status()
        elif choice == "3":
            print("Exiting bot.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

async def print_server_messages():
    servers = bot.guilds

    print("\n--- Servers ---")
    for index, server in enumerate(servers, 1):
        print(f"{index}. {server.name}")

    server_choice = input("Enter the number corresponding to the server you want to scrape: ")

    try:
        server_index = int(server_choice) - 1
        selected_server = servers[server_index]

        print(f"Scraping messages from {selected_server.name}...")
        await scrape_server_messages(selected_server)
    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid server number.")

async def scrape_server_messages(server):
    text_channels = [channel for channel in server.channels if isinstance(channel, discord.TextChannel)]

    print("\n--- Available Channels ---")
    for index, channel in enumerate(text_channels, 1):
        print(f"{index}. {channel.name}")

    channel_choice = input("Enter the number corresponding to the channel you want to scrape: ")

    try:
        channel_index = int(channel_choice) - 1
        selected_channel = text_channels[channel_index]

        message_count = int(input("Enter the number of messages to print: "))

        print(f"\n{Fore.RED}--- Messages from #{selected_channel.name} ---{Style.RESET_ALL}")
        messages = []
        async for message in selected_channel.history(limit=message_count):
            if not message.author.bot:
                messages.append(message)


        sorted_messages = sorted(messages, key=lambda msg: msg.created_at)

        for message in sorted_messages:
            print(f"{Fore.MAGENTA}Author: {Fore.CYAN}{message.author.display_name}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Timestamp: {Fore.GREEN}{message.created_at}{Style.RESET_ALL}")
            print(f"Content: {message.content}")
            print("---------------------")

            if message.attachments:
                print(f"\n{Fore.RED}--- MEDIA ---{Style.RESET_ALL}")
                for attachment in message.attachments:
                    if attachment.url:
                        print(f"{Fore.RED}{attachment.url}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}[Media Link]{Style.RESET_ALL}")
    except (ValueError, IndexError):
        print("Invalid input. Please enter valid numbers.")

async def change_status():
    new_status = input("Enter the new status: ")
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name=new_status))
    print(f"Bot status changed to 'Away' with custom playing status '{new_status}'.")

bot.run('PROVIDE-TOKEN', bot=True)
