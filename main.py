# TEE PELI TÄHÄN
import pygame
import random

#HUOMIO:
#PELIN HAHMOA SIIRRETÄÄN VASEMMALLE JA OIKEALLE NÄPPÄIMILLÄ A JA D!

class TasoHyppelyPeli:
    def __init__(self):

        # Pygame alustus
        pygame.init()
        pygame.display.set_caption("Hyppelypeli")
        self.naytto=pygame.display.set_mode((400, 500))
        self.kello=pygame.time.Clock()

        # Pisteet
        self.pisteet=0

        # Pelaaja
        self.pelaaja=Pelaaja(200,450)

        # Pelaajaryhmä
        self.pelaaja_ryhma=pygame.sprite.Group()
        self.pelaaja_ryhma.add(self.pelaaja)
        
        # Tasojen tiedot
        self.taso_kuva=pygame.image.load("Kuvat/ovi.png").convert_alpha()
        self.max_taso_maar=10
        self.tasot=pygame.sprite.Group()
        self.taso=Taso(200,495,120,self.taso_kuva)
        self.tasot.add(self.taso)

        # Kolikkojen tiedot
        self.kolikko_kuva=pygame.image.load("Kuvat/kolikko.png").convert_alpha()
        self.max_kolikko_maar=1
        self.kolikot=pygame.sprite.Group()
        self.kolikko=Kolikko(random.randint(0,400-self.kolikko_kuva.get_height()),random.randint(-200,-150),self.kolikko_kuva)
        self.kolikot.add(self.kolikko)
        self.kerätyt_kolikot=0
        

        # Suorita peli
        self.pelin_silmukka()

    #Luodaan tasot
    def luo_tasoja(self):
        if len(self.tasot)<self.max_taso_maar:
            leveys = random.randint(50,80)
            x_paikka = random.randint(20,400-leveys)
            y_paikka = self.taso.rect.top - random.randint(80,120)
            self.taso = Taso(x_paikka, y_paikka, leveys, self.taso_kuva)
            self.tasot.add(self.taso)


    # Pisteiden päivittäminen
    def paivita_pisteet(self):
        if self.pelaaja.siirron_maar>0:
            self.pisteet+=round(self.pelaaja.siirron_maar/20)
        

    # Kirjaa pisteet näytölle
    def kirjaa_pisteet(self):
        fontti = pygame.font.SysFont("Arial", 18)
        teksti = fontti.render("Pisteet: "+str(self.pisteet), True, (0, 0, 0))
        teksti2 = fontti.render("Kerätyt kolikot: "+str(self.kerätyt_kolikot), True, (0,0,0))
        self.naytto.blit(teksti, (0, 5))
        self.naytto.blit(teksti2, (0,20))
    
    # Hyppääminen tasolta toiselle
    def hyppy_tasolta(self):
        for taso in self.tasot:
            if taso.rect.colliderect(self.pelaaja.rect.x,self.pelaaja.rect.y+self.pelaaja.y_muutos,25,40):
                if self.pelaaja.rect.bottom<taso.rect.centery:
                    if self.pelaaja.vauhti_y>0:
                        self.pelaaja.rect.bottom=taso.rect.top
                        self.pelaaja.y_muutos=0
                        self.pelaaja.vauhti_y=-20
    
    # Kolikkojen luonti
    def luo_kolikkoja(self):
        if len(self.kolikot)<self.max_kolikko_maar:
            x_paikka=random.randint(0,400-self.kolikko_kuva.get_width())
            y_paikka=self.kolikko.rect.top - random.randint(1000,2000)
            self.kolikko=Kolikko(x_paikka, y_paikka, self.kolikko_kuva)
            self.kolikot.add(self.kolikko)

    # Kolikkojen kerääminen
    def keraa_kolikko(self):
        for kolikko in self.kolikot:
            if kolikko.rect.colliderect(self.pelaaja.rect.x,self.pelaaja.rect.y+self.pelaaja.y_muutos,25,40):
                self.pelaaja.y_muutos=0
                self.pelaaja.vauhti_y=-50
                self.kerätyt_kolikot+=1
                kolikko.poista()



    # Pelin silmukka ja logiikka
    def pelin_silmukka(self):
        pyorita=True
        while pyorita:
            siirron_maar=self.pelaaja.hahmon_liike()
            self.hyppy_tasolta()
            self.keraa_kolikko()
            for taso in self.tasot:
                taso.paivita(siirron_maar)
            for kolikko in self.kolikot:
                kolikko.paivita(siirron_maar)
            self.luo_tasoja()
            self.luo_kolikkoja()
            self.paivita_pisteet()

            self.naytto.fill((255,255,255))
            self.tasot.draw(self.naytto)
            self.kolikot.draw(self.naytto)
            self.kirjaa_pisteet()
            self.pelaaja_ryhma.draw(self.naytto)
            

            if self.pelaaja.rect.top>600:
                fontti = pygame.font.SysFont("Arial", 18)
                fontti2 = pygame.font.SysFont("Arial", 16)
                teksti = fontti.render("Peli on ohi. Keräsit "+str(self.pisteet) +" pistettä ja "+str(self.kerätyt_kolikot)+" kolikkoa.", True, (255, 255, 255))
                teksti2 = fontti2.render("Poistu painamalla 'Esc' ja aloita uudestaan painamalla 'Space'", True, (255,255,255))
                self.naytto.fill((30, 30, 30))
                self.naytto.blit(teksti, (5, 250))
                self.naytto.blit(teksti2, (5,285))

            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_SPACE: # Uuden pelin alustus
                        self.kerätyt_kolikot=0
                        self.pisteet=0
                        self.tasot.empty()
                        self.taso=Taso(200,495,120,self.taso_kuva)
                        self.tasot.add(self.taso)
                        self.kolikot.empty()
                        self.kolikko=Kolikko(random.randint(0,400-self.kolikko_kuva.get_height()),random.randint(-200,-150),self.kolikko_kuva)
                        self.kolikot.add(self.kolikko)
                        self.pelaaja.rect.center=(200,450)
                        self.pelaaja.x_muutos=0
                        self.pelaaja.y_muutos=0
                        self.pelaaja.vauhti_y=0
                        self.pelaaja.siirron_maar=0
                    if tapahtuma.key == pygame.K_ESCAPE: #Poistu pelistä
                        pyorita=False
        

            pygame.display.flip()
            self.kello.tick(60)

