import pygame, random

width = 800   #ancho de la ventana
height = 600   #alto de la ventana
black = (0,0,0)  #pixeles para el color negro
white = (255,255,255)   #pixeles para el color blanco

pygame.init() #inicializamos pygame
pygame.mixer.init()  #inicializar el mixer que nos sirve para el tema de sonido
screen = pygame.display.set_mode((width, height))   #creacion de ventana
pygame.display.set_caption("Bienvenido al juego tripulante")  #le damos un nombre a la ventana
clock = pygame.time.Clock()  #Creamos el reloj para controlar los frames/seg
score = 0
vida = 100

def texto(frame,text,size,x,y):
	font = pygame.font.SysFont('Small Fonts', size, bold=True)
	text_frame = font.render(text, True, white, black)
	text_rect = text_frame.get_rect()
	text_rect.midtop = (x,y)
	frame.blit(text_frame,text_rect)

def barra_vida(frame,x,y,nivel):
	longitud = 100
	alto = 20
	fill = int((nivel/100)*longitud)
	border = pygame.Rect(x, y, longitud, alto)
	fill = pygame.Rect(x, y, fill, alto)
	pygame.draw.rect(frame, (255,0,55),fill)
	pygame.draw.rect(frame, black, border, 4)


class Player(pygame.sprite.Sprite):  #Creamos la clase jugador y llamamos un objeto en pygame 
	def __init__(self):  #Inicializamos la clase
		super().__init__()  #definimos la superclase sprite
		self.image = pygame.image.load("assets/spaceship.png").convert()  #cargamos la imagen de nuestra nave jugador
		self.image.set_colorkey(black)  #removemos el fondo negro de la imagen
		self.rect = self.image.get_rect()  #obtenemos el cuadro de mi sprite
		self.rect.centerx = width // 2  #Determinamos la mitad del ancho de la pantalla para el cuadro delimitador del sprite
		self.rect.bottom = height  #Determinamos el alto del cuadro delimitador de nuestro sprite 
		self.speed_x = 0   #variable de velocidad
		self.vida = 100

	def update(self):
		self.speed_x = 0 #inicializamos la variable de velocidad en el eje x
		self.speed_y = 0 #inicializamos la variable de velocidad en el eje y
		keystate = pygame.key.get_pressed()  #preguntamos si alguna tecla ha sido presionada
		if keystate[pygame.K_LEFT]:
			self.speed_x = -5
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 5
		if keystate[pygame.K_UP]:
			self.speed_y = -5
		if keystate[pygame.K_DOWN]:
			self.speed_y = 5
		self.rect.x += self.speed_x  #Nos movemos en x según el valor que toma la velocidad si se presiona K_RIGTH o K_LEFT
		self.rect.y += self.speed_y  #Nos movemos en y según el valor que toma la velocidad si se presiona K_UP o K_DOWN
		if self.rect.right > width:  #Establecemos la condicion para que el sprite no sobrepase el valor maximo del ancho de la ventana
			self.rect.right = width
		if self.rect.left < 0:   #Establecemos la condicion para que el sprite no sobrepase el valor minimo del ancho de la ventana
			self.rect.left = 0
		if self.rect.bottom > height:   #Establecemos la condicion para que el sprite no sobrepase el valor maximo del alto de la ventana
			self.rect.bottom = height
		if self.rect.top < 0:  #Establecemos la condicion para que el sprite no sobrepase el valor minimo del alto de la ventana
			self.rect.top = 0

	def shoot(self):
		bullet1 = Bullet(self.rect.centerx - 20, self.rect.top + 25)
		all_sprites.add(bullet1)
		bullets.add(bullet1)

		bullet2 = Bullet(self.rect.centerx + 20, self.rect.top + 25)
		all_sprites.add(bullet2)
		bullets.add(bullet2)	

		#Agregamos sonido del misil
		misil_sound.play()


