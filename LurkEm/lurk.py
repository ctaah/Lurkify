import os
import asyncio
import discord
from colorama import Fore, Style


import colorama
colorama.init()


intents = discord.Intents.all()


async def change_status(client):
    print("\nSelect the type of activity:")
    print("1. Playing")
    print("2. Listening")
    print("3. Streaming")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        activity_title = input("Enter the title for Playing activity: ")
        await client.change_presence(activity=discord.Game(name=activity_title))
        print(Fore.GREEN + f"\nStatus changed to Playing {activity_title}" + Style.RESET_ALL)
    elif choice == 2:
        activity_title = input("Enter the title for Listening activity: ")
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity_title))
        print(Fore.GREEN + f"\nStatus changed to Listening {activity_title}" + Style.RESET_ALL)
    elif choice == 3:
        activity_title = input("Enter the title for Streaming activity: ")
        activity_url = input("Enter the URL for Streaming activity: ")
        await client.change_presence(activity=discord.Streaming(name=activity_title, url=activity_url))
        print(Fore.GREEN + f"\nStatus changed to Streaming {activity_title} at {activity_url}" + Style.RESET_ALL)


async def check_administrator_permissions(client):
    for guild in client.guilds:
        permissions = guild.me.guild_permissions
        if permissions.administrator:
            print(Fore.LIGHTBLUE_EX + f"{guild.name} - ID: {guild.id} - ADMINISTRATOR PERMISSIONS ENABLED" + Style.RESET_ALL)
        else:
            print(Fore.LIGHTRED_EX + f"{guild.name} - ID: {guild.id} - NO ADMINISTRATOR PERMISSIONS" + Style.RESET_ALL)


async def print_channel_messages(client):
    
    print("\nSelect a server:")
    for i, guild in enumerate(client.guilds):
        print(f"{i + 1}. {guild.name}")

    server_choice = int(input("Enter your choice: ")) - 1
    selected_guild = client.guilds[server_choice]

    
    print("\nSelect a channel:")
    for i, channel in enumerate(selected_guild.text_channels):
        print(f"{i + 1}. {channel.name}")

    channel_choice = int(input("Enter your choice: ")) - 1
    selected_channel = selected_guild.text_channels[channel_choice]

    
    num_messages = int(input("Enter the number of messages to print: "))

    
    async for message in selected_channel.history(limit=num_messages):
        print(f"{message.created_at.strftime('%Y-%m-%d %H:%M:%S')} {message.author}: {message.content}")


async def send_message_with_attachments(client):
    
    print("\nSelect a server:")
    for i, guild in enumerate(client.guilds):
        print(f"{i + 1}. {guild.name}")

    server_choice = int(input("Enter your choice: ")) - 1
    selected_guild = client.guilds[server_choice]

    
    print("\nSelect a channel:")
    for i, channel in enumerate(selected_guild.text_channels):
        print(f"{i + 1}. {channel.name}")

    channel_choice = int(input("Enter your choice: ")) - 1
    selected_channel = selected_guild.text_channels[channel_choice]

    
    message_content = input("Enter the message content: ")

    
    has_attachments = input("Does the message have attachments? (yes/no): ").lower() == 'yes'

    
    files = []
    if has_attachments:
        num_attachments = int(input("Enter the number of attachments: "))
        for i in range(num_attachments):
            file_path = input(f"Enter the file path for attachment {i + 1}: ")
            file = discord.File(file_path)
            files.append(file)

    
    await selected_channel.send(content=message_content, files=files)



async def print_ban_list(client):
    for guild in client.guilds:
        print(f"\nBans in {guild.name}:")
        try:
            bans = guild.bans()
            for ban_entry in bans:
                user = ban_entry.user
                print(f"{user.name} - {user.id}")
        except discord.Forbidden:
            print("Missing permissions to view bans")
        except discord.HTTPException as e:
            print(f"An error occurred while fetching bans: {e}")



async def handle_events(client):
    
    print(Fore.YELLOW + f"\nLogged in as {client.user}" + Style.RESET_ALL)

    
    while True:
        print("\nUser Menu:")
        print("1. Change status")
        print("2. Check server permissions")
        print("3. Print messages from server")
        print("4. Send message with attachments")
        print("5. Print ban list from all servers")
        print("6. Logout")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            await change_status(client)
            await asyncio.sleep(1)  
            os.system('cls' if os.name == 'nt' else 'clear')  
        elif choice == 2:
            await check_administrator_permissions(client)
            input("\nPress Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')  
        elif choice == 3:
            await print_channel_messages(client)
            input("\nPress Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')  
        elif choice == 4:
            await send_message_with_attachments(client)
            input("\nPress Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')  
        elif choice == 5:
            await print_ban_list(client)
            input("\nPress Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')  
        elif choice == 6:
            print(Fore.RED + "\nLogging out..." + Style.RESET_ALL)
            await client.close()
            break


class MyClient(discord.Client):
    async def on_ready(self):
        await handle_events(self)


client = MyClient(intents=intents)


async def main():
    while True:
        try:
            
            os.system('cls' if os.name == 'nt' else 'clear')

            
            token = input("Enter your Discord bot token: ")

            print(Fore.YELLOW + "\nLogging in..." + Style.RESET_ALL)

            
            await client.start(token)
        except KeyboardInterrupt:
            print(Fore.RED + "\nLogging out..." + Style.RESET_ALL)
            await client.close()
            break
        except Exception as e:
            print(Fore.RED + f"\nAn error occurred: {e}" + Style.RESET_ALL)
            input("Press Enter to continue...")


if __name__ == "__main__":
    asyncio.run(main())
