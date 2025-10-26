import pygame,sys,random

def ball_animation():
    global ball_speed_x,ball_speed_y,player_score,opponent_score,score_time
    ball.x+=ball_speed_x
    ball.y+=ball_speed_y

    if ball.top<=0 or ball.bottom>=screen_height:
     ball_speed_y*=-1
    
    if ball.left<=0 :
      pygame.mixer.Sound.play(score_sound)
      player_score+=1
      score_time= pygame.time.get_ticks()

    if ball.right>=screen_width:
      pygame.mixer.Sound.play(score_sound)
      opponent_score+=1
      score_time= pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x>0 : 
       pygame.mixer.Sound.play(hit_sound)
       if abs(ball.right-player.left)<10 :
          ball_speed_x*=-1
       elif abs(ball.bottom-player.top)<10 and ball_speed_y>0:
          ball_speed_x*=-1
       elif abs(ball.top-player.bottom)<10 and ball_speed_y<0:
          ball_speed_x*=-1
       
    if ball.colliderect(opponent) and ball_speed_x<0: 
         pygame.mixer.Sound.play(hit_sound)
         if abs(ball.left-opponent.right)<10 :
          ball_speed_x*=-1
         elif abs(ball.bottom-opponent.top)<10 and ball_speed_y>0:
          ball_speed_x*=-1
         elif abs(ball.top-opponent.bottom)<10 and ball_speed_y<0:
          ball_speed_x*=-1
       
         

def player_animation():
   player.y+=player_speed
   if player.top<=0 :
       player.top=0
   if player.bottom>=screen_height:
       player.bottom=screen_height

def opponent_animation():
   opponent.y+=opponent_speed
   if opponent.top<=0 :
       opponent.top=0
   if opponent.bottom>=screen_height:
       opponent.bottom=screen_height


def ball_restart():
   global ball_speed_x,ball_speed_y,score_time

   current_time=pygame.time.get_ticks()
   ball.center=(screen_width/2,screen_height/2)

   if current_time-score_time<700:
      number_three =game_font.render("3",False,light_grey)
      screen.blit(number_three,(screen_width/2-10,screen_height/2-50))
   if 700<current_time-score_time<1400:
      number_two =game_font.render("2",False,light_grey)
      screen.blit(number_two,(screen_width/2-10,screen_height/2-50))
   if 1400<current_time-score_time<2100:
      number_one =game_font.render("1",False,light_grey)
      screen.blit(number_one,(screen_width/2-10,screen_height/2-50))
      
   if current_time-score_time<2100:
      ball_speed_x,ball_speed_y=0,0
   else :
        ball_speed_y=7*random.choice((1,-1))
        ball_speed_x=7*random.choice((1,-1))
        score_time=None

def game_over():
    global player_score, opponent_score, ball_speed_x, ball_speed_y, game_active, game_over_time
    

    current_time = pygame.time.get_ticks()
    elapsed = current_time - game_over_time

    # Stop the ball
    ball_speed_x = 0
    ball_speed_y = 0

    # Render centered text
    gameover_sound=pygame.mixer.Sound("gameover2.mp3")
    pygame.mixer.Sound.play(gameover_sound)
    game_over_text = game_font.render("GAME OVER", True, light_grey)
    text_rect = game_over_text.get_rect(center=(screen_width / 2, screen_height / 2-40))
    screen.blit(game_over_text, text_rect)

    # After 3 seconds, reset the game
    if elapsed > 3000:
        player_score = 0
        opponent_score = 0
        ball.center = (screen_width / 2, screen_height / 2)
        ball_speed_x = 7 * random.choice((1, -1))
        ball_speed_y = 7 * random.choice((1, -1))
        game_over_time = None
        game_active = True
        
pygame.mixer.pre_init(44100,-16,2,1024)
pygame.init()
clock=pygame.time.Clock()

screen_width=1290
screen_height=750
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Ping Pong')

ball=pygame.Rect(screen_width/2-15,screen_height/2-15,30,30)
player=pygame.Rect(screen_width-20,screen_height/2-70,10,140)
opponent=pygame.Rect(10,screen_height/2-70,10,140)

bg_color=pygame.Color('grey12')
light_grey=(200,200,200)

ball_speed_x=7*random.choice((1,-1))
ball_speed_y=7*random.choice((1,-1))   
player_speed=0
opponent_speed=0


 
player_score=0
opponent_score=0
game_font=pygame.font.Font("freesansbold.ttf",30)

score_time=None
game_active = True
game_over_time = None
hit_sound=pygame.mixer.Sound("bat.mp3")
score_sound=pygame.mixer.Sound("ding.mp3")
music=pygame.mixer.Sound("music2.mp3")
pygame.mixer.Sound.play(music)


running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_DOWN:
              player_speed+=7
           if event.key == pygame.K_UP:
              player_speed-=7
        if event.type == pygame.KEYUP:
           if event.key ==pygame.K_DOWN:
              player_speed-=7
           if event.key == pygame.K_UP:
              player_speed+=7
        if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_s:
              opponent_speed+=7
           if event.key == pygame.K_w:
              opponent_speed-=7
        if event.type == pygame.KEYUP:
           if event.key ==pygame.K_s:
              opponent_speed-=7
           if event.key == pygame.K_w:
              opponent_speed+=7
        if event.type==pygame.KEYDOWN:
           if event.key==pygame.K_ESCAPE:
             running=False
    
    
    screen.fill(bg_color)
    pygame.draw.rect(screen,light_grey,player)
    pygame.draw.rect(screen,light_grey,opponent)
    pygame.draw.ellipse(screen,light_grey,ball)
    pygame.draw.aaline(screen,light_grey,(screen_width/2,0),(screen_width/2,screen_height))
    
    if game_active:
      ball_animation()
      player_animation()
      opponent_animation()
      if score_time:
         ball_restart()
      if player_score==5 or opponent_score==5:
         game_active=False
         game_over_time=pygame.time.get_ticks()
    else:
       game_over()
       
    player_text =game_font.render(f"{player_score}",False,light_grey)
    screen.blit(player_text,(screen_width/2+20,screen_height/2-15))

    opponent_text =game_font.render(f"{opponent_score}",False,light_grey)
    screen.blit(opponent_text,(screen_width/2-40,screen_height/2-15))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()


