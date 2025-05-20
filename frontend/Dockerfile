# Utilise l'image officielle Node.js
FROM node:20

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier tout le reste des fichiers de l'app
COPY . .

# Construire l'application pour la prod
RUN npm run build

# Exposer le port par défaut de Nuxt
EXPOSE 3000

# Lancer le serveur Nuxt
CMD ["npm", "run", "preview"]

