# Vinter 2020 - grått och regnigt.
# I stället för att vänta på snön IRL ska vi skapa snöfall i Python!
# Din utmaning är att skapa ett så vintrigt snöfall som möjligt.

# 1. Installera pygame. Skriv i terminalen: pip install pygame
# 2. Skapa en mapp "Vinter" och lägg i den både den här filen (vinter.py) och bildfilen (flinga.png) 
# 3. Öppna mappen i Visual Studio Code genom att välja File > Open Folder...
# 4. Testa!
# 5. Ändra koden för att skapa det vintrigaste snöfallet. 

# Fungerar det inte? Hör av dig till Martin på Hangouts och berätta vilka felmeddelanden du får

import pygame, sys
from pygame.locals import *
import random

# -----Konstanter-----
GRAVITATION = 0.1

#Skärmens storlek
BREDD = 1200
HÖJD = 800

# bara för spelaren
FRIKTION = 0.98 


# -----Här är "ritningen" (klassen) för hur snöflingorna ska fungera-----
class Flinga:

    # Det här händer allra först när snöflingan skapas!
    def __init__(self, sprite, hastighet_x = 0, hastighet_y = 0, max_fallhastighet = 1, vind = 0):
        
        # Sätt snöflingan på en slumpad position OVANFÖR skärmen, så att den faller ovanifrån
        self.pos_x = random.randint(0, BREDD)
        self.pos_y = random.randint(-100, -10)
        
        self.hastighet_x = hastighet_x
        self.hastighet_y = hastighet_y
        self.max_fallhastighet = max_fallhastighet

        self.sprite = sprite 
 
    # Rita snöflingan
    def rita(self, screen):
        screen.blit(self.sprite,(self.pos_x, self.pos_y))

    # Uppdatera / Flytta på snöflingan
    def uppdatera(self):
        
        # Flingan faller snabbare
        self.hastighet_y += GRAVITATION

        # Begränsa hur snabbt flingan kan falla
        if self.hastighet_y > self.max_fallhastighet:
            self.hastighet_y = self.max_fallhastighet

        # Ändra hastighet i x-led så att flingan åker lite fram och tillbaka
        # self.hastighet_x += random.uniform(-0.8, 0.8)
        
        # Flytta på flingan
        self.pos_x += self.hastighet_x
        self.pos_y += self.hastighet_y

    # Har flingan fallit så långt att den inte längre syns på skärmen?
    def är_död(self):
        if self.pos_y > HÖJD:
            return True

        return False

# Här är ritningen/klassen för snöflingor slut
#---------------------------------    


# Starta pygame
pygame.init()

# Skärmen
screen = pygame.display.set_mode((BREDD,HÖJD))

# -----Player/Spelaren-----
player_sprite = pygame.image.load('mario.png')
player_position_x = 300
player_position_y = 200
player_hastighet_x = 1
player_hastighet_y = -2
player_stannar = True
player_hoppar = False

def rita_player():
    screen.blit(player_sprite,(player_position_x, player_position_y))


# Bildfilen för snöflingan
flinga_sprite = pygame.image.load('flinga.png')

# I den här listan hamnar alla snöflingor
flingor = []

# -----Spel-loopen-----
    # Har något hänt? "events"
    # Uppdatera game state
    # Rita ut på skärmen
while True:

    # Ska det skapas en ny snöflinga? I det här fallet är det en procents chans vid varje uppdatering
    # (Om ett slumptal mellan 0 och 99 blir 0),
    if random.randint(0, 100) == 0:
        # SKAPA EN NY SNÖFLINGA
        ny_flinga = Flinga(sprite = flinga_sprite, max_fallhastighet= 10, hastighet_x= 3)

        #Lägg till den nya snöflingan i listan
        flingor.append(ny_flinga)

        # Skriv ut i terminalen hur många snöflinga det finns. (Om du vill ha koll på hur många det finns)
        #print(len(flingor))


    # Uppdatera alla snöflinga
    for flinga in flingor:
        flinga.uppdatera()
        
        # Om en snöflinga är "död", ta bort den från listan
        if flinga.är_död():
            flingor.remove(flinga)


    #For-loop - den där get() ger alltså en LISTA med händelser. Kolla vilken TYP
    for event in pygame.event.get(): 
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Knapp nedtryck?
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                player_hastighet_x = -1
                player_stannar = False

            if event.key == K_RIGHT:
                player_hastighet_x = 1
                player_stannar = False

            # Hopp
            if event.key == K_UP:
                player_hastighet_y = -5

            # Används ej för tillfället
            if event.key == K_DOWN:
                player_position_y += 5

        #Knapp släppt?            
        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                #player_hastighet_x = 0
                player_stannar = True


    if player_stannar == True:
        player_hastighet_x *= FRIKTION

    player_hastighet_y += GRAVITATION

    # Flyttar spelaren!
    player_position_x += player_hastighet_x
    player_position_y += player_hastighet_y

    # Golv för spelaren
    if player_position_y > HÖJD - 100:
        player_position_y = HÖJD - 100
        player_hastighet_y = 0

    # Lite rött när spelaren rör sig åt sidan!
    röd = int(abs(player_hastighet_x) * 255)

    #-----Rita på skärmen-----

    # "Sudda ut" bakgrunden först.
    # Prova gärna att ta bort screen.fill-raden så får du ser varför den behövs! 
    #             R   G  B
    screen.fill((röd, 0, 0))
    
    # Rita spelaren
    rita_player()
    
    # Rita alla snöflingor
    for flinga in flingor:
            flinga.rita(screen)

    # Uppdatera skärmen så att alla förändringar syns!
    pygame.display.update()