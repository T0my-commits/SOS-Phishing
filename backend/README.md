# Comment démarrer le docker
- sudo docker-compose up --remove-orphans
- sudo docker compose run web pip install -r requirements.txt # installer des dépendances

# A améliorer
- OK Ajouter le nombre de pièces jointes ouvertes
- OK Patrick Hooper case
- OK Faire une copie des targets pour chaque campagne
- Ajouter export PDF des dashboards
- Ajouter template utilisé dans Options
- Modifier DB
  - OK formes normales campaign
  - message timestamp events
  - ordre préférence interests
  - ajouter le model backup server
  - ajouter credentials filled
  - ajouter le champs de feeback après compromission
- Mettre le logo user en orange si admin
- Envoyer mail avec les crédentials à la création d'un utilisateur
- Règle d'exception ou fonction de test d'envoie de mail
- Duplication des adresses mail et numéros de téléphone
- Intégrer les graphs de feedbacks dans les dashboards
- Ajouter note réalise dans feedback pour SOS Phishing uniquement
- Compter le nombre de personnes qui n'ouvrent pas leurs mails et re-calculer user vigilance
- Mesures de remédiation après une campagne
- Relier la classe CognitiveBiases à un flow de templates
- Afficher les "tags" d'une campagne (affichage simplifié des biais cognitifs)
- Stocker l'adresse MAC de l'appareil qui à cliqué sur un lien pour ne pas polluer la DB avec du brute forcing
- Blacklist IP pour fonctionnalités non payées
- Longueur message verification front, compteur caractères
- numéros de version des classes de copy
- email_1, email_2, email_3 dans les templates de fichiers CSV
- Retirer pays dans ligne du tableau dashboard si pas de pays dans place of work

- Préciser conditions de keep_data dans export csv target
- Finir export csv target
- Vérifier que l'url_id est unique avant de l'utiliser dans la création de campagne
- Vérifier que la date de début d'une campagne et la date de fin sont cohérentes
