import pygame
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, GiftEvent
import concurrent.futures 
from helper import utils, config
import objs

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(config.MUSIC_SOUND_PATH) 
pygame.mixer.music.play(-1,0.0)
pygame.mixer.music.set_volume(0.1)



# ===================================================
tiktokEvents:list[int] = []
votesA = 1
votesB = 1
def reset_votes():
    global votesA, votesB, tiktokEvents
    tiktokEvents = []
    votesA = 1
    votesB = 1

wyr = objs.WYR()

# ===================================================
pygame.time.set_timer(config.CustomEvent.start, 20_000)
# pygame.time.set_timer(config.CustomEvent.timer, 7_000,)
# pygame.time.set_timer(config.CustomEvent.end, 9_000,)

# ===================================================

def game():
    global votesA, votesB, tiktokEvents
    
    bg = pygame.image.load(config.BG_TEMPLATE_PATH)
    bg = pygame.transform.scale(bg, (config.WIDTH, config.HEIGHT))
    
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

    running = True
    while running:
        
        if len(tiktokEvents) > 0 and not wyr.is_paused:
            print(f" events:{len(tiktokEvents)} votesA:{votesA} votesB:{votesB}")
            wyr.donate_event(votesA, votesB)
            tiktokEvents.pop()
            
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == config.CustomEvent.start:
                pygame.time.set_timer(config.CustomEvent.timer, 15_000, loops=1)
                pygame.time.set_timer(config.CustomEvent.end, 19_000, loops=1)
                reset_votes()
                wyr.start_event()
            if event.type == config.CustomEvent.timer:
                wyr.timer_event()
            if event.type == config.CustomEvent.end:
                wyr.end_event()
            
        screen.blit(bg, (0,0))
        wyr.draw(screen)
        pygame.display.flip()

    pygame.quit()





client: TikTokLiveClient = TikTokLiveClient(unique_id="@mia_asmr_planet")

class GiftId:
    rose = 5655
    tiktok = 5269

@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID:", client.room_id)

@client.on("gift")
async def on_gift(event:GiftEvent):
    global votesA, votesB, tiktokEvents
    
    if event.gift.streakable and not event.gift.streaking:
        # print(f"{event.user.nickname} x{event.gift.count} {event.gift.info.name}")
        
        if event.gift.id == GiftId.rose:
            votesA += event.gift.count
            tiktokEvents.append(0)
        if event.gift.id == GiftId.tiktok:
            votesB += event.gift.count
            tiktokEvents.append(0)


if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor() as executor:
        game_future = executor.submit(game)
        client_future = executor.submit(client.run)
        
    # game()
    # client.run()
