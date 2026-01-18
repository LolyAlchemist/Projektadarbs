
class SelectNumber:
    def __init__(self, pygame, font):
        self.pygame = pygame
        self.btn_w = 80
        self.btn_h = 80
        self.my_font = font
        self.selected_number = 0 

        self.color_selected = (0,170,255)
        self.color_normal = (0, 0, 0)

        self.btn_positions = [(800,50), (890,50),
                              (800,150), (890,150),
                              (800,250), (890,250),
                              (800,350), (890,350),
                              (800,450)]

        
    
    def draw(self,pygame,surface):
        for index, pos in enumerate(self.btn_positions):
            pygame.draw.rect(surface, self.color_normal, [pos[0], pos[1], self.btn_w, self.btn_h], width=3, border_radius = 10)

            if self.button_hover(pos):
                pygame.draw.rect(surface, self.color_selected, [pos[0], pos[1], self.btn_w, self.btn_h], width=3, border_radius=10)
            
                text_surface = self.my_font.render(str(index + 1), False, (0,170,255))
            else:
                
                text_surface = self.my_font.render(str(index + 1), False, self.color_normal)
                
            if self.selected_number > 0:
                if self.selected_number - 1 == index:
                    pygame.draw.rect(surface, self.color_selected, [pos[0], pos[1], self.btn_w, self.btn_h], width=3, border_radius=10)
                    text_surface = self.my_font.render(str(index + 1), False, self.color_selected)
                    


            surface.blit(text_surface, (pos[0] + 30, pos[1] + 26))
    

    def button_clicked(self, mouse_x:int, mouse_y:int) -> None:
        for index, pos in enumerate(self.btn_positions):
            if self.on_button(mouse_x, mouse_y, pos):
                self.selected_number = index + 1
    



    def button_hover(self, pos: tuple) -> bool|None:
        mouse_pos = self.pygame.mouse.get_pos()
        if self.on_button(mouse_pos[0], mouse_pos[1], pos):
            return True
    
    def on_button(self, mouse_x:int , mouse_y:int, pos:tuple) -> bool:
        return pos[0] < mouse_x < pos[0] + self.btn_w and pos[1] < mouse_y < pos[1] + self.btn_h
          
