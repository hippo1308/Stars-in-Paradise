"""
Tushi Thakkar
ICS3U0
FINAL CULMINATING
2/6/25
Stars in Paradise
"""
# importing modules needed
import sys, pygame, random, datetime

# initializing pygame in order to use its functions
pygame.init()
pygame.mixer.init()

# INFINITE SCROLLING SYSTEM
cameraX = 0  # Camera's position in the infinite world
BG_WIDTH = 1200  # Width of a single background tile
BG_SPEED = 5  # How fast in pixels, the background scrolls

# Character positions (relative to screen, NOT world)
kaelX = 300  # Kael stays roughly centered on screen
kaelY = 500
lumaX = 320  # Luma stays roughly centered on screen
lumaY = 500

# Scrolling boundaries - when characters hit these, trigger scrolling
SCROLL_LEFT_BOUNDARY = 200
SCROLL_RIGHT_BOUNDARY = 1000

# HEALTH SYSTEM
kaelHealth = 5  # Maximum health (5 hearts)
lumaHealth = 5  # Maximum health (5 hearts)
score = 0

# Collision cooldown to prevent multiple hits, and health decreasing too much
kaelCollisionCooldown = 0
lumaCollisionCooldown = 0
COLLISION_COOLDOWN_TIME = 60  # frames (2 seconds at 30 fps)

"""The main idea of using for loops to get the animation
 images is iterating through the files named 'x1', 'x2', 'x3', by 
 simply changing the number(i), each character has a movement which is
 labeled and numbered in the order, so when iterated back to back,
 they perform an animation. This logic is used for Luma and Kael, along with
 the left movements, where the images are flipped horizontally before 
 loading"""

# Animation loading
kaelIdle = []
for i in range(1, 7):
    imgIdleK = pygame.transform.scale(pygame.image.load(f'icons,sprites/kael/idle{i}.png'), (150, 150))
    kaelIdle.append(imgIdleK)

kaelRun = []
for x in range(1, 9):
    imgRunK = pygame.transform.scale(pygame.image.load(f'icons,sprites/kael/run{x}.png'), (150, 150))
    kaelRun.append(imgRunK)

kaelJump = []
for j in range(1, 9):
    imgJumpK = pygame.transform.scale(pygame.image.load(f'icons,sprites/kael/jump{j}.png'), (150, 150))
    kaelJump.append(imgJumpK)

kaelHit = []
for h in range(1, 5):
    imgHitK = pygame.transform.scale(pygame.image.load(f'icons,sprites/kael/hit{h}.png'), (150, 150))
    kaelHit.append(imgHitK)

lumaIdle = []
for X in range(1, 7):
    imgIdleL = pygame.transform.scale(pygame.image.load(f'icons,sprites/luma2/idle{X}.png'), (150, 150))
    lumaIdle.append(imgIdleL)

lumaRun = []
for R in range(1, 7):
    imgRunL = pygame.transform.scale(pygame.image.load(f'icons,sprites/luma2/run{R}.png'), (150, 150))
    lumaRun.append(imgRunL)

lumaJump = []
for J in range(1, 10):
    imgJumpL = pygame.transform.scale(pygame.image.load(f'icons,sprites/luma/jump{J}.png'), (150, 150))
    lumaJump.append(imgJumpL)

enemy1 = []
for w in range(1, 3):
    imgEnemy1 = pygame.transform.scale(pygame.image.load(f'enemies/enemy{w}.png'), (70, 80))
    enemy1.append(imgEnemy1)

enemy2 = []
for t in range(3, 5):
    imgEnemy2 = pygame.transform.scale(pygame.image.load(f'enemies/enemy{t}.png'), (70, 80))
    enemy2.append(imgEnemy2)

enemy3 = []
for p in range(5, 7):
    imgEnemy3 = pygame.transform.scale(pygame.image.load(f'enemies/enemy{p}.png'), (70, 80))
    enemy3.append(imgEnemy3)

kaelHeart = []
for o in range(5, -1, -1):
    kaelHeartImg = pygame.transform.scale(pygame.image.load(f'icons,sprites/hearts/tile00{o}.png'), (50, 80))
    kaelHeart.append(kaelHeartImg)

lumaHeart = []
for y in range(5, -1, -1):
    lumaHeartLuma = pygame.transform.scale(pygame.image.load(f'icons,sprites/hearts/tile00{y}.png'), (50, 80))
    lumaHeart.append(lumaHeartLuma)

