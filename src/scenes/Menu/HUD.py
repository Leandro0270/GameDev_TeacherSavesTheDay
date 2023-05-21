import pygame

class HUD:
    def __init__(self, player, total_items, objective, surface):
        self.player = player
        self.total_items = total_items
        self.items_collected = 0
        self.objective = objective
        self.surface = surface
        self.font = pygame.font.Font(None, 36)  # Use a fonte desejada aqui

    def draw_objective(self):
        objective_text = self.font.render(f"Objective: {self.objective}", True, (0, 0, 0))
        self.surface.blit(objective_text, (10, 10))  # Posiciona no canto superior esquerdo

    def draw_life(self):
        life_text = self.font.render(f"Life: {self.player.life}", True, (255, 13, 13))
        self.text_rect = life_text.get_rect(topright=(self.surface.get_width() - 10, 10))  # Posiciona no canto superior direito
        self.surface.blit(life_text, self.text_rect)

    def draw_items(self):
        items_text = self.font.render(f"Items: {self.items_collected}/{self.total_items}", True, (13, 37, 255))
        # Posiciona abaixo do texto da vida, no canto superior direito
        text_rect = items_text.get_rect(topright=(self.surface.get_width() - 10, self.text_rect.bottom + 10))
        self.surface.blit(items_text, text_rect)

    def update(self):
        self.draw_objective()
        self.draw_life()
        self.draw_items()

    def item_collected(self):
        self.items_collected += 1


