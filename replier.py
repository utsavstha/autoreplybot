import os
import sys
import time
from collections import defaultdict
from telethon import functions, types
from telethon.sessions import StringSession

from telethon import TelegramClient, events

import logging
logging.basicConfig(level=logging.WARNING)

# "When did we last react?" dictionary, 0.0 by default
recent_reacts = defaultdict(float)


def get_env(name, message, cast=str):
    if name in os.environ:
        return os.environ[name]
    while True:
        value = input(message)
        try:
            return cast(value)
        except ValueError as e:
            print(e, file=sys.stderr)
            time.sleep(1)


def can_react(chat_id):
    # Get the time when we last sent a reaction (or 0)
    last = recent_reacts[chat_id]

    # Get the current time
    now = time.time()

    # If 10 minutes as seconds have passed, we can react
    if now - last < 10 * 60:
        # Make sure we updated the last reaction time
        recent_reacts[chat_id] = now
        return True
    else:
        return False


# Register `events.NewMessage` before defining the client.
# Once you have a client, `add_event_handler` will use this event.
@events.register(events.NewMessage)
async def handler(event):
    # We can also use client methods from here
    client = event.client
   
        # if can_react(event.chat_id):

    await event.respond(r'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus id ante fringilla, porta est vitae, auctor erat. Vivamus ut mattis nisl. Vestibulum ultrices orci non urna fermentum, ac sodales mauris posuere. Suspendisse viverra lacus et ipsum laoreet tincidunt. Etiam nisi ex, posuere vel sapien posuere, ultricies suscipit ex. Mauris quis elementum nisl, vel tincidunt ipsum. Praesent scelerisque elit eu turpis dapibus, sed efficitur urna sagittis.')
    # await event.send_file('files/sample.mp3')
    await client.send_file(event.chat_id, 'files/sample.mp3',voice_note=True)
    await client.send_file(event.chat_id, 'files/image.jpg')
    await client.send_file(event.chat_id, 'files/dummy.pdf')
    await client.send_file(event.chat_id, 'files/test.txt')
    sender = await event.get_sender()

    # result = await client(functions.contacts.BlockRequest(
    #                 id=sender
    #             ))

client = TelegramClient(
    StringSession('1BVtsOHcBuxadomCjJ3MIbYQ077Q3r0MUntPPynRoNE8tXIoqwNcfvGXh2XbblKUi40z2VZTgEuLU1JVUh9WFMgMooQ8_DnswOAovBr1BY6ZNgGlG4l-u6jDJK1I6RQNAF-TxO3UExDOsxO630JfzFv0fSKFnGQNdXDVNx0xpxElgvjan3y-kboaAELXfv6SL-cx6dcORsW2FB9ctQAOkoEccEcwxPkZ6HYlWHNXnhCf7L5QgofnK0bE3XHf38KVHKzf9mFTYxOOTlH19PYlMpWipiPbpjZQjETLzu5iwVH08hg-eCtnaJX5nrJJFGzHTyrhYsEFCd_RGGCm--RN4MyGBhI7xonQ='),
    27172087,
    "3a160707c6d92a576f4224cc322b731e",
    proxy=None
)

with client:
    # This remembers the events.NewMessage we registered before
    client.add_event_handler(handler)
    print(client.session.save())
    print('(Press Ctrl+C to stop this)')
    client.run_until_disconnected()