# Screen setup
WIDTH = 1200
HEIGHT = 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# changing the window name
pygame.display.set_caption("Stars in Paradise")

# Background image setup for infinite scrolling
bg = pygame.image.load('main.png')
bg1 = pygame.image.load('bgs/bg3.png')

# transforming each to the screen's W, H
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
bg1 = pygame.transform.scale(bg1, (BG_WIDTH, HEIGHT))

# UI element display
control = pygame.image.load('controls.png')
control = pygame.transform.scale(control, (WIDTH, HEIGHT))

# initial game state when starting
gameState = "home"

# image set up for game state changing variables - the play and next buttons
# PLAY BUTTON
playBtn = pygame.image.load('icons,sprites/playBtn.png')
playBtn = pygame.transform.scale(playBtn, (150, 75))
playBtnRect = playBtn.get_rect(topleft=(975, 675))

# NEXT BUTTON
nextBtn = pygame.image.load('icons,sprites/nextBtn.png')
nextBtn = pygame.transform.scale(nextBtn, (250, 150))
nextBtnRect = nextBtn.get_rect(topleft=(500, 600))

# loading the star image
star = pygame.image.load('icons,sprites/star.png')
star = pygame.transform.scale(star, (40, 40))

# Sound
ripMomSound = pygame.mixer.music.load('sound/Mommy.mp3')
"""the mixer module basically controls the background music, 
by loading the mp3and then playing at a speed,/volume (functions) """

# flag to track the music, so it doesn't restart or
# keep playing when program is closed
musicStarted = False

# setting pace
clock = pygame.time.Clock()

# Movement flags
# KAEL
moveRight = False
moveLeft = False
jump = False
hit = False

# LUMA
moveRightL = False
moveLeftL = False
jumpL = False

# Animation tracking
# knowing the ONGOING frame of the character being displayed
currentFrameKael = 0
currentFrameLuma = 0
currentFrameEnemy1 = 0
currentFrameEnemy2 = 0
currentFrameEnemy3 = 0

# how fast to iterate through the lists of images for animation
frameSpeed = 0.25

# Separate velocity variables for each character for jumping
velocityKael = -15
velocityLuma = -15

# INFINITE SCROLLING VARIABLES
bgOffset = 0  # Background scroll offset -
""" the amount of pixels the bg moves, away from camera 
from starting position (therefore, starts with 0)"""
worldDistance = 0  # How far we've traveled in the world

# OBSTACLE SYSTEM FOR INFINITE SCROLLING
obstacles = []
nextObstacleDistance = 500  # Distance to next obstacle spawn

# Enemy animation tracking
enemyAnimationSpeed = 0.1  # Slower animation for enemies

#score list
scores = []

#score flag
scoreWritten = False

def checkCollision(rect1, rect2):
    #Check if two rectangles collide
    return rect1.colliderect(rect2)

def getCharacterRect(x, y, width=50, height=50):
    #Get character collision rectangle - made smaller and more centered
    # Offset the rectangle to center it better on the character sprite
    offset_x = 20  # Move rectangle slightly right to center on character
    offset_y = 70  # Move rectangle slightly down to center on character
    return pygame.Rect(x + offset_x, y + offset_y, width, height)

def getEnemyRect(obstacle):
    #Get enemy collision rectangle - made smaller and more centered for
    # better collision detection"""

    new_width = 40# 70-30
    new_height = 50# 80-30

    # Center the smaller collision box on the enemy sprites
    offset_x = 15# new_width // 2
    offset_y = 15# new_height // 2

    #returning a rectangle around the enemy
    return pygame.Rect(
        obstacle['x'] + offset_x,
        obstacle['y'] + offset_y,
        new_width,
        new_height
    )

def takeDamage(character):
    #Handle character taking damage
    global kaelHealth, lumaHealth, kaelCollisionCooldown, lumaCollisionCooldown

    if character == "kael" and kaelCollisionCooldown <= 0:
        kaelHealth = max(0, kaelHealth - 1)
        kaelCollisionCooldown = COLLISION_COOLDOWN_TIME

    elif character == "luma" and lumaCollisionCooldown <= 0:
        lumaHealth = max(0, lumaHealth - 1)
        lumaCollisionCooldown = COLLISION_COOLDOWN_TIME
        """we use the max() function here instead of -= because this would trigger game over. so once the 
         character health is -ve, it automatically sets to 0. Also we use the cool down to basically 
         stop the health from decreasing every frame the enemy is colliding with the characters, so in the
         condition, where cooldown starts with 0, to allow for damage to be taken, 
         then no more damage is taken until those 60 frames have passed."""

