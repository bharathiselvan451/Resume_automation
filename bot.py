from datetime import datetime, timedelta, timezone
import discord
from claudAI import generate_resume, html_to_pdf
import gspread
import time



#
# Replace with your actual token
TOKEN = "MTUwOTA4NjQwMjM4ODgyNDE5NA.G7H_1U.VqCX9GsLyyaRyUzsLNmHyNWCuXBQuGjPIThkB8"

intents = discord.Intents.default()
intents.message_content = True  # Required to read message text

client = discord.Client(intents=intents)

JD_list = []


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

    # Replace with the specific Text Channel ID you want to scan
    CHANNEL_ID = 1509088600849911840  # Must be an integer, not a string

    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        print("Channel not found. Check the ID and bot permissions.")
        return

    print(f"Fetching messages from #{channel.name} from the last hour...")

    # Calculate the timestamp for exactly 1 hour ago (timezone-aware)
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)

    # Fetch history; "after" filters messages newer than the given timestamp
    async for message in channel.history(after=one_hour_ago, limit=None):
        #print(f"[{message.created_at}] {message.author}: {message.content}")
        if message.content:
            JD_list.append(message.content)
        if message.attachments:
            for attachment in message.attachments:
                if attachment.filename.endswith('.txt'):
                    try:
                        file_bytes = await attachment.read()
                        file_text = file_bytes.decode('utf-8')
                        JD_list.append(file_text)
                    except Exception as e:
                        print(f"Could not read file: {e}")
                              

    print("Finished fetching messages.")
    await jd_process(JD_list)
    

async def jd_process(JD_list):

    for i in JD_list:
        generate_resume(i)
        time.sleep(1)
        name = await html_to_pdf()
        gc = gspread.service_account(filename='credentials.json')
        sh = gc.open("job_search_auto")
        worksheet = sh.sheet1
        new_row_data = [str(i), name]
        worksheet.append_row(new_row_data)


client.run(TOKEN)
