import pygame;

class Fighter:
    def __init__(self,player,x,y,data,sprite_sheet,animation_steps,flip):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.rect = pygame.Rect(x,y,80,180)
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet,animation_steps)
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.updatetime = pygame.time.get_ticks()
        self.running = False
        self.attack_cd = 0
        self.hit = False
        self.alive = True
    
    def load_images(self,sprite_sheet,animation_steps):
        animation_list = []
        for y,animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size,y * self.size,self.size,self.size)
                temp_img_list.append(pygame.transform.scale(temp_img,(self.size*self.image_scale,self.size*self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self,screen_width,screen_height,surface,target):
        dx = 0
        dy = 0
        SPEED = 10
        GRAVITY = 2
        self.running = False
        self.attack_type = 0

        # Get keypresses
        key = pygame.key.get_pressed()

        # attacking check
        if self.attacking == False and self.alive == True:
            if self.player == 1:

                # Movement
                if key[pygame.K_a]:  # Move left
                    dx -= SPEED
                    self.running = True
                if key[pygame.K_d]:  # Move right
                    dx += SPEED
                    self.running = True
                if key[pygame.K_SPACE] and self.jump==False:
                    self.vel_y = -30
                    self.jump = True
                if key[pygame.K_e] or key[pygame.K_s]:
                    self.attack(surface,target)

                    if key[pygame.K_e]:
                        self.attack_type = 1
                    if key[pygame.K_s]:
                        self.attack_type = 2
        
        if self.attacking == False and self.alive == True:
            if self.player == 2:

                # Movement
                if key[pygame.K_LEFT]:  # Move left
                    dx -= SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:  # Move right
                    dx += SPEED
                    self.running = True
                if key[pygame.K_UP] and self.jump==False:
                    self.vel_y = -30
                    self.jump = True
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(surface,target)

                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2
        
        self.vel_y += GRAVITY
        dy += self.vel_y

        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True
        
        if self.attack_cd > 0:
            self.attack_cd -= 1

        #ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        # Apply movement
        self.rect.x += dx
        self.rect.y += dy
    
    def update(self):
        if self.health <= 0:
            self.alive = False
            self.health = 0
            self.update_action(6)
        elif self.hit == True:
            self.update_action(5)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.jump == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cd = 50
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.updatetime > animation_cd:
            self.frame_index += 1
            self.updatetime = pygame.time.get_ticks()
        
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action])-1
            else:
                self.frame_index = 0
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cd += 20
                if self.action == 5:
                    self.hit = False
                    self.attacking = False
                    self.attack_cd = 20

    
    def attack(self,surface,target):
        if self.attack_cd == 0:
            self.attacking = True
            attack_hitbox = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip),self.rect.y,(2*self.rect.width),self.rect.height)

            if attack_hitbox.colliderect(target.rect):
                target.health -= 10
                target.hit = True

    def draw(self,surface):
        img = pygame.transform.flip(self.image,self.flip,False)
        surface.blit(img,(self.rect.x-(self.offset[0]*self.image_scale),self.rect.y-(self.offset[1]*self.image_scale)))

    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.updatetime = pygame.time.get_ticks()