#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, pygame, random, math, time, string, logging
from pygame.locals import *
from espeak import espeak

log = logging.getLogger('Contando con JAMCito run')
log.setLevel(logging.DEBUG)

class JamcitO(pygame.sprite.Sprite):
	
	def __init__(self):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.image = pygame.image.load("datos/terron.png")
		self.rect = self.image.get_rect(center = (450, 300))

	def update(self):
		self.rect.centerx = pygame.mouse.get_pos()[0]
		self.rect.centery = pygame.mouse.get_pos()[1]	

class Estrella(pygame.sprite.Sprite):
	
	def __init__(self,centro,imagen):
		pygame.sprite.Sprite.__init__(self, self.containers)
		self.image=pygame.image.load(imagen)
		self.rect=self.image.get_rect(center=centro)

class Estrellita(pygame.sprite.Sprite):
	
	def __init__(self,centro,imagen):
		pygame.sprite.Sprite.__init__(self,self.containers)
		self.image=pygame.image.load(imagen)
		self.rect=self.image.get_rect(center=centro)



#Funciones para preguntar
def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass

def display_box(screen, message,maxcar):
  fontobject = pygame.font.Font("datos/fuente.ttf",70)
  pygame.draw.rect(screen, (255,0,0),
                   ((screen.get_width() / 2) - 44*maxcar/2,
                    (screen.get_height() / 2) - 10,
                    40*maxcar,72), 0)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 44*maxcar/2-2,
                    (screen.get_height() / 2) - 12,
                    40*maxcar+4,76), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (0,0,0)),
                ((screen.get_width() / 2) - 44*maxcar/2+4, (screen.get_height() / 2) - 10))
  pygame.display.flip()

def pregunta(pantalla,maxcar,numerico):
  pygame.font.init()
  current_string = []
  display_box(pantalla, string.join(current_string,""),maxcar)
  while 1:
    tecla = get_key()
    if tecla == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif tecla == K_RETURN:
      break
    elif tecla == K_MINUS:
      current_string.append("_")
    elif ( (numerico)  )  and \
           len(current_string)<maxcar:
      current_string.append(chr(tecla))
    display_box(pantalla,string.join(current_string,""),maxcar)
  return string.join(current_string,"")


#bucle principal del juego
#def juego(pantalla,idioma,nombre):
def main(pantalla,idioma):
	global habla, diccionario
	objeto=diccionario[random.randrange(len(diccionario))]
	#define la fuente:
	fuente1 = pygame.font.Font("datos/fuente.ttf",45)

	#define los objetos del juego
	fondo = pygame.image.load(objeto["fondo"])
	todos = pygame.sprite.RenderUpdates()
	estrellas = pygame.sprite.Group()
	jam = pygame.sprite.Group()
	JamcitO.containers = jam,todos
	Estrella.containers = estrellas,todos
	Estrellita.containers = estrellas,todos
	jamcito=JamcitO()
	mano_der=(140-5,30-5)
	mano_izq=(140-250,30-250)
	#define los posibles centros de las estrellas
	centros=[]
	for cy in range(50,501,90):
		for cx in range(50,851,100):
			centros+=[(cx+random.randrange(-10,11),cy+random.randrange(-10,11))]
	#crea una cantidad aleatoria de estrellas en lugares aleatorios
	numero1=random.randrange(15)
	for i in range(numero1):
		donde=random.randrange(len(centros))
		Estrella(centros[donde],objeto["imageng"])
		del centros[donde]
	#define los centros para las estrellas que se van contando
	centros=[]
	for cx in range(400,860,30):
		centros+=[(cx,800)]
	#al principio no se han contado estrellas
	cuenta=0
	#define la velocidad del juego
	reloj = pygame.time.Clock()
	CUADROS_POR_SEGUNDO = 60
	#decir las instrucciones
	if idioma=="ES":
#		habla.synth(objeto["cuenta"][idioma]+", "+nombre)
		habla.synth(objeto["cuenta"][idioma]+", ")
	elif idioma=="EN":
		habla.synth(objeto["cuenta"][idioma]+", ")
		habla.set_voice("es-la")
