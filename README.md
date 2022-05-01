# Cyber X Infra
---


# Table des matières

1. ### [Introduction](#Introduction)
2. ### [Fonctionnalités](#Fonctionnalités)
3. ### [Installation](#Installation)
    1. #### [Infrastructure](#Infrastructure)
        1. #### [Pré-requis](#Pré-requis)
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