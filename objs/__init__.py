
import pygame
from helper import utils, config
import random



class Text:
    
    def __init__(self, text:str, center:tuple[int,int], font_size:int=32) -> None:
        self.font_size:int = font_size
        self.text:str = self.__wrap_text(text)
        self.font:str = pygame.font.Font(config.FONT_PATH, font_size)
        self.render:pygame.Surface = self.font.render(text, True, (0,0,0), (255,255,255))
        self.rect:pygame.Rect = self.render.get_rect()
        self.rect.center = center
        
    def update(self, text, center):
        self.text:str = self.__wrap_text(text)
        self.render:pygame.Surface = self.font.render(text, True, (0,0,0), (255,255,255))
        self.rect:pygame.Rect = self.render.get_rect()
        self.rect.center = center
        
    def draw(self, screen:pygame.Surface):
        screen.blit(self.render, self.rect)
        
    def __wrap_text(self, text:str)->str:
        words:list[str] = text.split(" ")
        max_char_count = int(config.WIDTH*0.75/self.font_size)
        char_count = 0
        n_text:str = ""
        for word in words:
            if char_count >= max_char_count:
                n_text += word+" \n"
            n_text += word+" "
            
        return n_text
        
        
class Prompt:
    
    def __init__(self, img_src:str, is_top:bool) -> None:
        self.img_src = img_src
        self.perc:int = 50
        
        if is_top:
            self.bg_rect = pygame.Rect(0, 0, config.WIDTH, config.HEIGHT//2)
            self.bg_color = pygame.Color(150, 0, 0)
        else:
            self.bg_rect = pygame.Rect(0, config.HEIGHT//2, config.WIDTH, config.HEIGHT//2)
            self.bg_color = pygame.Color(0, 0, 150)
            
        self.main_text = Text("Prompt " + ("A" if is_top else "B"), self.bg_rect.center)
        self.perc_text = Text(f"%{self.perc}", self.bg_rect.center)

    def set_perc(self, perc:int):
        self.perc= perc
        self.perc_text.update(f"%{self.perc}", self.bg_rect.center)

    def reset(self, text:str):
        self.perc = 50
        self.main_text.update(text, self.bg_rect.center)
        self.perc_text.update(f"%{self.perc}", self.bg_rect.center)

    def draw(self, screen:pygame.Surface):
        pygame.draw.rect(screen, self.bg_color, self.bg_rect, 0)
        self.main_text.draw(screen)
        self.perc_text.draw(screen)
        


wyr_texts = utils.read_json(config.WYRS_PATH)

class WYR:
    
    def __init__(self) -> None:
        self.votesA = 1
        self.votesB = 1
        self.prompt1:Prompt = Prompt(img_src="", is_top=True)
        self.prompt2:Prompt = Prompt(img_src="", is_top=False)
        
        self.start_sound = pygame.mixer.Sound(config.START_SOUND_PATH)
        self.timer_sound = pygame.mixer.Sound(config.TIMER_SOUND_PATH)
        self.end_sound = pygame.mixer.Sound(config.END_SOUND_PATH)

    def update_votes(self, votesA:int, votesB:int):
        total = votesA+votesB
        self.prompt1.set_perc(int(votesA/total*100))
        self.prompt2.set_perc(int(votesB/total*100))
    
    def start_event(self):
        self.__reset_prompt()
        self.__reset_votes()
        self.start_sound.play()

    def timer_event(self):
        self.timer_sound.play()
        
    def end_event(self):
        self.end_sound.play()
        
    def draw(self, screen:pygame.Surface):
        self.prompt1.draw(screen)
        self.prompt2.draw(screen)
                
    def __reset_prompt(self):
        wyr_text = random.choice(wyr_texts)
        self.prompt1.reset(wyr_text["option_a"])
        self.prompt2.reset(wyr_text["option_b"])
        
    def __reset_votes(self):
        self.votesA = 1
        self.votesB = 1