class Enemy(pygame.sprite.Sprite):  #Creamos la clase jugador y llamamos un objeto en pygame 
	def __init__(self):  #Inicializamos la clase
		super().__init__()  #definimos la superclase sprite
		self.image = pygame.image.load("assets/enemy.png").convert()  #cargamos la imagen de nuestra nave jugador
		self.image.set_colorkey(black)  #removemos el fondo negro de la imagen
		self.rect = self.image.get_rect()  #obtenemos el cuadro de mi sprite
		self.rect.x = random.randrange(width - self.rect.width)  #Determinamos la mitad del ancho de la pantalla para el cuadro delimitador del sprite
		self.rect.y = random.randrange(-500,-40)
		self.speedy = random.randrange(1, 10)
		self.speedx = random.randrange(-5, 5)

	def update(self):
		self.rect.y += self.speedy
		#self.rect.x += self.speedx
		if self.rect.top > height + 10 or self.rect.left < -25 or self.rect.right > width + 22 :
			self.rect.x = random.randrange(width - self.rect.width)
			self.rect.y = random.randrange(-100,-40)
			self.speedy = random.randrange(2, 6)


class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("assets/missile.png")
		self.image.set_colorkey(black)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()


def show_go_screen_game_over():
	screen.blit(fondo, [0, 0])
	texto(screen, "GAME OVER", 65, width // 2, height / 2)
	texto(screen, "Presiona Enter para continuar", 17, width // 2, height * 3/4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					waiting = False


def show_go_screen():
	screen.blit(fondo, [0, 0])
	texto(screen, "Bienvenido a Spaceship", 65, width // 2, height / 4)
	texto(screen, "Presiona tecla espacio para disparar y las flechas para moverte", 27, width // 2, height // 2)
	texto(screen, "Presiona Enter para empezar", 17, width // 2, height * 3/4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					waiting = False

# Cargar fondo.
fondo = pygame.image.load("assets/Space-Wallpaper.png").convert()

# Cargar sonidos
misil_sound = pygame.mixer.Sound("assets/Crunch.wav")
explosion_misil_sound = pygame.mixer.Sound("assets/Teleport2.wav")
#pygame.mixer.music.load("assets/music.ogg")
#pygame.mixer.music.set_volume(0.1)

# Cargar sonidos
laser_sound = pygame.mixer.Sound("assets/Crunch.wav")
explosion_sound = pygame.mixer.Sound("assets/Teleport2.wav")
#pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.1)


#all_sprites = pygame.sprite.Group()  #Creamos el grupo de todos los sprites
#enemy_list = pygame.sprite.Group()
#bullets = pygame.sprite.Group()


#player = Player()  #Creamos nuestra instancia jugador
#all_sprites.add(player)  #Agregamos a nuestro jugador al grupo de sprites

#for i in range(5):
#	enemy = Enemy()
#	all_sprites.add(enemy)  #Agregamos a nuestro enemigo al grupo de sprites
#	enemy_list.add(enemy)


# Game Loop donde programamos la lógica de ejecución del juego 
running = True
init_game = True
game_over = False

while running:
	if init_game:
		show_go_screen()
		init_game = False
		game_over = False
		all_sprites = pygame.sprite.Group()
		enemy_list = pygame.sprite.Group()
		bullets = pygame.sprite.Group()

		player = Player()
		all_sprites.add(player)

		for i in range(5):
			enemy = Enemy()
			all_sprites.add(enemy)
			enemy_list.add(enemy)

		#Marcador / Score
		score = 0

	if game_over==True:
		show_go_screen_game_over()
		init_game = True

	# Mantenemos el loop corriendo a una velocidad de 60 frames / seg
	clock.tick(60)
	# Evaluamos el estado del evento
	for event in pygame.event.get():
		# Creamos el evento para salir de la ventana
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()
				

	# Actualizamos todos los sprites
	all_sprites.update()

	#colisiones enemy - misil	
	colision = pygame.sprite.groupcollide(enemy_list, bullets, True, True)
	for k in colision:
		score+=1
		explosion_misil_sound.play()
		enemy = Enemy()
		all_sprites.add(enemy)
		enemy_list.add(enemy)

	# Colisiones jugador - enemy
	hits = pygame.sprite.spritecollide(player, enemy_list, True)
	for hit in hits:
		player.vida -=25 
		enemy = Enemy()
		all_sprites.add(enemy)	
		enemy_list.add(enemy)
		if player.vida <=0:
			game_over = True	

	#Dibujamos / Renderizamos
	screen.blit(fondo, [0,0])
	all_sprites.draw(screen)  #Dibujamos en pantalla los sprites

	#indicador y score
	texto(screen, ('  SCORE: '+ str(score)+'      '),30, width-85,2)
	barra_vida(screen, width-285, 0, player.vida)

	# *after* drawing everything, flip the display.
	pygame.display.flip()

pygame.quit()