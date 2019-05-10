from random import randint

from map_objects.rectangle import Rect
from map_objects.tile import Tile

class GameMap:
    # Uma classe para inicialização de mapa
    
    def __init__(self, width, height):
        self.width = width # Largura do mapa
        self.height = height # Altura do mapa
        self.tiles = self.initialize_tiles() # Array de tiles do mapa
        
    # Inicialização de um array de mapas
    def initialize_tiles(self):
        # Array com primeira linha tiles em coordenada y (altura) e segunda linha tiles em coordenada x (largura)
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)] # Tiles em True = Bloqueadas por padrão
        
        return tiles
    
    # Gerador de mapa (cavocando salas em um mapa totalmente sólido)
    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player):
        rooms = [] # Lista das salas geradas
        num_rooms = 0 # Guarda número de salas no mapa
        
        # Randomizando o tamanho das salas
        for r in range(max_rooms):
            # Altura e largura aleatoria
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # Posição aleatoria sem sair dos limites do mapa
            x = randint(0, map_width - w - 1)      
            y = randint(0, map_height - h - 1)
            
            new_room = Rect(x, y, w, h) # Objeto que irá representar a nova sala
            
            # Checagem de interseção
            for other_room in rooms: # Se o loop for não der 'break', então a sala será criada
                if new_room.intersect(other_room):
                    break
            else:
                # Não há interseções, então a sala é valida
                
                # 'Pintar' a sala nos tiles do mapa (nesse caso, cavocar)
                self.create_room(new_room)
                
                # Centraliza as coordenadas x e y da sala
                (new_x, new_y) = new_room.center()
                
                # Checagem de sala inicial
                if num_rooms == 0:
                    # Centraliza o jogador na sala inicial
                    player.x = new_x
                    player.y = new_y
                else:
                    # Todas as salas além da inicial
                    # Conectar a sala anterior com um tunel
                    
                    # Centralizar as coordenadas da sala anterior
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    
                    # Cara ou coroa (1 ou 0)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                        
                rooms.append(new_room)
                num_rooms += 1
                    
                
    
    # Gerador de salas
    def create_room(self, room):
        # Anda pelas tiles do retangulo e define elas como passaveis (não bloqueadas)
        for x in range(room.x1 + 1, room.x2): # Incremento de 1 para gerar uma parede sólida entre salas
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
                
    # Gerador de tuneis
    # Gera tuneis horizontais
    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
    
    # Gera tuneis verticais
    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
    
    
    # Checa se o tile é bloqueado
    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
 