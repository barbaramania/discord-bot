"""
This program interacts with the AWS EC2 metadata to retrieve specific server information.
It demonstrates a basic Discord bot that responds to user messages with EC2 metadata details.
Key Features:
- Retrieves the EC2 server's region, public IP, availability zone, instance ID, and type.
- Provides a help command for users to see all available commands.
- Includes error handling to account for potential issues, such as server unavailability or connection problems, providing informative error messages when necessary.
- Designed with scalability in mind, allowing adaptation for multiple EC2 servers if needed.

Usage:
1. Ensure that the bot token is stored in a `.env` file under the variable `TOKEN`.
2. Install necessary Python libraries: `discord`, `ec2_metadata`, and `python-dotenv`.
3. Run the program, and the bot will respond to messages in a Discord server.

Commands:
- `hello` / `hi`: Greets the user.
- `bye`: Says goodbye.
- `region`: Returns the EC2 server's region.
- `ip`: Returns the EC2 server's public IP.
- `zone`: Returns the availability zone of the EC2 server.
- `id`: Returns the EC2 instance ID.
- `type`: Returns the EC2 instance type.
- `help`: Lists all available commands.
"""

import discord
from discord.ext import commands
import os
import random
from ec2_metadata import ec2_metadata
from dotenv import load_dotenv

# Load the .env file
load_dotenv("token.env")

# Error handling for missing environment variables
try:
    token = str(os.getenv('TOKEN'))
    if not token:
        raise ValueError("Bot token is missing. Ensure it is defined in 'token.env'.")
except Exception as e:
    print(f"Error: {e}")
    exit(1)

# Print the EC2 instance region, ID, and availability zone
print(f"Region: {ec2_metadata.region}")
print(f"Instance ID: {ec2_metadata.instance_id}")
print(f"Availability Zone: {ec2_metadata.availability_zone}")

# Combine the Availability Zone and Region for context
print(f"The EC2 instance is located in {ec2_metadata.availability_zone} within the {ec2_metadata.region} region.")


# Intents setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

# Create the Discord client
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    # Extract user and message details
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    print(f'Message "{user_message}" by {username} on {channel}')

    # Skip if the message is from the bot itself
    if message.author == client.user:
        return

    # Respond to user commands
    try:
        if user_message.lower() in ["hello", "hi", "hello world"]:
            await message.reply(f'Hello {username}!')
        elif user_message.lower() == "bye":
            await message.reply(f'Bye {username}!')
        elif user_message.lower() == "region":
            await message.reply(f'Here is the EC2 Instance Region: {ec2_metadata.region}')
        elif user_message.lower() == "ip":
            await message.reply(f'Here is the public EC2 Instance IP: {ec2_metadata.public_ipv4}')
        elif user_message.lower() == "zone":
            await message.reply(f'Here is the EC2 Instance Availability Zone: {ec2_metadata.availability_zone}')
        elif user_message.lower() == "id":
            await message.reply(f'Here is the EC2 Instance ID: {ec2_metadata.instance_id}')
        elif user_message.lower() == "type":
            await message.reply(f'Here is the type of Instance Currently Running: {ec2_metadata.instance_type}')
        elif user_message.lower() == "Tell me about my server!":
            await message.reply(f'The EC2 instance is located in {ec2_metadata.availability_zone} within the {ec2_metadata.region} region.')
        elif user_message.lower() == "help":
            await message.reply(
                "# __Here is a list of my commands:__\n"
                "hello/hi: Greets the user\n"
                "bye: Says goodbye\n"
                "region: Returns the Region of the EC2 Server\n"
                "ip: Returns the Public IP of the EC2 Server\n"
                "zone: Returns the Availability Zone of the EC2 Server\n"
                "id: Returns the EC2 Instance ID\n"
                "type: Returns the type of the Current Running Instance"
            )
        else:
            await message.reply("I didn't understand that command. Type `help` for a list of my commands.")
    except Exception as e:
        # Handle errors gracefully
        await message.reply("An error occurred while processing your request. Please try again later.")
        print(f"Error: {e}")

# Start the bot
try:
    client.run(token)
except Exception as e:
    print(f"Failed to start the bot: {e}")
