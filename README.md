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
    2. #### [Attaque](#Attaque)

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

### 3.I Infrastructure

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

