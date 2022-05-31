import pygame
import pytmx
import pyscroll

from player import Player

class Game:
    def __init__(self):
        # cree la fenetre de jeux
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Pygame - Aventure")
        #charger la carte TMX
        tmx_data = pytmx.util_pygame.load_pygame('games/carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        #generer un jpueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)
        #defenir une listes des rectangle des collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        #dessiner le goupe de calc
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # defenir le rectangle de entrer dans la maison
        enter_house = tmx_data.get_object_by_name("enter_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)


    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.mov_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.mov_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            self.player.mov_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.mov_right()
            self.player.change_animation('right')

    def switch_house(self):
        # charger la carte TMX
        tmx_data = pytmx.util_pygame.load_pygame('games/house.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # defenir une listes des rectangle des collision
        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le goupe de calc
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # defenir le rectangle de entrer dans la maison
        enter_house = tmx_data.get_object_by_name("exit_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)
        #recuperer le point de spawn de la maison
        spawn_house_point = tmx_data.get_object_by_name('spawn_house')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 10


    def switch_world(self):
        # charger la carte TMX
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # defenir une listes des rectangle des collision
        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # dessiner le goupe de calc
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # defenir le rectangle de entrer dans la maison
        enter_house = tmx_data.get_object_by_name("enter_house")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        #recuperer le point de spawn devant la maison
        spawn_house_point = tmx_data.get_object_by_name('enter_house_exit')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y + 10


    def update(self):
        self.group.update()
        #verifier l'entree dans la maison
        if self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = 'house'

        #verifier
        if self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()
            self.map = 'world'

        #verif colision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):

        clock = pygame.time.Clock()
        # boucle de jeu
        running = True
        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)
        pygame.quit()