def hitEnemy(obstacle):
    #Handle hitting an enemy - convert to star and increase score
    global score
    obstacle['isHit'] = True
    obstacle['hitTime'] = pygame.time.get_ticks()
    score += 1
    """the get_ticks() is used to store the TIME Kael hits the enemy, which gets put into the dictionary
    so we know the exact point for the enemy to turn into a star"""

def drawHearts():
    #Draw single heart for each character that changes frame based on health
    # Draw Kael's heart (top left) - heart frame based on remaining health
    # Frame 0 = full health (5), Frame 5 = no health (0)
    # basically the reverse of takeDamage()
    kael_heart_frame = max(0, 5 - kaelHealth)  # 5-5=0 (full), 5-0=5 (empty)
    screen.blit(kaelHeart[kael_heart_frame], (10, 50))

    # Draw Luma's heart (below Kael's)
    luma_heart_frame = max(0, 5 - lumaHealth)
    screen.blit(lumaHeart[luma_heart_frame], (10, 120))

def drawUI():
    #Draw all UI elements
    # Draw hearts
    drawHearts()

    # Draw distance and score
    font = pygame.font.Font("icons,sprites/m6x11.ttf", 36)
    distance_text = font.render(f"Distance: {int(worldDistance)}", True, (65, 67, 65))
    score_text = font.render(f"* Score *: {score}", True, (242, 52, 215))

    screen.blit(distance_text, (950, 30))
    screen.blit(score_text, (950, 70))

    # Draw character names next to hearts, with a downloaded font and Font()
    name_font = pygame.font.Font("icons,sprites/m6x11.ttf", 34)
    kael_name = name_font.render("Kael", True, (243, 129, 5))
    luma_name = name_font.render("Luma", True, (85, 7, 139))

    screen.blit(kael_name, (70, 75))
    screen.blit(luma_name, (70, 145))

def checkGameOver():
    #Check if game should end, just a flag function
    if kaelHealth <= 0 or lumaHealth <= 0:
        return True
    else:
        return False

def spawnObstacle():
    # Spawn new obstacles as we scroll, randomly
    global nextObstacleDistance, worldDistance

    if worldDistance >= nextObstacleDistance:#this condition is always passed
        # Randomly choose enemy type (0, 1, or 2 for enemy1, enemy2, enemy3)
        enemyType = random.randint(0, 2)

        # Create new enemy obstacle
        obstacle = {
            'x': WIDTH + random.randint(0, 200),
            'y': random.randint(300, 550),
            'width': 70,  # Fixed width based on your enemy sprite size
            'height': 80,  # Fixed height based on your enemy sprite size
            'enemyType': enemyType,  # 0=enemy1, 1=enemy2, 2=enemy3
            'currentFrame': 0.0,  # Current animation frame (float for smooth animation)
            'isHit': False,  # Track if enemy has been hit
            'hitTime': 0  # When the enemy was hit
        }

        obstacles.append(obstacle)
        nextObstacleDistance += random.randint(300, 800)


def updateObstacles(scrollSpeed):
    #Move obstacles with the scrolling and remove off-screen ones
    global obstacles

    for obstacle in obstacles[:]:
        obstacle['x'] -= scrollSpeed

        # Update enemy animation only if not hit
        if obstacle['isHit'] == False:
            obstacle['currentFrame'] += enemyAnimationSpeed

            # Reset animation frame based on enemy type (all have 2 frames)
            if obstacle['currentFrame'] >= 2:
                obstacle['currentFrame'] = 0.0

        # Remove obstacles that have scrolled off the left side
        if obstacle['x'] + obstacle['width'] < -100:
            obstacles.remove(obstacle)


