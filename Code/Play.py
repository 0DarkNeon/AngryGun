# import pygame.draw
import Varis
import random
from Varis import *
pg = pygame

pygame.init()
screen = pygame.display.set_mode((Varis.screen_w, Varis.screen_h))

Arial = pygame.font.SysFont('arial', round(Varis.one * 16))

Bad_move_list = [Varis.one, 0, 0, 0, 0, 0, 0, Varis.one * -1]



class Game:
    def __init__(self):
        # Vars
        self.is_in_game = True
        Varis.for_but_is_click = False
        self.tick = 0

        # Pers Vars
        self.Pers_Icon = Varis.Pers_Icon
        self.Pers_curr_icon = self.Pers_Icon.copy()
        self.Pers = Pers(self.Pers_Icon)
        self.Pers_group = pygame.sprite.Group()
        self.Pers_group.add(self.Pers)
        self.Pers_speed = Varis.one

        # Pers weapon
        self.Pers_weapon_icon = Varis.Pers_all_weapon_list[Varis.Pers_current_weapon_info_list[1]][Varis.Select_pers_list_index[Varis.Pers_current_weapon_info_list[1]]][0]
        self.Pers_weapon = Pers_weapon(Varis.Pers_current_weapon_info_list[0])
        self.Pers_weapon_group = pygame.sprite.Group()
        self.Pers_weapon_group.add(self.Pers_weapon)


        # Pers Melee weapon
        self.Pers_melee_icon = Varis.Laser_Sword_Normal_Icon

        self.Laser_sword_icon = Varis.Laser_Sword_Normal_Icon
        self.Fire_whip_icon = Varis.Fire_Whip_Normal_Icon
        self.Holy_hammer_icon = Varis.Holy_Hammer_Icon


        # Pers Gun

        self.Pers_gun_icon = Varis.Minigun_Norm_Icon
        Varis.gun_info_scale_koef = Varis.gun_info_size[0] / self.Pers_gun_icon.get_rect()[2] * 0.8
        self.Weapon_info_icon_size = [round(self.Pers_gun_icon.get_rect()[2] * Varis.gun_info_scale_koef), round(self.Pers_gun_icon.get_rect()[3] * Varis.gun_info_scale_koef)]
        Varis.Bullet_group = pygame.sprite.Group()

        # Minigun Vars
        self.Minigun_icon = Varis.Gun_list[0][0]
        # self.Minigun_bullets = pygame.sprite.Group()
        self.Minigun_can_shot = True
        self.Minigun_power = 0

        # Shotgun Vars
        self.Shotgun_icon = Varis.Gun_list[1][0]
        # self.Shotgun_bullets = pygame.sprite.Group()
        self.Shotgun_can_shot = True
        self.Shotgun_shot_count = 0

        # Flame Thrower Vars
        self.FThrower_icon = Varis.Gun_list[2][0]
        # self.Flame_bullets = pygame.sprite.Group()
        self.FThrower_can_shot = True

        # WTF Gun Vars
        self.WTF_Gun_icon = Varis.Gun_list[3][0]
        self.WTF_Gun_can_shot = True

        self.Pers_gun_icon_list = [self.Minigun_icon, self.Shotgun_icon, self.FThrower_icon, self.WTF_Gun_icon]
        self.Pers_melee_icon_list = [self.Laser_sword_icon, self.Fire_whip_icon, self.Holy_hammer_icon]
        self.Pers_weapon_icon_list = [self.Pers_gun_icon_list, self.Pers_melee_icon_list]

        # Objects
        Varis.Hard_Objects_group = pygame.sprite.Group()

        # Enemy
        Varis.Enemy_group = pygame.sprite.Group()


    @staticmethod
    def EXIT():
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    @staticmethod
    def give_font(size):
        return pygame.font.SysFont('arial', size)

    @staticmethod
    def draw_text_cen(text, cen, font, color):
        text_draw = font.render(text, False, color)
        rect = text_draw.get_rect(center=cen)
        screen.blit(text_draw, rect)

    @staticmethod
    def draw_text_pos(text, pos, font, color):
        text_draw = font.render(text, False, color)
        screen.blit(text_draw, text_draw.get_rect(lefttop=pos))

    @staticmethod
    def game_generate():


        is_pers = False
        while not is_pers:
            for x_line in range(len(Varis.empty_grid_matrix)):
                for this_tile in range(len(Varis.empty_grid_matrix[x_line])):
                    if random.randint(0, 50) == 7 and Varis.empty_grid_matrix[x_line][this_tile]:
                        pers_gen_tile = Varis.empty_grid_matrix[x_line][this_tile]
                        # print(pers_gen_tile)
                        Varis.pers_pos = [pers_gen_tile[0] + Varis.block / 2, pers_gen_tile[1] + Varis.block / 2]
                        is_pers = True

        enemy_count = 0
        while not enemy_count >= 5:
            for x_line in range(len(Varis.empty_grid_matrix)):
                for this_tile in range(len(Varis.empty_grid_matrix[x_line])):
                    if random.randint(0, 50) == 7 and Varis.empty_grid_matrix[x_line][this_tile]:
                        enemy_gen_tile = Varis.empty_grid_matrix[x_line][this_tile]
                        Varis.Enemy_group.add(Stone_warrior(Varis.Stone_Warrior_Icon, Varis.Stone_warrior_size, enemy_gen_tile[0], enemy_gen_tile[1]))
                        enemy_count += 1

    @staticmethod
    def rotate_pers_gun():
        mouse_pos = pygame.mouse.get_pos()
        angle = math.atan2(mouse_pos[1] - Varis.pers_cen[1] - Varis.pers_size[1], mouse_pos[0] - Varis.pers_cen[0] - Varis.pers_size[1])

        Varis.pers_weapon_angle = angle
        if Varis.Select_weapon_id != Varis.Gun_list[-1][2]:
            Varis.pers_weapon_image_angle = angle


    def draw_game(self):
        # Time
        self.tick += 1
        if self.tick > Varis.max_tick:
            self.tick = 0


        # if Varis.Pers_current_weapon_info_list[1] != 1 or Varis.Is_pers_melee_can_attack:
        self.rotate_pers_gun()

        """
        if Varis.pers_weapon_angle < 0:
            Varis.pers_weapon_angle += 360
        if Varis.pers_weapon_image_angle < 0:
            Varis.pers_weapon_image_angle += 360
        """

        Varis.WTF_Bullet_info_list[0] = random.randint(0, 100) / 10


        # Game place draw
        screen.fill(Varis.BLACK)

        Varis.Pers_all_weapon_list[Varis.Pers_current_weapon_info_list[1]][Varis.Select_pers_list_index[Varis.Pers_current_weapon_info_list[1]]][0] = self.Pers_weapon_icon

        Varis.Enemy_group.draw(screen)

        Varis.Hard_Objects_group.draw(screen)
        if Varis.Flame_Bullets:
            Varis.Flame_Bullets.draw(screen)
        if Varis.WTF_Bullets:
            Varis.WTF_Bullets.draw(screen)
        if Varis.Bullet_group:
            Varis.Bullet_group.draw(screen)
        self.Pers_weapon_group.draw(screen)
        self.Pers_group.draw(screen)


        Varis.draw_rect_points(screen, self.Pers_weapon.rect, Varis.is_draw_collide_points)

        for enemy in Varis.Enemy_group:
            if Varis.Pers_current_weapon_info_list[1] == 1 and not Varis.Is_pers_melee_can_attack and enemy.can_be_hurt_by_melee and pygame.sprite.collide_mask(self.Pers_weapon, enemy):
                enemy.hp -= max(Varis.Melee_weapon_info_list[Varis.Select_pers_list_index[1]][0] - enemy.defence, 0)
                enemy.can_be_hurt_by_melee = False
            screen.blit(enemy.hp_text, enemy.hp_text_rect)


        # for x in range(0, Varis.game_screen_w, Varis.block * 2):
        #    for y in range(0, Varis.game_screen_h, Varis.block * 2):
        #        pygame.draw.rect(screen, (0, 60, 60), (x, y, Varis.block * 2, Varis.block * 2), 2)

        # Game data info draw
        pygame.draw.rect(screen, Varis.GREY50, (Varis.game_screen_w, 0, Varis.screen_w - Varis.game_screen_w, Varis.game_screen_h))
        # Gun info draw
        pygame.draw.rect(screen, Varis.BLACK, (Varis.gun_info_pos[0], Varis.gun_info_pos[1], Varis.gun_info_size[0], Varis.gun_info_size[1]), 0, round(Varis.tile / 2))
        Pers_weapon_info_icon = pygame.transform.scale(self.Pers_weapon_icon, (round(self.Weapon_info_icon_size[0]), round(self.Weapon_info_icon_size[1])))
        screen.blit(Pers_weapon_info_icon, (Pers_weapon_info_icon.get_rect(center=Varis.gun_info_cen)[0], Pers_weapon_info_icon.get_rect(center=Varis.gun_info_cen)[1]))
        pygame.draw.rect(screen, Varis.GREY50, (Varis.game_screen_w, 0, Varis.gun_info_pos[0], Varis.gun_info_pos[1] + round(Varis.one * 4)))
        pygame.draw.rect(screen, Varis.GREY50, (Varis.game_screen_w, Varis.gun_info_pos[1] + Varis.gun_info_size[1] - round(Varis.one * 4), Varis.gun_info_pos[0], Varis.game_screen_h - Varis.gun_info_pos[1] - Varis.gun_info_size[1] + round(Varis.one * 4)))
        pygame.draw.rect(screen, Varis.GREY50, (Varis.game_screen_w, Varis.gun_info_pos[1], Varis.gun_info_pos[1] + round(Varis.one * 4), Varis.gun_info_size[1]))
        pygame.draw.rect(screen, Varis.GREY50, (Varis.gun_info_pos[0] + Varis.gun_info_size[0] - round(Varis.one * 4), Varis.gun_info_pos[1], Varis.gun_info_pos[1] + round(Varis.one * 4), Varis.gun_info_size[1]))

        self.draw_text_cen(Varis.Pers_all_weapon_list[Varis.Pers_current_weapon_info_list[1]][Varis.Select_pers_list_index[Pers_current_weapon_info_list[1]]][1], (Varis.gun_info_cen[0], Varis.gun_info_cen[1] + round(Varis.data_dis_block * 1.5)), self.give_font(round(Varis.data_dis_block / 1.5)), Varis.BLACK)
        pygame.draw.rect(screen, Varis.GREY200, (Varis.gun_info_pos[0], Varis.gun_info_pos[1], Varis.gun_info_size[0], Varis.gun_info_size[1]), round(Varis.tile / 2), round(Varis.tile / 2))

        # Buttons draw
        for q in range(len(Varis.dd_but_pos)):
            pygame.draw.rect(screen, Varis.dd_but_color[q], (Varis.dd_but_pos[q][0], Varis.dd_but_pos[q][1], Varis.data_dis_block, Varis.data_dis_block), round(max(Varis.data_dis_block / 10, 5)), round(max(Varis.data_dis_block / 5, 5)))
            pygame.draw.polygon(screen, Varis.dd_but_color[q], Varis.dd_but_triangles_pos[q], 0)

        self.normalize_Vars()

        pygame.display.update()


        # Groups update
        Varis.Hard_Objects_group.update(True)
        self.Pers_group.update((round(Varis.pers_pos[0]), round(Varis.pers_pos[1])))
        # Varis.Bullet_group.update()

        Varis.Enemy_group.update()


        Varis.Minigun_Bullets.update()
        Varis.Shotgun_Bullets.update()
        Varis.Flame_Bullets.update()
        Varis.WTF_Bullets.update()

        self.Pers_weapon_group.update(self.Pers_weapon_icon)

        # Vars update


        Varis.clock.tick(90)


    def Buttons_and_Mouse(self):
        # Get event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.EXIT()

            # Key down one time
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_in_game = False
                # Num press events
                """
                elif event.key == pygame.K_1:
                    Varis.Select_weapon_id = 0
                elif event.key == pygame.K_2:
                    Varis.Select_weapon_id = 1
                elif event.key == pygame.K_3:
                    Varis.Select_weapon_id = 2
                elif event.key == pygame.K_0:
                    Varis.Select_weapon_id = 999
                """

            # Mouse actions
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.FINGERDOWN:
                Varis.for_but_is_click = True

                # Change weapon click event
                pressed = pygame.mouse.get_pressed()
                if is_point_in_box(pygame.mouse.get_pos(), (Varis.gun_info_pos[0], Varis.gun_info_pos[1], Varis.gun_info_size[0], Varis.gun_info_size[1])) and (pressed[0] or pressed[1] or pressed[2]):
                    z = 0
                    for boolean in Varis.Weapon_type_select_list:
                        Varis.Weapon_type_select_list[z] = not boolean
                        if Varis.Weapon_type_select_list[z]:
                            Varis.Pers_current_weapon_info_list[1] = z
                        z += 1



                    Varis.Select_weapon_id = Varis.Select_weap_list_of_id[Varis.Pers_current_weapon_info_list[1]][Varis.Select_pers_list_index[Pers_current_weapon_info_list[1]]]
                    """for i in range(len(Varis.Weapon_type_select_list) - 1):
                        if Varis.Weapon_type_select_list[i]:
                            Varis.Pers_current_weapon_info_list[1] = i
                    """

                    Varis.Select_weapon_id = Varis.Select_weap_list_of_id[Varis.Pers_current_weapon_info_list[1]][Varis.Select_pers_list_index[Pers_current_weapon_info_list[1]]]


            elif event.type == pygame.MOUSEBUTTONUP or event.type == pygame.FINGERUP:
                Varis.for_but_is_click = False
                self.Shotgun_icon = Varis.Shotgun_Norm_Icon

        keys = pygame.key.get_pressed()

        # Move event
        if (keys[pygame.K_UP] or keys[pygame.K_w] or (Varis.for_but_is_click and is_point_in_box(pygame.mouse.get_pos(), (Varis.dd_but_pos[1][0], Varis.dd_but_pos[1][1], Varis.data_dis_block, Varis.data_dis_block)))) and Varis.pers_can_go_up:
            self.Pers.pers_move_up()
        elif (keys[pygame.K_DOWN] or keys[pygame.K_s] or (Varis.for_but_is_click and is_point_in_box(pygame.mouse.get_pos(), (Varis.dd_but_pos[3][0], Varis.dd_but_pos[3][1], Varis.data_dis_block, Varis.data_dis_block)))) and Varis.pers_can_go_down:
            self.Pers.pers_move_down()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a] or (Varis.for_but_is_click and is_point_in_box(pygame.mouse.get_pos(), (Varis.dd_but_pos[0][0], Varis.dd_but_pos[0][1], Varis.data_dis_block, Varis.data_dis_block)))) and Varis.pers_can_go_left:
            self.Pers.pers_move_left()
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d] or (Varis.for_but_is_click and is_point_in_box(pygame.mouse.get_pos(), (Varis.dd_but_pos[2][0], Varis.dd_but_pos[2][1], Varis.data_dis_block, Varis.data_dis_block)))) and Varis.pers_can_go_right:
            self.Pers.pers_move_right()

        # Weapon reload time
        if self.tick % (40 - round(self.Minigun_power)) == 0:
            self.Minigun_can_shot = True
        if self.tick % 120 == 0:
            self.Shotgun_can_shot = True
        if self.tick % 2 == 0:
            self.FThrower_can_shot = True
        if self.tick % 20 == 0:
            self.WTF_Gun_can_shot = True

        if Varis.Weapon_type_select_list[0]:

            # Minigun animation
            if self.tick % (40 - round(self.Minigun_power)) == 0 and self.Minigun_power != 0:
                if self.Minigun_icon == Varis.Minigun_Norm_Icon:
                    self.Minigun_icon = Varis.Minigun_Shot_Icon
                elif self.Minigun_icon != Varis.Minigun_Norm_Icon:
                    self.Minigun_icon = Varis.Minigun_Norm_Icon


            # Click in game place
            if pygame.mouse.get_pos()[0] <= Varis.game_screen_w and Varis.for_but_is_click:
                # Guns Animation
                # Minigun Icon
                if Varis.Select_weapon_id == Varis.Gun_list[0][2]:
                    self.Minigun_power = min(self.Minigun_power + 0.16, 35)
                    Varis.gun_info_scale_koef = Varis.gun_info_size[0] / self.Pers_weapon_icon.get_rect()[2] * 0.8

                # Shotgun Animation
                elif Varis.Select_weapon_id == Varis.Gun_list[1][2]:
                    Varis.gun_info_scale_koef = Varis.gun_info_size[0] / self.Pers_weapon_icon.get_rect()[2] * 0.8
                    if self.Shotgun_shot_count == 3:
                        if self.tick == 0:
                            self.Shotgun_icon = Varis.Shotgun_Shot1_Icon
                        elif self.tick == 15:
                            self.Shotgun_icon = Varis.Shotgun_Shot2_Icon
                        elif self.tick == 25:
                            self.Shotgun_icon = Varis.Shotgun_Shot3_Icon
                        elif self.tick == 35:
                            self.Shotgun_icon = Varis.Shotgun_Shot4_Icon
                        elif self.tick == 45 and self.Shotgun_icon == Varis.Shotgun_Shot4_Icon:
                            self.Shotgun_icon = Varis.Shotgun_Norm_Icon
                            self.Shotgun_shot_count = 0

                # Flame Thrower Animation
                elif Varis.Select_weapon_id == Varis.Gun_list[2][2]:
                    Varis.gun_info_scale_koef = Varis.gun_info_size[0] / self.Pers_weapon_icon.get_rect()[2] * 0.8

                # WTF Gun Animation
                elif Varis.Select_weapon_id == Varis.Gun_list[-1][2]:
                    Varis.gun_info_scale_koef = Varis.gun_info_size[0] / self.Pers_weapon_icon.get_rect()[2] * 0.8


                # Gun Shot
                # Minigun Shot
                if Varis.Select_weapon_id == Varis.Gun_list[0][2] and self.Minigun_can_shot:
                    self.Minigun_can_shot = False
                    bullet = self.Pers.create_bullet(Varis.WHITE, 12, (3, 3), random.choice((5, 5, 0, 0, 0, -5, -5)), Varis.block * (9 + self.Minigun_power / 5), 0)
                    Varis.Bullet_group.add(bullet)
                    Varis.Minigun_Bullets.add(bullet)

                # Shotgun shot
                elif Varis.Select_weapon_id == Varis.Gun_list[1][2] and self.Shotgun_can_shot and self.Shotgun_icon == Varis.Shotgun_Norm_Icon and self.Shotgun_shot_count != 3:
                    self.Shotgun_can_shot = False
                    self.Shotgun_shot_count += 1
                    self.Minigun_power = 0
                    for q in range(9):
                        chance = random.choice((True, True, False))
                        if chance:
                            bullet = self.Pers.create_bullet(Varis.YELLOW, 10, (5, 5), (40 - 10 * q), Varis.block * 6, 1)
                            Varis.Bullet_group.add(bullet)
                            Varis.Shotgun_Bullets.add(bullet)

                # Flame Thrower shot
                elif Varis.Select_weapon_id == Varis.Gun_list[2][2] and self.FThrower_can_shot:
                    self.Minigun_power = 0
                    # color, speed, size, path_change, die_distance
                    for q in range(6):
                        select = random.randint(0, 2)
                        # Red flame
                        if select == 0:
                            size = random.randint(2, 8)
                            bullet = self.Pers.create_bullet(Varis.FLAME_BULLET_COLOR_3, 4, (size, size), random.randint(-50, 50) / 100, Varis.block * random.randint(25, 40) / 10, 2)
                            Varis.Bullet_group.add(bullet)
                            Varis.Flame_Bullets.add(bullet)
                        # Orange flame
                        elif select == 1:
                            size = random.randint(4, 10)
                            bullet = self.Pers.create_bullet(Varis.FLAME_BULLET_COLOR_2, 4, (size, size), random.randint(-50, 50) / 100, Varis.block * random.randint(20, 35) / 10, 2)
                            Varis.Bullet_group.add(bullet)
                            Varis.Flame_Bullets.add(bullet)
                        # Yellow flame
                        elif select == 2:
                            size = random.randint(5, 15)
                            bullet = self.Pers.create_bullet(Varis.FLAME_BULLET_COLOR_1, 4, (size, size), random.randint(-30, 30) / 100, Varis.block * random.randint(15, 30) / 10, 2)
                            Varis.Bullet_group.add(bullet)
                            Varis.Flame_Bullets.add(bullet)


                # WTF Gun Shot
                elif Varis.Select_weapon_id == Varis.Gun_list[-1][2] and self.WTF_Gun_can_shot:
                    self.WTF_Gun_can_shot = False
                    # Shot times random count
                    chance = random.randint(0, 1000)
                    if 100 <= chance <= 300:
                        shoots = 2
                    elif 301 <= chance <= 326:
                        shoots = 3
                    elif chance % 200 == 0:
                        shoots = 15
                    else:
                        shoots = 1

                    # Shot
                    for q in range(shoots):
                        width = random.choice((random.randint(4, 30), random.randint(4, 10)))
                        height = random.choice((random.randint(4, 30), random.randint(4, 10)))
                        size = random.choice(((width, width), (height, height), (width, height), (height, width), (math.ceil(width / 2), math.ceil(height * 2)), (math.ceil(width * 2), math.ceil(height / 2))))
                        color_power = random.choice(((Varis.RED, Varis.WTF_Red_Icon), (Varis.ORANGE, Varis.WTF_Orange_Icon), (Varis.YELLOW, Varis.WTF_Yellow_Icon), (Varis.GREEN, Varis.WTF_Green_Icon), (Varis.CYAN, Varis.WTF_Cyan_Icon), (Varis.BLUE, Varis.WTF_Blue_Icon), (Varis.PURPLE, Varis.WTF_Purple_Icon), (Varis.PINK, Varis.WTF_Pink_Icon), (Varis.WHITE, Varis.WTF_White_Icon), (Varis.GREY25, Varis.WTF_Black_Icon)))
                        self.WTF_Gun_icon = color_power[1]
                        bullet = self.Pers.create_bullet(color_power[0], random.randint(10, 100) / 10, size, random.randint(0, 180) / 10, Varis.block * random.randint(50, 150) / 10, 999)
                        Varis.pers_weapon_angle = random.randint(0, 360)

                        Varis.Bullet_group.add(bullet)
                        Varis.WTF_Bullets.add(bullet)

                        # Weapon index select(weapon icon change)

            self.Pers_gun_icon_list = [self.Minigun_icon, self.Shotgun_icon, self.FThrower_icon, self.WTF_Gun_icon]
            self.Pers_weapon_icon_list = [self.Pers_gun_icon_list, self.Pers_melee_icon_list]
            if Varis.Select_weapon_id == Varis.Gun_list[Varis.Select_pers_list_index[0]][2]:
                self.Pers_weapon_icon = self.Pers_weapon_icon_list[Varis.Pers_current_weapon_info_list[1]][Varis.Select_pers_list_index[0]]
                self.Weapon_info_icon_size = [self.Pers_weapon_icon.get_rect()[2] * Varis.gun_info_scale_koef, self.Pers_weapon_icon.get_rect()[3] * Varis.gun_info_scale_koef]


        elif Varis.Weapon_type_select_list[1]:

            if self.tick % Varis.Melee_weapon_list[Varis.Select_pers_list_index[1]][5] and not Varis.Is_pers_melee_can_attack:
                Varis.Melee_weapon_list[Varis.Select_pers_list_index[1]][4] += 1
                if Varis.Melee_weapon_list[Varis.Select_pers_list_index[1]][4] > len(Varis.Melee_weapon_list[Varis.Select_pers_list_index[1]][3]) - 1:
                    Varis.Melee_weapon_list[Varis.Select_pers_list_index[1]][4] = 0

            if Varis.Select_weapon_id == Varis.Melee_weapon_list[Varis.Select_pers_list_index[1]][2]:
                self.Pers_weapon_icon = Varis.Melee_weapon_list[Varis.Select_pers_list_index[1]][3][Varis.Melee_weapon_list[Varis.Select_pers_list_index[1]][4]]
                self.Weapon_info_icon_size = [self.Pers_weapon_icon.get_rect()[2] * Varis.gun_info_scale_koef, self.Pers_weapon_icon.get_rect()[3] * Varis.gun_info_scale_koef]
            #self.Pers_melee_icon_list = [self.Laser_sword_icon, self.Fire_whip_icon, self.Holy_hammer_icon]

            if pygame.mouse.get_pos()[0] <= Varis.game_screen_w and Varis.for_but_is_click:
                if Varis.Is_pers_melee_can_attack:
                    self.Pers_weapon.angle_change_times = Varis.Melee_weapon_info_list[Varis.Select_pers_list_index[1]][3]
                Varis.Is_pers_melee_can_attack = False

            # Fire whip change icon to attack and normal


            icon_index = 0
            if Varis.Is_pers_melee_can_attack:
                icon_index = 0
            elif not Varis.Is_pers_melee_can_attack:
                icon_index = 1
            for q in range(len(self.Pers_melee_icon_list)):
                self.Pers_melee_icon_list[q] = Varis.Melee_weapon_list[Varis.Select_pers_list_index[1]][6][icon_index]

            self.Pers_weapon_icon_list = [self.Pers_gun_icon_list, self.Pers_melee_icon_list]
            self.Pers_weapon_icon = self.Pers_weapon_icon_list[Varis.Pers_current_weapon_info_list[1]][Varis.Select_pers_list_index[Varis.Pers_current_weapon_info_list[1]]]
            self.Weapon_info_icon_size = [self.Pers_weapon_icon.get_rect()[2] * Varis.gun_info_scale_koef, self.Pers_weapon_icon.get_rect()[3] * Varis.gun_info_scale_koef]

        # Vars change
        self.Minigun_power = max(self.Minigun_power - 0.10, 0)

    @staticmethod
    def normalize_Vars():
        Varis.pers_can_go_up = Varis.pers_can_go_down = Varis.pers_can_go_right = Varis.pers_can_go_left = True
        Varis.pers_cen = [Varis.pers_pos[0] - round(Varis.pers_size[0] / 2), Varis.pers_pos[1] - round(Varis.pers_size[1] / 2)]
        Varis.dd_but_color = [Varis.GREY200, Varis.GREY200, Varis.GREY200, Varis.GREY200]


    def in_game(self):
        self.is_in_game = True
        self.game_generate()
        while self.is_in_game:
            self.draw_game()
            self.Buttons_and_Mouse()
        Varis.can_continue = True


