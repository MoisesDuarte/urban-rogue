import tcod as libtcod

# Renderiza todo os elementos de tela
def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
 
    # Desenha todas as tiles do mapa
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight # Array com tiles guardados em gamemap
                
                # Renderização de paredes e chão com base em fov visivel (visible = True)
                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)
                        
                    game_map.tiles[x][y].explored = True # Marca tile como já explorada, a mantendo 'acesa' no mapa
                 
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET) # Definindo o background como tile parede
                    else:  
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET) # Definindo o background como tile chão
            
    # Desenha todas as entidades da lista entities com draw_entity   
    for entity in entities:
        draw_entity(con, entity, fov_map) 
          
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0) # 'Leva' as mudanças para tela
    
# Limpar as entidades depois de coloca-las na tela (para que elas se movam sem deixar um rastro)
def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)
  
# Desenha a entidade      
def draw_entity(con, entity, fov_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color) # Definindo a cor da entidade
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE) # Desenhando no console as coordenadas x e y, com background vazio
    
# Apaga o caracter que representa esse objeto (no caso, seu rastro)
def clear_entity(con, entity):
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