def drawObstacles():
    #Draw all current obstacles with enemy sprites or stars if hit
    current_time = pygame.time.get_ticks()

    for obstacle in obstacles[:]:
        if obstacle['isHit']:
            # Draw star instead of enemy
            screen.blit(star, (obstacle['x'], obstacle['y']))

            # Remove star after 1 second (1000 milliseconds)
            # the total time spent on the game - the time hit = the time passed since enemy was hit
            if current_time - obstacle['hitTime'] > 1000:
                obstacles.remove(obstacle)
        else:
            # Get the appropriate enemy sprite list and current frame
            enemyType = obstacle['enemyType']
            frameIndex = int(obstacle['currentFrame'])

            if enemyType == 0:
                # Use enemy1 sprites
                screen.blit(enemy1[frameIndex], (obstacle['x'], obstacle['y']))
            elif enemyType == 1:
                # Use enemy2 sprites
                screen.blit(enemy2[frameIndex], (obstacle['x'], obstacle['y']))
            elif enemyType == 2:
                # Use enemy3 sprites
                screen.blit(enemy3[frameIndex], (obstacle['x'], obstacle['y']))

def obstacleCollision():
    # Handle all collision detection between characters and enemies
    global kaelCollisionCooldown, lumaCollisionCooldown

    # Update collision cool downs, bringing back to 0 since if cool down is too large
    # the damage happens less often in fps, even if collision occurs,
    # CHECK CONDITION IN TAKE DAMAGE
    if kaelCollisionCooldown > 0:
        kaelCollisionCooldown -= 1
    if lumaCollisionCooldown > 0:
        lumaCollisionCooldown -= 1

    kaelRect = getCharacterRect(kaelX, kaelY)
    lumaRect = getCharacterRect(lumaX, lumaY)

    for obstacle in obstacles[:]:
        if obstacle['isHit']: # "if obstacle is Hit == True"
            continue  # Skip hit enemies

        enemyRect = getEnemyRect(obstacle)

        # Check if Kael is hitting (M key pressed) and colliding with enemy
        if hit == True and checkCollision(kaelRect, enemyRect):
            hitEnemy(obstacle)
            continue  # Don't check for damage collision if hitting

        # Check for damage collisions (only if not in cooldown frames)
        if hit == False and checkCollision(kaelRect, enemyRect):
            takeDamage("kael")

        if checkCollision(lumaRect, enemyRect):
            takeDamage("luma")

