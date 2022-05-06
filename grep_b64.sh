 #!/bin/bash
 grep -v "192.168.1.31" resultat_tcpdump.txt >> resultat2_tcpdump.txt 
 for line in $(cat resultat2_tcpdump.txt); do echo "$line"|sed -r "s/\t//ig" >> newresultat_tcpdump.txt;done
 rm resultat2_tcpdump.txt
 #le b est le compteur pour le while 
 #tant que b n est pas égale au nombre de ligne le boucle ne s'arrete pas
 b=0
 c=$(wc -l newresultat_tcpdump.txt)
 while [[ $b < $c ]]; 
 do 
	b=$(($b+1))
	#si c est une ligne comptant les 60 caracteres de la lignes on pousse sur le fichier sinon
	#on enléve le retour a la ligne et on en rajoute a la fin pour pas avoir tous collé 
	for line in $(cat newresultat_tcpdump.txt); 
	do
		a=$(echo "$line" | wc -c)
		if [[ $a == 61 ]];
		then
			echo "$line" >> base.txt
			b=$(($b+1))
			echo $b
		else 
			echo "$line"| tr -d "\n" |echo -e "\n">> base.txt
			b=$(($b+1))
			echo $b
		fi
	done
 done 
 tail -n1 newresultat_tcpdump.txt >> base.txt
 #on prend la deriere ligne qui ne fais pas 60
 rm newresultat_tcpdump.txt
 for line in $(cat base.txt); do echo "$line"| sed -r "s/\t//ig"| sed 's/\(.*\)\(.\{32\}\)/\2/' | tr -d "\n" >> resultat_b64.txt ;done
 rm base.txt
 # ici restitution en base 64
 #le deuxieme sed récupère les  32 derniers caractere de la ligne et le premier enlève les tabulations