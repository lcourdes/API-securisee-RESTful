# Créez une API sécurisée RESTFUL en utilisant Django Rest
Projet 10 de la formation Openclassrooms Développeur d'application Python

## Description
Ce projet a pour objectif de répondre à la demande d'une société d'édition de logiciels de développement et de collaboration qui a décidé de publier une application permettant de remonter et suivre des problèmes techniques (issue tracking system). Cette solution s’adresse à des entreprises clientes, en B2B.

Les applications permettront essentiellement aux utilisateurs de créer divers projets, d'ajouter des utilisateurs à des projets spécifiques, de créer des problèmes au sein des projets et d'attribuer des libellés à ces problèmes en fonction de leurs priorités, de balises, etc.

Les applications doivent pouvoir exploiter les points de terminaison de l'API qui serviront les données.
Ce répertoire contient l'API développée pour répondre à ce besoin.

Remarques :
- L'authentification JWT (JSON Web Token) est utilisée pour authentifier les utilisateurs.
- L'API respecte des mesures de sécurité OWASP

## Procédure d'installation

### Import du dépôt Github
Dans un dossier de travail, importez le dépôt github puis, changez de répertoire courant pour vous positionner dans le répertoire cloné. 
```sh
$ git clone https://github.com/lcourdes/API-securisee-RESTful.git
$ cd API-securisee-RESTful.git
```

### Création d'un environnement virtuel
Il est recommandé d'installer un environnement virtuel. Pour ce faire, suivez les instructions 
ci-dessous :

- S'il ne l'est pas déjà, installez le package *virtualenv* :
```sh
$ pip install virtualenv
```

- Créez un environnement de travail et activez-le :
```sh
$ python3 -m venv env
$ source env/bin/activate
```

### Installation des librairies
Installez les librairies nécessaires au bon fonctionnement du programme à l'aide du fichier requirements.txt :
```sh
$ pip install -r requirements.txt
```

### Lancement du serveur

Pour démarrer le programme, déplacez-vous dans le projet Django et démarrer le serveur :
```sh
$ cd application
$ python3 manage.py runserver
```

L'adresse est fournie dans le terminal et peut être ouverte dans un navigateur.

## Les points de terminaison

Tous les points de terminaison ont été documentés sur PostMan. Pour plus d'informations, vous pouvez consulter cette documentation via le lien suivant :

[![github_icone](README_pictures/logo-postman.png)](https://documenter.getpostman.com/view/25647707/2s93CNLYKV)

### Authentification

| Points de terminaison d'API  | Méthode HTTP | URI      |
|------------------------------|--------------|----------|
| Inscription de l'utilisateur | POST         | /signup/ |
| Connexion de l'utilisateur   | POST         | /login/  |

### Gestion des projets

| Points de terminaison d'API                                                                 | Méthode HTTP | URI             |
|---------------------------------------------------------------------------------------------|--------------|-----------------|
| Récupérer la liste de tous les projets (projects) rattachés à l'utilisateur (user) connecté | GET          | /projects/      |
| Créer un projet                                                                             | POST         | /projects/      |
| Récupérer les détails d'un projet (project) via son id                                      | GET          | /projects/{id}/ |
| Mettre à jour un projet                                                                     | PUT          | /projects/{id}/ |
| Supprimer un projet et ses problèmes                                                        | DELETE       | /projects/{id}/ |

### Gestion des collaborateurs d'un projet

| Points de terminaison d'API                                                        | Méthode HTTP | URI                        |
|------------------------------------------------------------------------------------|--------------|----------------------------|
| Récupérer la liste de tous les utilisateurs (users) attachés à un projet (project) | GET          | /projects/{id}/users/      |
| Ajouter un utilisateur (collaborateur) à un projet                                 | POST         | /projects/{id}/users/      |
| Supprimer un utilisateur d'un projet                                               | DELETE       | /projects/{id}/users/{id}/ |

### Gestion des problèmes associés à un problème

| Points de terminaison d'API                                          | Méthode HTTP | URI                         |
|----------------------------------------------------------------------|--------------|-----------------------------|
| Récupérer la liste des problèmes (issues) liés à un projet (project) | GET          | /projects/{id}/issues/      |
| Créer un problème dans un projet                                     | POST         | /projects/{id}/issues/      |
| Mettre à jour un problème dans un projet                             | PUT          | /projects/{id}/issues/{id}/ |
| Supprimer un problème d'un projet                                    | DELETE       | /projects/{id}/issues/{id}/ |

### Gestion des commentaires d'un problème

| Points de terminaison d'API                                    | Méthode HTTP | URI                                  |
|----------------------------------------------------------------|--------------|--------------------------------------|
| Créer des commentaires sur un problème (issue)                 | POST         | /projects/{id}/issues/comments/      |
| Récupérer la liste de tous les commentaires liés à un problème | GET          | /projects/{id}/issues/comments/      |
| Modifier un commentaire                                        | PUT          | /projects/{id}/issues/comments/{id}/ |
| Supprimer un commentaire                                       | DELETE       | /projects/{id}/issues/comments/{id}/ |
| Récupérer un commentaire via son id                            | GET          | /projects/{id}/issues/comments/{id}/ |

## Lien Github

[![github_icone](README_pictures/github.png)](https://github.com/lcourdes/https://github.com/lcourdes/API-securisee-RESTful)
