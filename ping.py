#! /usr/bin/env python3
import sys
from scapy.all import *
from r_conf import *

faireping ("37.187.176.161")


# commande tcpdump 
# tcpdump -i eth0 icmp -A
# -A afficher le paquet je vais voir pour le grep

# tcpdump -i eth0 src 172.27.32.1 -A -n  >>resultat_tcpdump.txt
# recupere seulement les paquets de lip source car sinon ca prend tous les paquets icmp
# -n supprime le renommage et affiche les adresse ip plus facile pour filtre

# il faut grep pour recuperer la derniere lettre et balancer le tous dans un fichier txt 

# grep '^E' re.txt
# print(my[-1:]) permet d'isoler le dernier caractere 

# le fichier qui récupere et traite les fichiers pour les reconstruire est opérationnelle sous le nom de grep.sh 
# donc d un coté on a le fichier .ping qui execute puis de l autre coté un tcp dump qui récupere et isole les icmp sur 
# un fichier txt puis on le traite avec le fichier sh

# tcpdump -i ens192 src 192.168.1.36 and icmp -A -n

# 
# 
# sudo tcpdump -i ens3 src 86.217.186.243 and icmp -A -n >> resultat_tcpdump.txt
# sudo tcpdump -i ens3 src 37.187.176.161 and icmp -A -n >> resultat_tcpdump.txt