#		habla.synth(nombre)
		habla.set_voice("en-us")
	elif idioma=="FR":
		habla.synth(objeto["cuenta"][idioma]+", ")
		habla.set_voice("es-la")
#		habla.synth(nombre)
		habla.set_voice("fr")
	#ciclo principal del juego
	while True:
		reloj.tick(CUADROS_POR_SEGUNDO)
		todos.update()
		pos_hombre=(jamcito.rect.centerx,jamcito.rect.centery)
		pmi=(pos_hombre[0]-mano_izq[0],pos_hombre[1]-mano_izq[1])
		pmd=(pos_hombre[0]-mano_der[0],pos_hombre[1]-mano_der[1])
		for evento in pygame.event.get():
			if evento.type == QUIT:
				pygame.quit()
				return
			if evento.type == MOUSEBUTTONDOWN:
				for i in estrellas:
					dizq = math.sqrt((pmi[0]-i.rect.centerx)**2 + (pmi[1]-i.rect.centery)**2)
					dder = math.sqrt((pmd[0]-i.rect.centerx)**2 + (pmd[1]-i.rect.centery)**2)			
					if dizq<30.0:
						i.kill()
						Estrellita(centros[cuenta],objeto["imagenp"])
						cuenta+=1
						if cuenta==1:
							habla.synth(objeto["singular"][idioma])
						else:
							habla.synth(str(cuenta)+" "+objeto["plural"][idioma])
						time.sleep(1)
					if dder<30.0:
						i.kill()
						Estrellita(centros[cuenta],objeto["imagenp"])
						cuenta+=1
						if cuenta==1:
							habla.synth(objeto["singular"][idioma])
						else:
							habla.synth(str(cuenta)+" "+objeto["plural"][idioma])
						time.sleep(1)						
		pantalla.blit(fondo, (0,0) )
		todos.draw(pantalla)
		if idioma=="ES":
			ren = fuente1.render(u"Has contado:", 1, (0, 0, 0))
		elif idioma=="EN":
			ren = fuente1.render(u"You have counted:", 1, (0,0,0))
		elif idioma=="FR":
			ren = fuente1.render(u"T'as compté:", 1, (0,0,0))
		pantalla.blit(ren,(5,780))
		pygame.display.flip()
		if cuenta==numero1:
			jamcito.rect.centerx=600
			jamcito.rect.centery=400
			pantalla.blit(fondo, (0,0) )
			todos.draw(pantalla)
			if idioma=="ES":
				ren = fuente1.render(u"Has contado:", 1, (0, 0, 0))
			elif idioma=="EN":
				ren = fuente1.render(u"You have counted:", 1, (0,0,0))
			elif idioma=="FR":
				ren = fuente1.render(u"T'as compté:", 1, (0,0,0))
			pantalla.blit(ren,(5,780))
			pygame.display.flip()
			if idioma=="ES":
#				habla.synth("Muy bien "+nombre)
				habla.synth("Muy bien ")
				habla.synth(objeto["hascontado"][idioma])
				time.sleep(4)
				habla.synth(objeto["cuantas"][idioma])
				time.sleep(2)
			elif idioma=="EN":
				habla.synth("Well done")
				habla.set_voice("es-la")
#				habla.synth(nombre)
				habla.set_voice("en-us")
				habla.synth(objeto["hascontado"][idioma])
				time.sleep(4)
				habla.synth(objeto["cuantas"][idioma])
				time.sleep(2)
			elif idioma=="FR":
				habla.synth("Bien fait")
				habla.set_voice("es-la")
#				habla.synth(nombre)
				habla.set_voice("fr")
				habla.synth(objeto["hascontado"][idioma])
				time.sleep(4)
				habla.synth(objeto["cuantas"][idioma])
				time.sleep(2)
			usuario=pregunta(pantalla,2,True)
			if int(usuario)==numero1:
				if idioma=="ES":
