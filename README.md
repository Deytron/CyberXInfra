# Cyber X Infra
---


# Table des matières

1. ### [Introduction](#Introduction)
2. ### [Fonctionnalités](#Fonctionnalités)
3. ### [Installation](#Installation)
    1. #### [Infrastructure](#Infrastructure)
        1. #### [Pré-requis](#Pré-requis)
        2. #### [Windows Server](#WindowsServer)
        3. #### [Clients Windows](#ClientsWindows)
        4. #### [Monitoring](#Monitoring)
    2. #### [Attaque](#Attaque)
        1. #### [Script ps1](#Pré-requis)
        2. #### [Script ps1 asministrator](#WindowsServer)
        3. #### [Script bat](#ClientsWindows)
        4. #### [Script .exe](#Monitoring)
        

# 1. Introduction

CyberXInfra est notre projet de B3 avec Adrien, Ange Brochard, Marc Texier et Romain Ranaivoson. Le projet consiste en la mise en place d'une infrastructure basique type entreprise et l'attaque de celle-ci via un facteur extérieur.

# 2. Fonctionnalités

- Utilisation du réseau interne pour la communication entre les machines
- Utilisation de VMWare ESXi pour la gestion des machines virtuelles
- Connexion au réseau interne par l'extérieur via Wireguard
- Mise en place de Windows Active Directory avec deux Domain Controllers pour la HA
- Utilisation de deux machines Windows 10 en tant que targets
- Utilisation de Check_MK pour le monitoring des machines et du réseau
- Check_MK est installé sur une autre machine Linux pour le monitoring
- Hack avec Excel, Cobalt Strike
- Exploitation de faille de la version 1903 de Windows

# 3. Installation

## 3.I Infrastructure

> Le déploiement de l'infrastructure ne peut se faire actuellement de manière automatisée. Ansible (ou autre) peut être envisagé comme évolution logique pour la mise en place de l'infrastructure.

### 3.I.A Pré-requis

