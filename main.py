import pygame
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, GiftEvent
import concurrent.futures 
from helper import utils, config
import objs

pygame.init()

# ===================================================

wyr = objs.WYR()

# ===================================================
pygame.time.set_timer(config.CustomEvent.start, 10_000)
pygame.time.set_timer(config.CustomEvent.timer, 7_000)
pygame.time.set_timer(config.CustomEvent.end, 9_000)

# ===================================================

def game():
    screen = pygame.display.set_mode([config.WIDTH, config.HEIGHT])

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == config.CustomEvent.start:
                wyr.start_event()
            if event.type == config.CustomEvent.timer:
                wyr.timer_event()
            if event.type == config.CustomEvent.end:
                wyr.end_event()

        screen.fill((0, 0, 0))
        wyr.draw(screen)
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


if __name__ == '__main__':
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     game_future = executor.submit(game)
    #     client_future = executor.submit(client.run)
        
    game()
