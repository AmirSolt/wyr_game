import pygame
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, GiftEvent
import concurrent.futures 

pygame.init()

def game():
    # Set up the drawing window
    screen = pygame.display.set_mode([500, 500])

    # Run until the user asks to quit
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        pygame.display.flip()

    pygame.quit()

client: TikTokLiveClient = TikTokLiveClient(unique_id="@ben_toye")

@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)


@client.on("gift")
async def on_gift(event: GiftEvent):
    # Streakable gift & streak is over
    if event.gift.streakable and not event.gift.streaking:
        print(f"{event.user.unique_id} sent {event.gift.count}x \"{event.gift.info.name}\"")

    # Non-streakable gift
    elif not event.gift.streakable:
        print(f"{event.user.unique_id} sent \"{event.gift.info.name}\"")



# async def on_comment(event: CommentEvent):
#     print(f"{event.user.nickname} -> {event.comment}")

# client.add_listener("comment", on_comment)

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor() as executor:
        game_future = executor.submit(game)
        client_future = executor.submit(client.run)

    # You can also handle the results if needed
    # game_res = game_future.result()
    # client_res = client_future.result()