1. Téléchargez : 
- [VMWare ESXi (création de compte nécessaire)](https://customerconnect.vmware.com/group/vmware/evalcenter?p=free-esxi7)
- ISO Windows 10 (version 1903) via Azure ou par les océans
- ISO Windows Server 2019 via Azure ou par les océans
- [ISO Rocky Linux Minimal](https://download.rockylinux.org/pub/rocky/8/isos/x86_64/Rocky-8.5-x86_64-minimal.iso)
- (Si besoin) [Wireguard](https://www.wireguard.com/install/)

2. Installez VMWare ESXi, puis créez les machines virtuelles suivantes :
- DC1 (Windows Server 2019, min. 4 Go de RAM, 2vCPU et 40Go disque)
- DC2 (Windows Server 2019, min. 4 Go de RAM, 2vCPU et 40Go disque)
- Machine1DEV (Windows 10 1903, min. 2 Go de RAM, 1vCPU et 30Go disque)
- Machine2ADMIN (Windows 10 1903, min. 2 Go de RAM, 1vCPU et 30Go disque)
- Monitoring (Linux, min. 1 Go de RAM, 1vCPU et 5Go disque)

### 3.I.B Windows Server

1. Une fois les machines virtuelles _DC_ créées, installez Windows sur les deux machines. Pas besoin de clé produit.

2. Procédez sur les deux machines à la mise en place des services et la création d'une forêt :

    1. Rendez-vous dans le gestionnaire de serveurs (la fenêtre s'ouvre normalement totue seule au lancement)
    ![](https://i.imgur.com/A9gMqv5.png)

    2. Cliquez sur Gérer > Ajouter des rôles et fonctionnalités

    3. Installez au moins le service AD DS et DNS, puis faites suivant

    4. Une fois l'installation terminée, cliquez sur l'alerte en haut à droite de la fenêtre > Promouvoir le serveur en contrôleur de domaine

    5. Si vous êtes sur le DC1, créez une forêt au passage. Sinon, ajoutez le serveur dans un domaine existant. Nommez le domaine comme vous voulez, pour notre part ça a été "malgache.local".

    6. Mettez les mots de passe de restauration, suivant, blabla et boum ! Redémarrez le PC.

3. Une fois le domaine créé, vous devrez faire quelques réglages réseau :

    1. Clic droit en bas à droite > Ouvrir les paramètres réseau et Internet

    2. Allez dans Ethernet > Modifier les options d'adaptateur > Clic droit sur votre carte Ethernet
    
    3. **Désactivez l'IPv6**. C'est pas forcément nécessaire, mais selon votre réseau ça peut tout casser

    4. Cliquez sur Protocole Internet IPv4 > Propriétés, puis changez les paramètres comme suit :
    
    ```
    Adresse IP : Choisissez celle que vous souhaitez
    Masque de sous-réseau : Adapté selon votre réseau
    Passerelle : La passerelle de votre routeur

    DNS Principal : 127.0.0.1
    DNS Secondaire : 8.8.8.8 ou autre
    ```

    > Théorie : il n'est pas nécessaire de mettre localhost en DNS, mais bon on sait jamais

    ![](https://i.imgur.com/4dHIgSV.png)

4. Vos clients n'auront pas d'accès Internet. Pour remédier à ça, dans le gestionnaire de serveurs :

    1. Cliquez sur Outils > DNS

    2. Clic droit sur **WIN-XXXXXX** > Propriétés > Redirecteurs

    3. Ajoutez en redirecteur l'adresse passerelle de votre routeur, puis appliquez

5. Pour lier les deux contrôleurs de domaine :

    1. Dans le gestionnaire de serveurs, cliquez sur Ajouter d'autres serveur à gérer

    2. Entrez l'adresse IP du DC2, et inversement dans le DC2, entrez l'adresse du DC1



### 3.I.C Clients Windows

1. Une fois les machines Windows 10 créées, installez Windows sur les deux machines. Pas besoin de clé produit. Choisissez un nom d'utilisateur random dont vous vous souviendrez.

2. Clic droit en bas à droite > Ouvrir les paramètres réseau et Internet

    1. Allez dans Ethernet > Modifier les options d'adaptateur > Clic droit sur votre carte Ethernet
    
    2. **Désactivez l'IPv6**. C'est pas forcément nécessaire, mais selon votre réseau ça peut tout casser

    3. Cliquez sur Protocole Internet IPv4 > Propriétés, puis changez les paramètres comme suit :
    
    ```
    Adresse IP : Choisissez celle que vous souhaitez
    Masque de sous-réseau : Adapté selon votre réseau
    Passerelle : La passerelle de votre routeur

    DNS Principal : L'adresse IP du DC1
    DNS Secondaire : L'adresse IP du DC2
    ```

3. Pour ajouter le PC client dans le domaine Active Directory : 

    1. Allez dans Paramètres > Comptes > Comptes Scolaires ou Professionnel > Ajouter un compte

    2. Ajoutez le nom de domaine, entrez en nom d'utilisateur votre user du DC1 et votre mot de passe, puis redémarrez la machine

4. Installez Microsoft Office sur le PC. Légalement ou illégalement, peu importe

### 3.I.D Monitoring

1. Une fois la machine Linux créée, installez Rocky Linux sur la machine. User et mot de passe au choix, activez Internet et c'est parti

2. Pour installer Check_MK, l'outil de monitoring, utilisez en tant que sudo les commandes suivantes :

```bash
dnf install https://download.checkmk.com/checkmk/2.0.0p23/check-mk-raw-2.0.0p23-el8-38.x86_64.rpm
omd create website
```

3. Une fois installé, lancez l'interface de monitoring avec `omd start website`

4. Dans votre navigateur, rendez-vous sur http://IPMACHINE/website/ et connectez-vous avec les credentials donnés lors de la création du site

5. Vous pouvez ajouter des hôtes et customiser votre dashboard comme vous le souhaitez pour surveiller votre réseau. Seulement, si vous souhaitez surveiller un hôte, vous devez installer l'agent de surveillance.

    1. Sur les Windows, utilisez cette commandes Powershell :
    ```
    $client = New-Object System.Net.WebClient
    $client.DownloadFile("http://IPMACHINE/monitorsite/check_mk/agents/windows/check_mk_agent.msi", .\check_mk_agent.msi)
    ```

    2. Double cliquez sur le fichier check_mk_agent.msi et suivez les instructions

    Notre dashboard ressemble à ceci, très basique

    ![](https://i.imgur.com/CLf9Nhr.png)

## 3.II Attaque

L'attaque se déroule en trois étapes: 

- La première étape est une campagne de phishing. Quoi de mieux étant donné que, dans le monde, plus de 90% des données volées sont dûes à une campagne de phishing.
- Dans la deuxième partie, il y aura un fichier Excel dans le mail pour Martine de la compta qui l'ouvrira. Celui-ci cachera un fichier.exe, 2 fichiers ps1 et un fichier bat.
- La troisième partie utilisera un script qui se lancera pour pousser le .exe sur la GPO.

### 1. init.ps1

Le fichier init.ps1 est le fichier qui va être téléchargé en premier, il permet de venir chercher one.ps1 et l'executer en admin, ce qui nous permettera de désactiver defender puisque notre victime est admin local de sa machine. 

### 2. one.ps1 administrator

Comme vu au dessus, ce script va permettre plusieurs choses, dans un premier temps, on vient désactiver defender et on ajoute une exception dans C:\windows\Temp au cas ou defender se réactive etc etc. Ensuite on vient télécharger le script d'ange, le .exe, expliqué juste après. On télécharge aussi notre beacon cobalt strike, c2.bat, et on vient lancer ces 2 scripts ce qui va nous  permettre d'obtenir un "shell" et de faire noetre pivot vers le domain controller.   

### 3. c2.bat

c2.bat est juste la commande powershell généré via cobalt strike

### 4.exe
PS (nous avons upload les py le .exe est le résultats de la compilation entre ping et r_conf)
Ce .exe écrit en Python se nomme "Windows coolsence" pour paraître inaperçu. Après son exécution, il récupère l'output de la commande `ipconfig/all` du PC, le converti en base64, puis envoie 32 caractères ping par ping sur un VPS. Sur la partie VPS, l'attaquant a ouvert deux fenêtres, une avec un tcpdump comme cela :

```sudo tcpdump -i ens3 src XXX.XXX.XXX.XXX and icmp -A -n >> resultat_tcpdump.txt```

Le `-A` récupère les paquets, le `-n` résout les adresses IP puis le tout est exporté dans `resultat_tcpdump.txt`.
Pour la src, si vous avez l'adresse IP de la machine c'est plus simple, autrement vous mettez la vôtre car le ping renverra les caractères également, donc vous pourrez les récupérer.

Et une deuxième fenêtre dans >> pour avoir une fenêtre verbeuse, histoire de savoir quand l'attaque sera finie.
Une fois terminé, l'attaquant éxécutera un script Bash qui récupèrera le `resultat_tcpdump.txt` pour reformer le fichier en base 64.