#######################################################################################################################
####################################################### CLASSES #######################################################
#######################################################################################################################


#|------------------------------------------------- Pers -------------------------------------------------|
class Pers(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image

        self.image = Varis.Pers_Icon
        self.rect = self.image.get_rect()

        Varis.pers_rect = self.rect

    def update(self, pos):
        self.image = Varis.Pers_Icon
        self.rect = self.image.get_rect()

        self.rect.topleft = pos
        Varis.pers_rect = self.rect
        self.is_collision()

    @staticmethod
    def is_collision():
        if math.ceil(Varis.pers_rect.right + Varis.one * 3) >= Varis.game_screen_w:
            Varis.pers_can_go_right = False
        if math.floor(Varis.pers_rect.left - Varis.one * 3) <= 0:
            Varis.pers_can_go_left = False
        if math.ceil(Varis.pers_rect.bottom + Varis.one * 3) >= Varis.game_screen_h:
            Varis.pers_can_go_down = False
        if math.floor(Varis.pers_rect.top - Varis.one * 3) <= 0:
            Varis.pers_can_go_up = False
        Varis.Hard_Objects_group.update()

    @staticmethod
    def create_bullet(color, speed, size, path_change, die_distance, bullet_index):
        if bullet_index == 0:
            return Minigun_Bullet(path_change, color, speed, size, die_distance)
        elif bullet_index == 1:
            return Shotgun_Bullet(path_change, color, speed, size, die_distance)
        elif bullet_index == 2:
            return Flame_Bullet(path_change, color, speed, size, die_distance)
        elif bullet_index == 999:
            return WTF_Bullet(path_change, color, speed, size, die_distance)

    # Move
    def pers_move(self, button_index, pos_change):
        Varis.dd_but_color[button_index] = Varis.LITTLE_BLUE
        Varis.pers_pos[0] += pos_change[0]
        Varis.pers_pos[1] += pos_change[1]
        self.is_collision()
        if Varis.Bad_move:# and Varis.pers_can_go_right and Varis.pers_can_go_left and Varis.pers_can_go_down and Varis.pers_can_go_up:
            if pos_change[0] != 0:
                this_bad_move_list = Bad_move_list.copy()
                if not Varis.pers_can_go_up:
                    this_bad_move_list.remove(-Varis.one)
                if not Varis.pers_can_go_down:
                    this_bad_move_list.remove(Varis.one)
                change_pos = random.choice(this_bad_move_list)
                Varis.pers_pos[1] += change_pos
            if pos_change[1] != 0:
                this_bad_move_list = Bad_move_list.copy()
                if not Varis.pers_can_go_right:
                    this_bad_move_list.remove(Varis.one)
                if not Varis.pers_can_go_left:
                    this_bad_move_list.remove(-Varis.one)
                change_pos = random.choice(this_bad_move_list)
                Varis.pers_pos[0] += change_pos
        self.is_collision()

    def pers_move_left(self):
        self.pers_move(0, (-Varis.one * 2, 0))

    def pers_move_right(self):
        self.pers_move(2, (Varis.one * 2, 0))

    def pers_move_up(self):
        self.pers_move(1, (0, -Varis.one * 2))

    def pers_move_down(self):
        self.pers_move(3, (0, Varis.one * 2))



# |------------------------------------------------- Bullets -------------------------------------------------|



class Minigun_Bullet(pygame.sprite.Sprite):
    def __init__(self, change_path, color, speed, size, die_distance):
        super().__init__()
        self.speed = speed
        self.die_distance = die_distance
        mouse_pos = pygame.mouse.get_pos()
        self.live_time = 0
        self.type_of_bullet = ""


        self.type_of_bullet = "Minigun"

        self.angle = math.degrees(math.atan2(mouse_pos[1] - Varis.pers_cen[1] - Varis.pers_size[1], mouse_pos[0] - Varis.pers_cen[0] - Varis.pers_size[0])) + change_path
        angle = math.degrees(math.atan2(mouse_pos[1] - Varis.pers_cen[1] - Varis.pers_size[1], mouse_pos[0] - Varis.pers_cen[0] - Varis.pers_size[0]))
        angle = math.radians(angle)

        self.angle = math.radians(self.angle)
        self.start_pos_x = Varis.pers_pos[0] + Varis.tile + math.cos(angle) * Varis.block * 2
        self.start_pos_y = Varis.pers_pos[1] + Varis.tile + math.sin(angle) * Varis.block * 2
        self.dx = math.cos(self.angle)
        self.dy = math.sin(self.angle)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(center=(self.start_pos_x, self.start_pos_y))
        self.image.fill(color)

        Varis.pers_weapon_angle = angle
        Varis.pers_weapon_image_angle = angle

        # Anti-stop
        if round(self.dx, 2) == 0 and round(self.dy, 2) == 0:
            self.dx = 0.2
            self.dy = 0.2

    def update(self, are_update_bullet=True, collide_rect=False, x=False, y=False, is_flame=False):
        if are_update_bullet:
            self.rect.x = self.rect.x + self.dx * self.speed
            self.rect.y = self.rect.y + self.dy * self.speed
            self.live_time += 1

        if (collide_rect and collide_rect.collidepoint(self.rect.center)) or self.rect.centerx > Varis.game_screen_w or self.rect.centerx < 0 or self.rect.centery > Varis.game_screen_h or self.rect.centery < 0:
            self.kill()


class Shotgun_Bullet(pygame.sprite.Sprite):
    def __init__(self, change_path, color, speed, size, die_distance):
        super().__init__()
        self.speed = speed
        self.die_distance = die_distance
        mouse_pos = pygame.mouse.get_pos()
        self.live_time = 0
        self.type_of_bullet = ""


        self.type_of_bullet = "Shotgun"

        self.angle = math.degrees(math.atan2(mouse_pos[1] - Varis.pers_cen[1] - Varis.pers_size[1], mouse_pos[0] - Varis.pers_cen[0] - Varis.pers_size[0])) + change_path
        angle = math.degrees(math.atan2(mouse_pos[1] - Varis.pers_cen[1] - Varis.pers_size[1], mouse_pos[0] - Varis.pers_cen[0] - Varis.pers_size[0]))

        angle = math.radians(angle)
        self.angle = math.radians(self.angle)
        self.start_pos_x = Varis.pers_pos[0] + Varis.tile + math.cos(angle) * Varis.block * 2
        self.start_pos_y = Varis.pers_pos[1] + Varis.tile + math.sin(angle) * Varis.block * 2
        self.dx = math.cos(self.angle)
        self.dy = math.sin(self.angle)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(center=(self.start_pos_x, self.start_pos_y))
        self.image.fill(color)

        Varis.pers_weapon_angle = angle
        Varis.pers_weapon_image_angle = angle

        self.can_reflection = False

        # Anti-stop
        if round(self.dx, 2) == 0 and round(self.dy, 2) == 0:
            self.dx = 0.2
            self.dy = 0.2

    def update(self, are_update_bullet=True, collide_rect=False, x=False, y=False, is_flame=False):
        if are_update_bullet:
            self.rect.x = self.rect.x + self.dx * self.speed
            self.rect.y = self.rect.y + self.dy * self.speed
            self.live_time += 1


        if collide_rect and collide_rect.collidepoint(self.rect.center):
            self.kill()
        elif self.rect.centerx > Varis.game_screen_w or self.rect.centerx < 0:
            if self.can_reflection:
                self.dx = -self.dx
        elif self.rect.centery > Varis.game_screen_h or self.rect.centery < 0:
            if self.can_reflection:
                self.dy = -self.dy


class Flame_Bullet(pygame.sprite.Sprite):
    def __init__(self, change_path, color, speed, size, die_distance):
        super().__init__()
        self.speed = speed
        self.die_distance = die_distance
        mouse_pos = pygame.mouse.get_pos()
        self.live_time = 0
        self.type_of_bullet = ""
        self.start_size = size
        self.size = size

        # Flame Thrower

        self.R = color[0]
        self.G = color[1]
        self.B = color[2]

        self.type_of_bullet = "Flame"
        self.angle = math.degrees(math.atan2(mouse_pos[1] - Varis.pers_cen[1] - Varis.pers_size[1], mouse_pos[0] - Varis.pers_cen[0] - Varis.pers_size[0]))
        self.angle = math.radians(self.angle)
        self.start_pos_x = Varis.pers_pos[0] + Varis.tile + math.cos(self.angle) * Varis.block * 2
        self.start_pos_y = Varis.pers_pos[1] + Varis.tile + math.sin(self.angle) * Varis.block * 2
        self.dx = math.cos(self.angle) + change_path
        self.dy = math.sin(self.angle) - change_path

        self.stop_x = self.dx / 500
        self.stop_y = self.dy / 500

        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(center=(self.start_pos_x, self.start_pos_y))
        self.image.fill((self.R, self.G, self.B))

        self.die_time = 100

        Varis.pers_weapon_angle = self.angle
        Varis.pers_weapon_image_angle = self.angle

        self.can_reflection = True



        # Anti-stop
        if round(self.dx, 5) == 0 and round(self.dy, 5) == 0:
            self.dx = 0.2
            self.dy = 0.2

    def update(self, are_update_bullet=True, collide_rect=False, x=False, y=False, is_flame=True):
        if are_update_bullet:
            self.rect.x = self.rect.x + self.dx * self.speed
            self.rect.y = self.rect.y + self.dy * self.speed
            self.live_time += 1
            self.R = max(30, self.R - self.live_time / Varis.FLAME_BULLET_COLOR_R_CHANGE)
            self.G = max(30, self.G - self.live_time / Varis.FLAME_BULLET_COLOR_G_CHANGE)
            self.B = max(30, self.B - self.live_time / Varis.FLAME_BULLET_COLOR_B_CHANGE)
            self.size = (self.size[0] + Varis.tile / 100, self.size[0] + Varis.tile / 100)
            self.image = pygame.Surface(self.size)
            self.image.fill((self.R, self.G, self.B))
            self.dx = max(abs(self.dx) - abs(self.stop_x), abs(self.stop_x)) * Varis.get_signum(self.dx)
            self.dy = max(abs(self.dy) - abs(self.stop_y), abs(self.stop_y)) * Varis.get_signum(self.dy)

        if round(self.dy, 1) == 0 and round(self.dx, 1) == 0:
            self.live_time = self.die_time + 1
            self.kill()

        if self.live_time > self.die_time:
            self.kill()


        # and not self.type_of_bullet == "Flame"
        if self.rect.centerx > Varis.game_screen_w or self.rect.centerx < 0:
            if self.can_reflection:
                self.dx = -self.dx
                self.live_time = max(self.live_time, round(self.die_time * 0.9))
        elif self.rect.centery > Varis.game_screen_h or self.rect.centery < 0:
            if self.can_reflection:
                self.dy = -self.dy
                self.live_time = max(self.live_time, round(self.die_time * 0.9))
        elif (collide_rect and collide_rect.collidepoint(self.rect.center)) or Varis.is_point_in_circle(self.start_pos_x, self.start_pos_y, self.die_distance, self.rect.centerx, self.rect.centery):
            self.kill()


class WTF_Bullet(pygame.sprite.Sprite):
    def __init__(self, change_path, color, speed, size, die_distance):
        super().__init__()
        self.speed = speed
        self.die_distance = die_distance
        self.change_path = change_path
        self.live_time = 0

        self.max_size = max(size[0], size[1])
        self.old_pos = (999999, 999999)

        self.type_of_bullet = "WTF"
        Varis.pers_weapon_angle = random.randint(-180, 180)

        self.angle = random.randint(-180, 180)
        self.angle = math.radians(self.angle)
        self.start_pos_x = Varis.pers_weapon_cen[0]
        self.start_pos_y = Varis.pers_weapon_cen[1]
        self.dx = math.cos(self.angle)
        self.dy = math.sin(self.angle)

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(center=(self.start_pos_x, self.start_pos_y))
        self.image.fill(color)

        Varis.pers_weapon_image_angle = self.angle

        self.reflection_chance = 3
        self.can_reflection = not bool(random.randint(0, self.reflection_chance))


    def update(self, are_update_bullet=True, collide_rect=False, x=False, y=False, is_flame=False):
        if are_update_bullet:
            self.rect.x = self.rect.x + self.dx * self.speed
            self.rect.y = self.rect.y + self.dy * self.speed
            #self.live_time += 1

            if self.rect.x == self.old_pos[0] and self.rect.y == self.old_pos[1]:
                self.kill()
            self.old_pos = (self.rect.x, self.rect.y)


        if self.rect.centerx > Varis.game_screen_w or self.rect.centerx < 0:
            if self.can_reflection:
                self.dx = -self.dx
                self.can_reflection = not bool(random.randint(0, self.reflection_chance))
        elif self.rect.centery > Varis.game_screen_h or self.rect.centery < 0:
            if self.can_reflection:
                self.dy = -self.dy
                self.can_reflection = not bool(random.randint(0, self.reflection_chance))


        elif (collide_rect and collide_rect.collidepoint(self.rect.center)) or not Varis.is_point_in_box(self.rect.center, (0 - self.max_size, 0 - self.max_size, Varis.game_screen_w + self.max_size, Varis.game_screen_h + self.max_size)):# or self.live_time > 500:
            self.kill()


# |------------------------------------------------- Pers_weapon -------------------------------------------------|
class Pers_weapon(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.orig_image = image
        self.image = self.orig_image
        self.rect = self.image.get_rect()
        Varis.pers_weapon_cen = self.rect.center

        self.angle = math.degrees(Varis.pers_weapon_angle)
        self.angle_change_times = round(Varis.Melee_weapon_info_list[Varis.Select_pers_list_index[1]][1] / Varis.Melee_weapon_info_list[Varis.Select_pers_list_index[1]][2])
        self.angle_change = Varis.Melee_weapon_info_list[Varis.Select_pers_list_index[1]][1]

        self.melee_attack_direction = 1

        self.mask = pygame.mask.from_surface(self.image, 10)


    def update(self, image):
        if Varis.Pers_current_weapon_info_list[1] == 0:
            self.rotate_to_mouse(image)
        elif Varis.Pers_current_weapon_info_list[1] == 1:
            if Varis.Is_pers_melee_can_attack:
                self.rotate_to_mouse(image)
            elif not Varis.Is_pers_melee_can_attack:
                if self.angle_change_times > 0:
                    self.melee_attack(image)
                    self.angle_change_times -= 1
                else:
                    for enemy in Varis.Enemy_group:
                        enemy.can_be_hurt_by_melee = True
                    Varis.Is_pers_melee_can_attack = True
                    self.melee_attack_direction *= -1


    def get_mask_rect(self):
        self.mask = pygame.mask.from_surface(self.image, 10)
        self.rect = self.mask.get_rect()

        self.rect.width = self.image.get_width()
        self.rect.height = self.image.get_height()

    def rotate_to_mouse(self, image):
        self.orig_image = image
        self.angle = math.degrees(Varis.pers_weapon_angle)
        Varis.pers_weapon_cen = self.rect.center
        if (-math.degrees(Varis.pers_weapon_angle) > 90 or -math.degrees(Varis.pers_weapon_angle) < -90) and Varis.Select_weapon_id != "g999":
            image = self.orig_image.copy()
            image = pygame.transform.rotate(image, self.angle)
            self.image = pygame.transform.flip(image, False, True)

        else:
            self.image = pygame.transform.rotate(self.orig_image.copy(), -math.degrees(Varis.pers_weapon_image_angle))

        #image.fill(Varis.RED)

        self.get_mask_rect()

        self.rect.centerx = Varis.pers_cen[0] + math.cos(Varis.pers_weapon_angle) * Varis.block * 1.3 + Varis.pers_size[0]
        self.rect.centery = Varis.pers_cen[1] + math.sin(Varis.pers_weapon_angle) * Varis.block * 1.3 + Varis.pers_size[1]



    def melee_attack(self, image):
        self.angle_change = Varis.Melee_weapon_info_list[Varis.Select_pers_list_index[1]][1]
        self.orig_image = image

        self.angle = Varis.pers_weapon_angle
        if self.angle_change != 360:
            angle_move_num = Varis.Melee_weapon_info_list[Varis.Select_pers_list_index[1]][2] * (round(self.angle_change / Varis.Melee_weapon_info_list[Varis.Select_pers_list_index[1]][2]) - self.angle_change_times) * self.melee_attack_direction
            Varis.pers_weapon_fake_angle = math.degrees(self.angle) - self.angle_change / 2 * self.melee_attack_direction + angle_move_num
        else:
            Varis.pers_weapon_fake_angle += Varis.Melee_weapon_info_list[Varis.Select_pers_list_index[1]][2]

        if (self.melee_attack_direction < 0 and 90 > Varis.pers_weapon_fake_angle > -90) or (self.melee_attack_direction > 0 and not (90 > Varis.pers_weapon_fake_angle > -90)):
            self.orig_image = pygame.transform.flip(self.orig_image, False, True)
        if -Varis.pers_weapon_fake_angle > 90 or -Varis.pers_weapon_fake_angle < -90:
            image = self.orig_image.copy()
            image = pygame.transform.rotate(image, Varis.pers_weapon_fake_angle)
            self.image = pygame.transform.flip(image, False, True)

        else:
            self.image = pygame.transform.rotate(self.orig_image.copy(), -Varis.pers_weapon_fake_angle)


        self.get_mask_rect()

        self.rect.centerx = Varis.pers_cen[0] + math.cos(math.radians(Varis.pers_weapon_fake_angle)) * Varis.block * 1.3 + Varis.pers_size[0]
        self.rect.centery = Varis.pers_cen[1] + math.sin(math.radians(Varis.pers_weapon_fake_angle)) * Varis.block * 1.3 + Varis.pers_size[1]
        Varis.pers_weapon_cen = self.rect.center


# |------------------------------------------------- Norm_Block_Object -------------------------------------------------|
class Norm_Block_Object(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


    def update(self, bullet_collision_check=False):
        if Varis.pers_rect.colliderect(self.rect):
            coll_point = max(6 * Varis.one, 1)
            if coll_point >= Varis.pers_rect.right - self.rect.left >= -coll_point:
                Varis.pers_can_go_right = False
            if coll_point >= Varis.pers_rect.left - self.rect.right >= -coll_point:
                Varis.pers_can_go_left = False
            if coll_point >= Varis.pers_rect.bottom - self.rect.top >= -coll_point:
                Varis.pers_can_go_down = False
            if coll_point >= Varis.pers_rect.top - self.rect.bottom >= -coll_point:
                Varis.pers_can_go_up = False
        if bullet_collision_check:
            if not Varis.is_point_in_circle(self.rect.centerx, self.rect.centery, Varis.block * 7, Varis.pers_pos[0], Varis.pers_pos[1]):
                Varis.Flame_Bullets.update(False, self.rect, self.rect.centerx, self.rect.centery)
            Varis.WTF_Bullets.update(False, self.rect, self.rect.centerx, self.rect.centery)
            Varis.Minigun_Bullets.update(False, self.rect, self.rect.centerx, self.rect.centery)
            Varis.Shotgun_Bullets.update(False, self.rect, self.rect.centerx, self.rect.centery)
            #Varis.Bullet_group.update(False, self.rect, self.rect.centerx, self.rect.centery)


# |------------------------------------------------- Stone_warrior -------------------------------------------------|
class Stone_warrior(pygame.sprite.Sprite):
    def __init__(self, image, size, x, y):
        super().__init__()
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.Vect_cen_x = self.rect.centerx
        self.Vect_cen_y = self.rect.centery
        self.can_go_right = True
        self.can_go_left = True
        self.can_go_down = True
        self.can_go_up = True

        self.dx = 0
        self.dy = 0

        self.ticks = 0

        self.hp = 20
        self.defence = 0.5
        self.can_be_hurt_by_melee = True

        self.hp_font = pygame.font.SysFont('arial', round(Varis.tile))

        self.hp_text = self.hp_font.render(str(round(self.hp)), False, Varis.WHITE)
        self.hp_text_rect = self.hp_text.get_rect()
        self.hp_text_rect.center = (self.rect.centerx, round(self.rect.top - Varis.tile))

        Varis.Stone_warrior_rects.append(self.rect)
        self.rect_index = Varis.Stone_warrior_rects.index(self.rect)

    def is_collision(self):

        self.can_go_right = True
        self.can_go_left = True
        self.can_go_down = True
        self.can_go_up = True

        if math.ceil(self.rect.right + Varis.one * 5) >= Varis.game_screen_w:
            self.can_go_right = False
            self.dx = -1
        if math.floor(self.rect.left - Varis.one * 5) <= 0:
            self.can_go_left = False
            self.dx = 1
        if math.ceil(self.rect.bottom + Varis.one * 5) >= Varis.game_screen_h:
            self.can_go_down = False
            self.dy = -1
        if math.floor(self.rect.top - Varis.one * 5) <= 0:
            self.can_go_up = False
            self.dy = 1

        """
        for i in range(len(Varis.Stone_warrior_rects) - 1):
            obj_rect = Varis.Stone_warrior_rects[i]
            if i != self.rect_index and Varis.is_in_circle(self.rect.centerx, self.rect.centery, Varis.block, obj_rect.centerx, obj_rect.centery):
                accuracy = Varis.one * 2
                accuracy_x = abs(self.dx) * 2
                accuracy_y = abs(self.dy) * 2
                if (obj_rect.right >= math.ceil(self.rect.right + accuracy_x) >= obj_rect.left) and (self.rect.bottomright[1] + accuracy >= obj_rect.top) and (self.rect.topright[1] - accuracy <= obj_rect.bottom):
                    self.can_go_right = False
                if (obj_rect.left <= math.ceil(self.rect.right - accuracy_x) <= obj_rect.left) and (self.rect.bottomleft[1] + accuracy >= obj_rect.top) and (self.rect.topleft[1] - accuracy <= obj_rect.bottom):
                    self.can_go_left = False
                if (obj_rect.bottom >= math.ceil(self.rect.bottom + accuracy_y) >= obj_rect.top) and (self.rect.bottomright[0] + accuracy >= obj_rect.left) and (self.rect.bottomleft[0] - accuracy <= obj_rect.right):
                    self.can_go_up = False
        """
        """
        for i in range(len(Varis.Stone_warrior_rects) - 1):
            obj_rect = Varis.Stone_warrior_rects[i]
            if i != self.rect_index and Varis.is_in_circle(self.rect.centerx, self.rect.centery, Varis.block, obj_rect.centerx, obj_rect.centery):
                accuracy = Varis.one * 2
                accuracy_x = abs(self.dx) * 2
                accuracy_y = abs(self.dy) * 2
                if (obj_rect.right >= math.ceil(self.rect.right + accuracy_x) >= obj_rect.left) and (self.rect.bottomright[1] + accuracy >= obj_rect.top) and (self.rect.topright[1] - accuracy <= obj_rect.bottom):
                    self.can_go_right = False
                if (obj_rect.left <= math.ceil(self.rect.right - accuracy_x) <= obj_rect.left) and (self.rect.bottomleft[1] + accuracy >= obj_rect.top) and (self.rect.topleft[1] - accuracy <= obj_rect.bottom):
                    self.can_go_left = False
                if (obj_rect.bottom >= math.ceil(self.rect.bottom + accuracy_y) >= obj_rect.top) and (self.rect.bottomright[0] + accuracy >= obj_rect.left) and (self.rect.bottomleft[0] - accuracy <= obj_rect.right):
                    self.can_go_up = False
                if (obj_rect.top <= math.ceil(self.rect.top - accuracy_y) <= obj_rect.bottom) and (self.rect.bottomright[0] + accuracy >= obj_rect.left) and (self.rect.bottomleft[0] - accuracy <= obj_rect.right):
                    self.can_go_down = False
        """


        for bullet in Varis.Guns_bullets_group_list[Varis.Select_pers_list_index[Pers_current_weapon_info_list[1]]]:
            if pygame.sprite.collide_rect(self, bullet):
                if (Varis.Select_pers_list_index[Pers_current_weapon_info_list[1]] == 2 and random.randint(0, 40) == 7) or (Varis.Select_pers_list_index[Pers_current_weapon_info_list[1]] != 2):
                    #print(self.dx, "<->", end=" ")
                    #lol = self.dx
                    self.dx += Varis.Bullets_info_list[Varis.Select_pers_list_index[Pers_current_weapon_info_list[1]]][1] * Varis.interval_limitation(0, 3, (self.rect.width / 3 - abs(self.rect.centerx - bullet.rect.centerx) / 1)) * Varis.get_signum(self.rect.centerx - bullet.rect.centerx)
                    self.dy += Varis.Bullets_info_list[Varis.Select_pers_list_index[Pers_current_weapon_info_list[1]]][1] * Varis.interval_limitation(0, 3, (self.rect.height / 3 - abs(self.rect.centery - bullet.rect.centery))) * Varis.get_signum(self.rect.centery - bullet.rect.centery)
                    #print(self.dx, "------------------------------------------", self.dx - lol)

                self.hp -= max(0, Varis.Bullets_info_list[Varis.Select_pers_list_index[Pers_current_weapon_info_list[1]]][0] - self.defence)
                bullet.kill()



        change_d = Varis.one * 2
        if not self.can_go_right:
            if self.can_go_left:
                self.dx = -change_d
            elif not self.can_go_left:
                self.dx = 0
                if self.can_go_up:
                    self.dy = -change_d
                elif self.can_go_down:
                    self.dy = change_d
        if not self.can_go_left:
            if self.can_go_right:
                self.dx = change_d
            elif not self.can_go_right:
                self.dx = 0
                if self.can_go_down:
                    self.dy = change_d
                elif self.can_go_up:
                    self.dy = -change_d
        if not self.can_go_down:
            if self.can_go_up:
                self.dy = -change_d
            elif not self.can_go_left:
                self.dy = 0
                if self.can_go_right:
                    self.dx = change_d
                elif self.can_go_left:
                    self.dx = -change_d
        if not self.can_go_up:
            if self.can_go_down:
                self.dy = change_d
            elif not self.can_go_left:
                self.dy = 0
                if self.can_go_left:
                    self.dx = -change_d
                elif self.can_go_right:
                    self.dx = change_d

        Varis.Hard_Objects_group.update()

    def change_move(self):
        self.is_collision()

        #if random.randint(0, 100)
        chance = random.randint(0, 100)
        if chance <= 40:
            self.dx = 0
        elif 40 < chance <= 50 + random.randint(-5, 10):
            self.dx = random.randint(-1, 1)
        else:
            self.dx = Varis.get_signum((Varis.pers_cen[0] - self.rect.centerx) / 100) * random.randint(0, 1)

        chance = random.randint(0, 100)
        if chance <= 40:
            self.dy = 0
        elif 40 < chance <= 50 + random.randint(-5, 10):
            self.dy = random.randint(-1, 1)
        else:
            self.dy = Varis.get_signum((Varis.pers_cen[1] - self.rect.centery) / 100) * random.randint(0, 1)

        if (not self.can_go_right and self.dx > 0) or (not self.can_go_left and self.dx < 0):
            self.dx = 0
        if (not self.can_go_down and self.dy > 0) or (not self.can_go_up and self.dy < 0):
            self.dy = 0



    def update(self):
        Varis.Stone_warrior_rects[self.rect_index] = self.rect

        self.ticks += 1

        if self.ticks > 100:
            self.ticks = 0



        if self.ticks % 20 == 0:
            self.change_move()

        self.is_collision()
        # if (self.dx > 0 and self.can_go_right) or (self.dx < 0 and self.can_go_left):
        self.Vect_cen_x += self.dx
        # if (self.dy > 0 and self.can_go_down) or (self.dy < 0 and self.can_go_up):
        self.Vect_cen_y += self.dy
        # print("(", self.Vect_cen_x, "\b, ", self.Vect_cen_y, ")")
        self.rect.center = (round(self.Vect_cen_x), round(self.Vect_cen_y))

        if round(self.hp) <= 0:
            self.kill()

        self.hp_text = self.hp_font.render(str(round(self.hp)), False, Varis.Enemy_hp_color)
        self.hp_text_rect = self.hp_text.get_rect()
        self.hp_text_rect.center = (self.rect.centerx, round(self.rect.top - Varis.tile))


