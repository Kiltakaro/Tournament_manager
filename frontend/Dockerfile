# Passer a node 20 ou 22 plus tard
FROM node:18

WORKDIR /frontend

# Copier les package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install
RUN npm install axios
COPY . .

# Construire l'application Vue.js
RUN npm run build

# Utiliser un serveur Nginx pour servir les fichiers statiques
FROM nginx:alpine

# Copier les fichiers générés par Vue.js vers le dossier Nginx
COPY --from=0 /frontend/dist /usr/share/nginx/html

# Exposer le port 80 pour Nginx
EXPOSE 80

# Commande par défaut pour Nginx
CMD ["nginx", "-g", "daemon off;"]