def drawInfiniteBackground():
    #Draw repeating background tiles
    global bgOffset

    """ Calculate how many tiles we need to cover 
    # the window screen, adding 2 for the tiles to 
    # blit once scrolling goes off-screen"""
    numTiles = (WIDTH // BG_WIDTH) + 2

    # Draw background tiles
    for i in range(numTiles):
        x = (i * BG_WIDTH) - (bgOffset % BG_WIDTH)
        screen.blit(bg1, (x, 0))

def scrollWorld(direction, speed):
    # Handle infinite world scrolling
    global bgOffset, worldDistance, cameraX

    # changing the coordinates and the position values to -ve OR
    # +ve by speed depending on the direction we're moving
    if direction == "right":
        bgOffset += speed
        worldDistance += speed
        cameraX += speed
        updateObstacles(speed)
        spawnObstacle()
    elif direction == "left":
        bgOffset -= speed
        worldDistance -= speed
        cameraX -= speed
        updateObstacles(-speed)

def displayHomeScreen():
    global musicStarted
    screen.blit(bg, (0, 0))# starting game title page
    pygame.draw.rect(screen, (0, 0, 0), playBtnRect)
    screen.blit(playBtn, (975, 675))
    if musicStarted == False: # using the flag to start the music, and play in a loop (-1)
        pygame.mixer.music.play(-1)
        musicStarted = True

def displayInstrucScreen():
    screen.blit(control, (0, 0)) # displaying the controls/instruction screen
    pygame.draw.rect(screen, (0, 0, 0), nextBtnRect)
    screen.blit(nextBtn, (500, 600))

def displayGameOver():
    global scores, scoreWritten
    # Display game over screen
    # Semi-transparent overlay, see through black layer
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128) #making it transparent, by changing opaqueness 0 = transparent, 255 = fully opaque
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Game over text
    font_large = pygame.font.Font("icons,sprites/m6x11.ttf", 72)
    font_medium = pygame.font.Font("icons,sprites/m6x11.ttf", 48)

    game_over_text = font_large.render("GAME OVER", True, (238, 5, 39))
    final_score_text = font_medium.render(f"Final Score: {score}", True, (242, 52, 215))
    final_distance_text = font_medium.render(f"Distance Traveled: {int(worldDistance)}", True, (186, 118, 255))
    restart_text = font_medium.render("Press R to Restart or ESC to Quit", True, (250, 226, 5))

    # Center the text
    #dividing the screen by 2, and subtracting the width of the
    # text itself to align perfect center by shift
    #USING .get_width() TO GET THE WIDTH, '{:^10}' doesn't work in pygame
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 100))
    screen.blit(final_score_text, (WIDTH//2 - final_score_text.get_width()//2, HEIGHT//2 - 20))
    screen.blit(final_distance_text, (WIDTH//2 - final_distance_text.get_width()//2, HEIGHT//2 + 20))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 80))

    """implementing files, starting condition is always allows to pass through
    using try and except blocks to prevent the program from stopping by IOError
    (when trying to input or output (IO) something and failing)"""
    if scoreWritten == False:
        scores.append(score)
        try:
            file = open("scores.txt", "w")  # Use "w" to overwrite
            file.write("All Scores:\n")  # Write header
            for s in scores:
                file.write(str(s) + "\n")
            file.close()
        except IOError:
            print("error, no file to write on")
        scoreWritten = True


def resetGame():
    #Reset all game variables for restart
    global kaelHealth, lumaHealth, score, obstacles, worldDistance, bgOffset, cameraX
    global kaelCollisionCooldown, lumaCollisionCooldown, nextObstacleDistance
    global kaelX, kaelY, lumaX, lumaY, scores, scoreWritten

    # Reset health and score
    kaelHealth = 5
    lumaHealth = 5
    score = 0
    scoreWritten = False

    # Reset collision cool downs
    kaelCollisionCooldown = 0
    lumaCollisionCooldown = 0

    # Reset world state
    obstacles = []
    worldDistance = 0
    bgOffset = 0
    cameraX = 0
    nextObstacleDistance = 500

    # Reset character positions
    kaelX = 300
    kaelY = 500
    lumaX = 320
    lumaY = 500

    print("All scores are saved! check scores.txt file to view")

def moveRightKael():
    global currentFrameKael, kaelX, lumaX

    """the instantaneous frame being displayed has to get 
    changed so that it can go through each index in the list of 
    movement to the respective character  """
    currentFrameKael += frameSpeed
    # when the index reaches out of the list, you reset to loop the movement
    if currentFrameKael >= len(kaelRun):
        currentFrameKael = 0

    # Move character, but check if we should scroll instead, by checking if Kael is near the
    # either edge of the screen.
    if kaelX < SCROLL_RIGHT_BOUNDARY:
        kaelX += 5
    else:
        # Character reached scroll boundary - scroll world instead
        scrollWorld("right", 5)
        lumaX -= 5
        if lumaX < SCROLL_LEFT_BOUNDARY:
            lumaX = SCROLL_LEFT_BOUNDARY
    screen.blit(kaelRun[int(currentFrameKael)], (kaelX, kaelY))

def moveLeftKael():
    global currentFrameKael, kaelX, lumaX

    # same logic but with flipped images for left
    currentFrameKael += frameSpeed
    if currentFrameKael >= len(kaelRun):
        currentFrameKael = 0

    # Move character, but check if we should scroll instead
    if kaelX > SCROLL_LEFT_BOUNDARY:
        kaelX -= 5
    else:
        # Character reached scroll boundary - scroll world instead
        scrollWorld("left", 5)
        lumaX += 5
        # Prevent Luma from going off-screen
        if lumaX > SCROLL_RIGHT_BOUNDARY:
            lumaX = SCROLL_RIGHT_BOUNDARY
    # using transform.flip function, with boolean tuples, for horizontal flip, hence True
    screen.blit(pygame.transform.flip(kaelRun[int(currentFrameKael)], True, False), (kaelX, kaelY))

def jumpRightKael(gravity, ground):
    global currentFrameKael, kaelX, kaelY, jump, velocityKael, lumaX

    currentFrameKael += frameSpeed
    if currentFrameKael >= len(kaelJump):
        currentFrameKael = 0
    # the velocity is -15, so really you're subtracting 15 from the y-value
    kaelY += velocityKael
    # while doing so, we also want to increase the velocity each time so,
    # we are subtracting less and less each time, bringing kael back to the ground
    velocityKael += gravity

    # Handle horizontal movement during jump
    if kaelX < SCROLL_RIGHT_BOUNDARY:
        kaelX += 3
    else:
        scrollWorld("right", 3)
        lumaX -= 3
        if lumaX < SCROLL_LEFT_BOUNDARY:
            lumaX = SCROLL_LEFT_BOUNDARY

    """ when the velocity becomes a positive int, and starts 
    bring kael down from GROUND LEVEL, we set kael's y back to the ground, reset jump 
    flag and velocity becomes -15 again to bring kael up when jump is true again"""
    if kaelY > ground:
        kaelY = ground
        jump = False
        velocityKael = -15

    screen.blit(kaelJump[int(currentFrameKael)], (kaelX, kaelY))

def jumpLeftKael(gravity, ground):
    # same logic but pasting flipped image
    global currentFrameKael, kaelX, kaelY, jump, velocityKael, lumaX
    currentFrameKael += frameSpeed
    if currentFrameKael >= len(kaelJump):
        currentFrameKael = 0

    kaelY += velocityKael
    velocityKael += gravity

    # Handle horizontal movement during jump
    if kaelX > SCROLL_LEFT_BOUNDARY:
        kaelX -= 3
    else:
        scrollWorld("left", 3)
        lumaX += 3
        if lumaX > SCROLL_RIGHT_BOUNDARY:
            lumaX = SCROLL_RIGHT_BOUNDARY

    if kaelY > ground:
        kaelY = ground
        jump = False
        velocityKael = -15

    screen.blit(pygame.transform.flip(kaelJump[int(currentFrameKael)], True, False), (kaelX, kaelY))

def hitRightKael():
    global currentFrameKael, kaelX, lumaX
    currentFrameKael += frameSpeed
    if currentFrameKael >= len(kaelHit):
        currentFrameKael = 0

    if kaelX < SCROLL_RIGHT_BOUNDARY:
        kaelX += 5
    else:
        scrollWorld("right", 5)
        lumaX -= 5
        if lumaX < SCROLL_LEFT_BOUNDARY:
            lumaX = SCROLL_LEFT_BOUNDARY

    screen.blit(kaelHit[int(currentFrameKael)], (kaelX, kaelY))

def hitLeftKael():
    global currentFrameKael, kaelX, lumaX
    currentFrameKael += frameSpeed
    if currentFrameKael >= len(kaelHit):
        currentFrameKael = 0

    if kaelX > SCROLL_LEFT_BOUNDARY:
        kaelX -= 5
    else:
        scrollWorld("left", 5)
        lumaX += 5

        if lumaX > SCROLL_RIGHT_BOUNDARY:
            lumaX = SCROLL_RIGHT_BOUNDARY

    screen.blit(pygame.transform.flip(kaelHit[int(currentFrameKael)], True, False), (kaelX, kaelY))

# EXACT SAME IDEA BUT WITH LUMA'S IMAGES
def moveRightLuma():
    global currentFrameLuma, lumaX, kaelX
    currentFrameLuma += frameSpeed
    if currentFrameLuma >= len(lumaRun):
        currentFrameLuma = 0

    if lumaX < SCROLL_RIGHT_BOUNDARY:
        lumaX += 5
    else:
        scrollWorld("right", 5)
        kaelX -= 5
        if kaelX < SCROLL_LEFT_BOUNDARY:
            kaelX = SCROLL_LEFT_BOUNDARY

    screen.blit(lumaRun[int(currentFrameLuma)], (lumaX, lumaY))

def moveLeftLuma():
    global currentFrameLuma, lumaX, kaelX
    currentFrameLuma += frameSpeed
    if currentFrameLuma >= len(lumaRun):
        currentFrameLuma = 0

    if lumaX > SCROLL_LEFT_BOUNDARY:
        lumaX -= 5
    else:
        scrollWorld("left", 5)
        kaelX += 5

    screen.blit(pygame.transform.flip(lumaRun[int(currentFrameLuma)], True, False), (lumaX, lumaY))

def jumpLeftLuma(gravity, ground):
    global currentFrameLuma, lumaX, lumaY, jumpL, velocityLuma, kaelX
    currentFrameLuma += frameSpeed
    if currentFrameLuma >= len(lumaJump):
        currentFrameLuma = 0

    lumaY += velocityLuma
    velocityLuma += gravity

    if lumaX > SCROLL_LEFT_BOUNDARY:
        lumaX -= 3
    else:
        scrollWorld("left", 3)
        kaelX += 3
        if kaelX < SCROLL_RIGHT_BOUNDARY:
            kaelX = SCROLL_RIGHT_BOUNDARY

    if lumaY > ground:
        lumaY = ground
        jumpL = False
        velocityLuma = -15

    screen.blit(pygame.transform.flip(lumaJump[int(currentFrameLuma)], True, False), (lumaX, lumaY))


def jumpRightLuma(gravity, ground):
    global currentFrameLuma, lumaX, lumaY, jumpL, velocityLuma, kaelX
    currentFrameLuma += frameSpeed
    if currentFrameLuma >= len(lumaJump):
        currentFrameLuma = 0

    lumaY += velocityLuma
    velocityLuma += gravity

    if lumaX < SCROLL_RIGHT_BOUNDARY:
        lumaX += 3
    else:
        scrollWorld("right", 3)
        kaelX -= 3

        if kaelX < SCROLL_LEFT_BOUNDARY:
            kaelX = SCROLL_LEFT_BOUNDARY

    if lumaY > ground:
        lumaY = ground
        jumpL = False
        velocityLuma = -15

    screen.blit(lumaJump[int(currentFrameLuma)], (lumaX, lumaY))

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if playBtnRect.collidepoint(event.pos):
                gameState = "introduction"
            elif nextBtnRect.collidepoint(event.pos):
                gameState = "begin"

        # Game over screen controls
        if gameState == "gameOver":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    resetGame()
                    gameState = "begin"
                elif event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    try:
                        file = open("scores.txt", "w")
                        file.write("")
                        file.close()
                    except IOError:
                        pass
                    sys.exit()

        # Kael controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moveRight = True
            elif event.key == pygame.K_LEFT:
                moveLeft = True
            elif event.key == pygame.K_UP:
                jump = True
                velocityKael = -15
            elif event.key == pygame.K_m:
                hit = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moveRight = False
            elif event.key == pygame.K_LEFT:
                moveLeft = False
            elif event.key == pygame.K_m:
                hit = False

        # Luma controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                moveRightL = True
            elif event.key == pygame.K_a:
                moveLeftL = True
            elif event.key == pygame.K_w:
                jumpL = True
                velocityLuma = -15

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                moveRightL = False
            elif event.key == pygame.K_a:
                moveLeftL = False

    if gameState == "home":
        displayHomeScreen()

    elif gameState == "introduction":
        displayInstrucScreen()

    elif gameState == "begin":
        # Check for game over
        if checkGameOver() == True: #FLAG FUNCTION WITH BOOLEAN VALUE RETURN
            gameState = "gameOver"
            continue

        # Draw infinite scrolling background
        drawInfiniteBackground()

        # Draw obstacles
        drawObstacles()

        # Handle collisions
        obstacleCollision()

        # Handle Kael's actions
        if jump:
            if moveLeft:
                jumpLeftKael(1, 500)
            else:
                jumpRightKael(1, 500)
        elif hit:
            if moveLeft:
                hitLeftKael()
            else:
                hitRightKael()
        elif moveLeft:
            moveLeftKael()
        elif moveRight:
            moveRightKael()
        else:
            screen.blit(kaelIdle[0], (kaelX, kaelY))

        # Handle Luma's actions
        if jumpL:
            if moveLeftL:
                jumpLeftLuma(1, 500)
            else:
                jumpRightLuma(1, 500)
        elif moveLeftL:
            moveLeftLuma()
        elif moveRightL:
            moveRightLuma()
        else:
            screen.blit(lumaIdle[0], (lumaX, lumaY))

        # Draw UI elements
        drawUI()

    elif gameState == "gameOver":
        # Keep drawing the last frame, and draw everything for the
        # next play (if user wants to play again)
        drawInfiniteBackground()
        drawObstacles()
        screen.blit(kaelIdle[0], (kaelX, kaelY))
        screen.blit(lumaIdle[0], (lumaX, lumaY))

        # Draw UI elements
        drawUI()

        # Draw game over screen on top
        displayGameOver()

    # Update display and control frame rate
    pygame.display.flip()
    clock.tick(30)  # 30 FPS