# Hahmon luonti peliin:
class Pelaaja(pygame.sprite.Sprite):    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Hahmon alkuasema
        self.x=x
        self.y=y

        # Loputtoman kiipeämisen muuttujat
        self.taustan_siirron_raja=100

        # Hahmon liikkeen muuttujat
        self.vauhti_y=0
        self.x_muutos=0
        self.y_muutos=0
        self.kiihtyvyys_y=1
        self.max_y=0

        # Hahmon kuva
        self.image=pygame.image.load("Kuvat/robo.png").convert_alpha()
        self.image=pygame.transform.scale(self.image,(25,40)) #Skaalataan kuvasta pienempi
        self.rect=pygame.Rect(0,0,15,40)
        self.rect.center=(self.x,self.y)
    
    def hahmon_liike(self):
        self.x_muutos=0
        self.y_muutos=0
        self.kiihtyvyys_y=1

        self.siirron_maar=0
        

        # Sivuttaisen liikkeen määrittäminen
        nappain=pygame.key.get_pressed()
        if nappain[pygame.K_a]:
            self.x_muutos=-10
        if nappain[pygame.K_d]:
            self.x_muutos=10

        # Seinään törmääminen
        if self.rect.left+self.x_muutos<0:
            self.x_muutos=0
        if self.rect.right+self.x_muutos>400:
            self.x_muutos=0
        
        # Alaspäin siirtyvän liikkeen pysäyttäminen tarpeeksi korkealla,
        # jotta tausta ja siten tasot eivät siirry ylöspäin
        if self.rect.top <= self.taustan_siirron_raja:
            if self.vauhti_y < 0:
                self.siirron_maar=-self.vauhti_y

        # Liike johtuen painovoimasta
        self.vauhti_y+=self.kiihtyvyys_y
        self.y_muutos+=self.vauhti_y+self.siirron_maar

        # Päivitä paikka
        self.rect.x+=self.x_muutos
        self.rect.y+=self.y_muutos
        self.mask=pygame.mask.from_surface(self.image)

        return self.siirron_maar
        

class Taso(pygame.sprite.Sprite):
    def __init__(self, x, y,leveys, kuva):
        pygame.sprite.Sprite.__init__(self)
        self.leveys=leveys
        self.image=kuva
        self.image=pygame.transform.scale(self.image, (self.leveys,10))
        self.rect=pygame.Rect(0,0,(8*self.leveys)//10,8)
        self.rect.center=(x,y)
        self.mask=pygame.mask.from_surface(self.image)

    
    def paivita(self,siirron_maar):
        self.rect.y += siirron_maar

        if self.rect.y > 500:
            self.kill()

class Kolikko(pygame.sprite.Sprite):
    def __init__(self, x, y, kuva):
        pygame.sprite.Sprite.__init__(self)
        self.image=kuva
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

    def paivita(self,siirron_maar):
        self.rect.y += siirron_maar

        if self.rect.y > 500:
            self.kill()
    
    def poista(self):
        self.kill()
    



if __name__=="__main__":
    TasoHyppelyPeli()