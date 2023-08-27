
import pygame
from helper import utils, config
import random

wyr_texts = utils.read_json(config.WYRS_PATH)
wyr_index = 0

class Text:
    
    def __init__(self, text:str, center:tuple[int,int], font_size:int=32, color:tuple[int,int,int]=(0,0,0), bg_color:tuple[int,int,int]=(255,255,255)) -> None:
        self.color = color 
        self.bg_color = bg_color 
        
        self.font_size:int = font_size
        self.font:pygame.font.Font = pygame.font.Font(config.FONT_PATH, font_size)
        
        self.text:str = text
        self.target_center:tuple[int,int] = center
        
        self.labels:list[pygame.Surface] = self.__get_labels(text)
        self.label_rects:list[pygame.Rect] = self.__get_rects()
    
    def set_font_size(self, font_size:int):
        self.font_size = font_size
        self.font:pygame.font.Font = pygame.font.Font(config.FONT_PATH, font_size)
        self.labels:list[pygame.Surface] = self.__get_labels(self.text)
        self.label_rects:list[pygame.Rect] = self.__get_rects()
    
    def update(self, text:str, color:tuple[int,int,int]=(0,0,0), bg_color:tuple[int,int,int]=(255,255,255) ):
        self.text:str = text
        self.color = color 
        self.bg_color = bg_color
        self.labels:list[pygame.Surface] = self.__get_labels(text)
        self.label_rects:list[pygame.Rect] = self.__get_rects()
        
    def draw(self, screen:pygame.Surface):
        for label, label_rect in zip(self.labels, self.label_rects):
            screen.blit(label, label_rect)
        
        
    def __get_labels(self, text:str)->list[pygame.Surface]:
        words:list[str] = text.split(" ")
        max_char_count = int(config.WIDTH*0.75/self.font_size)
        char_count = 0
        n_text:str = ""
        for word in words:
            char_count += len(word)
            if char_count >= max_char_count:
                n_text += word+" \n"
                char_count = 0
            else:
                n_text += word+" "
            
        n_labels:list[pygame.Surface] = [
            self.font.render(t, True, self.color, self.bg_color)
            for t in n_text.split("\n")]
            
        return n_labels
    
    def __get_rects(self)->list[pygame.Rect]:
        def func(n):
            if n % 2 == 0: 
                return [(x-n/2+.5) for x in range(n)]
            else:
                return [(x -n//2) for x in range(n)]
            
        rects = [label.get_rect() for label in self.labels]
        cx, cy = self.target_center
        multipliers = func(len(rects))
        for rect, m in zip(rects, multipliers):
            rect.center = (cx, cy+(rect.h*m))
        return rects
        
class Image:
    
    def __init__(self, src:str, center:tuple[int,int]) -> None:
        self.surface = pygame.image.load(src)
        self.rect = self.surface.get_rect() 
        self.rect.center = center

class Prompt:
    
    main_text_font_size = 50
    perc_font_size = 80
    perc_bloated_font_size = 100
    
    def __init__(self, img_src:str, is_top:bool) -> None:
        self.perc:int = 50
        
        if is_top:
            self.rect = pygame.Rect(0, 0, config.WIDTH, config.HEIGHT//2)
            dono_img_center = (self.rect.x + self.rect.w*0.16, self.rect.y + self.rect.h*0.57)
            main_text_center = (self.rect.x + self.rect.w*0.6, self.rect.y + self.rect.h*0.5)
            perc_text_center = (self.rect.x + self.rect.w*0.16, self.rect.y + self.rect.h*0.8)
        else:
            self.rect = pygame.Rect(0, config.HEIGHT//2, config.WIDTH, config.HEIGHT//2)
            dono_img_center = (self.rect.x + self.rect.w*0.16, self.rect.y + self.rect.h*0.43)
            main_text_center = (self.rect.x + self.rect.w*0.6, self.rect.y + self.rect.h*0.5)
            perc_text_center = (self.rect.x + self.rect.w*0.16, self.rect.y + self.rect.h*0.2)
            
        
        self.dono_img = Image(img_src, dono_img_center)
        self.main_text = Text("Prompt " + ("A" if is_top else "B"), main_text_center, font_size=self.main_text_font_size)
        self.perc_text = Text(f"%{self.perc}", perc_text_center, font_size=self.perc_font_size)

    def bloat_perc(self):
        self.perc_text.set_font_size(self.perc_bloated_font_size)
            
    def debloat_font_size(self):
        self.perc_text.set_font_size(self.perc_font_size)

    def set_perc(self, perc:int):
        self.perc= perc
        color = (0,0,0)
        if perc > 50:
            color = (0, 255, 0)
        if perc < 50:
            color = (255, 0, 0)
        self.perc_text.update(f"%{self.perc}", color=color)

    def reset(self, text:str):
        self.perc = 50
        self.main_text.update(text)
        self.perc_text.update(f"%{self.perc}")

    def draw(self, screen:pygame.Surface):
        screen.blit(self.dono_img.surface, self.dono_img.rect.topleft)
        self.main_text.draw(screen)
        self.perc_text.draw(screen)
        
class WYR:
    
    def __init__(self) -> None:
        self.prompt1:Prompt = Prompt(img_src=config.DONO_FLOWER_PATH, is_top=True)
        self.prompt2:Prompt = Prompt(img_src=config.DONO_TIKTOK_PATH, is_top=False)
        self.is_paused:bool = False
        self.start_sound = pygame.mixer.Sound(config.START_SOUND_PATH)
        self.start_sound.set_volume(0.3)
        self.dono_sound = pygame.mixer.Sound(config.DONO_SOUND_PATH)
        self.timer_sound = pygame.mixer.Sound(config.TIMER_SOUND_PATH)
        self.end_sound = pygame.mixer.Sound(config.END_SOUND_PATH)

    def update_votes(self, votesA:int, votesB:int):
        total = votesA+votesB
        self.prompt1.set_perc(int(votesA/total*100))
        self.prompt2.set_perc(int(votesB/total*100))

    
    
    def start_event(self):
        self.is_paused = False
        self.__reset_prompt()
        self.prompt1.debloat_font_size()
        self.prompt2.debloat_font_size()
        self.start_sound.play()

    def donate_event(self, votesA:int, votesB:int):
        self.update_votes(votesA, votesB)
        self.dono_sound.play()
        
    def timer_event(self):
        self.timer_sound.play()
        
    def end_event(self):
        self.is_paused = True
        if self.prompt1.perc > 50:
            self.prompt1.bloat_perc()
        if self.prompt2.perc > 50:
            self.prompt2.bloat_perc()
        self.end_sound.play()
  
        
    def draw(self, screen:pygame.Surface):
        
        self.prompt1.draw(screen)
        self.prompt2.draw(screen)
                
    def __reset_prompt(self):
        global wyr_index
        wyr_index = wyr_index%len(wyr_texts)
        wyr_text = wyr_texts[wyr_index]
        self.prompt1.reset(wyr_text["option_a"])
        self.prompt2.reset(wyr_text["option_b"])
        wyr_index +=1
        