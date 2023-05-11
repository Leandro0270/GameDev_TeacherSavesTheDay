import pygame

class student:
    def __init__(self, x, y, speed, image):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.following_player = True
        self.run_direction = None

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.topleft = (self.x, self.y)

    def follow_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance > 0:
            self.move(dx / distance, dy / distance)

    def run_away(self, player):
        dx = self.x - player.x
        dy = self.y - player.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance > 0:
            self.move(dx / distance, dy / distance)

    def collide_with_player(self, player):
        return self.rect.colliderect(player.rect)

    def update(self, player):
        if self.following_player:
            self.follow_player(player)
        else:
            self.run_away(player)
            if self.collide_with_player(player):
                self.following_player = True

    def panic(self):
        self.following_player = False

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)