#					habla.synth("Has contado bien "+nombre)
					habla.synth("Has contado bien ")
				elif idioma=="EN":
					habla.synth("Your count is correct ")
					habla.set_voice("es-la")
#					habla.synth(nombre)
					habla.set_voice("en-us")
				elif idioma=="FR":
					habla.synth("Tu as bien compté ")
					habla.set_voice("es-la")
#					habla.synth(nombre)
					habla.set_voice("fr")
			else:
				if idioma=="ES":
					habla.synth("No. Intenta de nuevo.")
				elif idioma=="EN":
					habla.synth("No. Try again.")
				elif idioma=="FR":
					habla.synth("Non. Essaie une fois de plus.")
			time.sleep(3)
			return

idioma="ES"
#nombre="Cristofer"
#inicializa diccionarios
diccionario= [ {"fondo" : "datos/fondo.png",
				"imageng" : "datos/estrella.png",
				"imagenp" : "datos/estrellita.png",
				"cuenta": {"ES":"Cuenta las estrellas",
						   "EN":"Count the stars",
						   "FR":"Compte les étoiles"},
				"singular" : {"ES":"una estrella",
						      "EN":"one star",
						      "FR":"une étoile"},
				"plural" : {"ES":"estrellas","EN":"stars","FR":"étoiles"},
				"hascontado": {"ES":"Has contado todas las estrellas.", 
				               "EN":"You counted all the stars.",
				               "FR":"Tu as compté toutes les étoiles."},
				"cuantas": {"ES":"¿Cuantas estrellas contaste?",
				            "EN":"How many stars did you count?",
				            "FR":"Combien des étoiles as-tu compté?"} },
			   {"fondo": "datos/fondo.png",
			    "imageng" : "datos/flor.png",
			    "imagenp" : "datos/florcita.png",
			    "cuenta" : {"ES":"Cuenta las flores",
						    "EN":"Count the flowers",
						    "FR":"Compte les feurs"},
			    "singular" : {"ES":"una flor",
			                  "EN":"one flowers",
			                  "FR":"un feurs"},
			    "plural" : {"ES":"flores","EN":"flowers","FR":"feurs"},
			    "hascontado": {"ES":"Has contado todas las flores.",
			                   "EN":"You counted all the flowers.",
			                   "FR":"Tu as compté tous les feurs."},
			    "cuantas" : {"ES":"¿Cuantas flores contaste?",
							 "EN":"How many flowers did you count?",
							 "FR":"Combien des fleurs as-tu compté?"} },
			   
			    {"fondo": "datos/fondo.png",
			    "imageng" : "datos/mariposa.png",
			    "imagenp" : "datos/mariposita.png",
			    "cuenta" : {"ES":"Cuenta las mariposas",
						    "EN":"Count the butterflys",
						    "FR":"Compte les feurs"},
			    "singular" : {"ES":"una mariposa",
			                  "EN":"one butterfly",
			                  "FR":"un feurs"},
			    "plural" : {"ES":"mariposas","EN":"butterflys","FR":"feurs"},
			    "hascontado": {"ES":"Has contado todas las mariposas.",
			                   "EN":"You counted all the butterflys.",
			                   "FR":"Tu as compté tous les feurs."},
			    "cuantas" : {"ES":"¿Cuantas mariposas contaste?",
							 "EN":"How many butterfly did you count?",
							 "FR":"Combien des fleurs as-tu compté?"} } ]

#inicializa el sintetizador de voz
habla=espeak
if idioma=="ES":
	habla.set_voice("es-la")
elif idioma=="EN":
	habla.set_voice("en-us")
elif idioma=="FR":
	habla.set_voice("fr")
habla.set_parameter(habla.core.parameter_RATE,140,False)
habla.set_parameter(habla.core.parameter_VOLUME,80,False)
#inicializa pygame
pygame.init()
#define las dimensiones y crea la ventana (pantalla)
dimensiones = ancho, alto = 1200, 900
pantalla = pygame.display.set_mode(dimensiones)
#apaga el cursor
pygame.mouse.set_visible(0)
#pon la musica
while True:
	main(pantalla,idioma)
