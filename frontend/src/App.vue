<template>
  <div id="app">
    <h1>Tournois de Paddle</h1>

    <!-- Formulaire pour ajouter un tournoi -->
    <div class="form-container">
      <h2>Ajouter un Tournoi</h2>
      <form @submit.prevent="ajouterTournoi">
        <div class="form-group">
          <label for="nom">Nom du Tournoi:</label>
          <input v-model="nomTournoi" type="text" id="nom" required />
        </div>
        <button type="submit">Ajouter le Tournoi</button>
      </form>
    </div>

    <!-- Formulaire pour inscrire un joueur à un tournoi -->
    <div class="form-container">
      <h2>Inscrire un Joueur</h2>
      <form @submit.prevent="inscrireJoueur">
        <div class="form-group">
          <label for="tournoiNom">Nom du Tournoi:</label>
          <input v-model="tournoiNom" type="text" id="tournoiNom" required />
        </div>
        <div class="form-group">
          <label for="nomJoueur">Nom du Joueur:</label>
          <input v-model="nomJoueur" type="text" id="nomJoueur" required />
        </div>
        <button type="submit">Inscrire le Joueur</button>
      </form>
    </div>

    <!-- Affichage de la liste des tournois -->
    <div class="list-container">
      <h2>Liste des Tournois</h2>
      <ul>
        <li v-for="tournoi in tournois" :key="tournoi.id" @click="fetchJoueurs(tournoi.nom)">
          {{ tournoi.nom }}
          <ul v-if="joueurs[tournoi.nom] && joueurs[tournoi.nom].length > 0">
            <li v-for="joueur in joueurs[tournoi.nom]" :key="joueur.id">
              {{ joueur.nom }}
            </li>
          </ul>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      nomTournoi: "",
      nomJoueur: "",
      tournoiNom: "",
      tournois: [],
      joueurs: {}
    };
  },
  methods: {
    // Fonction pour ajouter un tournoi
    ajouterTournoi() {
      axios.post("http://localhost:5000/tournois/", { nom: this.nomTournoi })
        .then(() => {
          this.fetchTournois();
        })
        .catch(error => {
          console.error("Erreur lors de l'ajout du tournoi", error);
        });
    },

    // Fonction pour inscrire un joueur à un tournoi
    inscrireJoueur() {
      axios.post("http://localhost:5000/joueurs/", { nom: this.nomJoueur, tournoi_nom: this.tournoiNom })
        .then(() => {
          this.fetchJoueurs(this.tournoiNom);
        })
        .catch(error => {
          console.error("Erreur lors de l'inscription du joueur", error);
        });
    },

    // Fonction pour récupérer la liste des tournois
    fetchTournois() {
      axios.get("http://localhost:5000/tournois/")
        .then(response => {
          this.tournois = response.data;
          this.tournois.forEach(tournoi => {
            this.fetchJoueurs(tournoi.nom);
          });
        })
        .catch(error => {
          console.error("Erreur lors de la récupération des tournois", error);
        });
    },

    // Fonction pour récupérer la liste des joueurs d'un tournoi
    fetchJoueurs(tournoiNom) {
      axios.get(`http://localhost:5000/tournois/nom/${tournoiNom}/id/`)
        .then(response => {
          const tournoiId = response.data.id;
          return axios.get(`http://localhost:5000/tournois/${tournoiId}/joueurs/`);
        })
        .then(response => {
          this.joueurs = { ...this.joueurs, [tournoiNom]: response.data };
        })
        .catch(error => {
          console.error("Erreur lors de la récupération des joueurs", error);
        });
    }
  },
  mounted() {
    this.fetchTournois();
  }
};
</script>

<style>
/* Ajoute des styles basiques pour le formulaire et la liste */
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  margin: 0;
  padding: 0;
}

#app {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

h1 {
  text-align: center;
  color: #333;
}

.form-container {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 10px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #333;
}

input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.list-container {
  margin-top: 20px;
}

ul {
  list-style-type: none;
  padding-left: 0;
}

li {
  padding: 10px;
  border-bottom: 1px solid #ccc;
}

li:hover {
  background-color: #f9f9f9;
}

li ul {
  margin-top: 10px;
  padding-left: 20px;
}

li ul li {
  border: none;
  padding: 5px 0;
}
</style>