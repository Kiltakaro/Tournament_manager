<template>
  <div id="app">
    <h1>Tournois de Paddle</h1>

    <!-- Formulaire pour ajouter un tournoi -->
    <div>
      <h2>Ajouter un Tournoi</h2>
      <form @submit.prevent="ajouterTournoi">
        <div>
          <label for="nom">Nom du Tournoi:</label>
          <input v-model="nomTournoi" type="text" id="nom" required />
        </div>
        <button type="submit">Ajouter le Tournoi</button>
      </form>
    </div>

    <!-- Formulaire pour inscrire un joueur à un tournoi -->
    <div>
      <h2>Inscrire un Joueur</h2>
      <form @submit.prevent="inscrireJoueur">
        <div>
          <label for="tournoiNom">Nom du Tournoi:</label>
          <input v-model="tournoiNom" type="text" id="tournoiNom" required />
        </div>
        <div>
          <label for="nomJoueur">Nom du Joueur:</label>
          <input v-model="nomJoueur" type="text" id="nomJoueur" required />
        </div>
        <button type="submit">Inscrire le Joueur</button>
      </form>
    </div>

    <!-- Affichage de la liste des tournois -->
    <div>
      <h2>Liste des Tournois</h2>
      <ul>
        <li v-for="tournoi in tournois" :key="tournoi.id">
          {{ tournoi.nom }}
        </li>
      </ul>
    </div>

    <!-- Affichage de la liste des joueurs d'un tournoi -->
    <div v-if="joueurs.length > 0">
      <h2>Liste des Joueurs du Tournoi {{ tournoiNom }}</h2>
      <ul>
        <li v-for="joueur in joueurs" :key="joueur.id">
          {{ joueur.nom }}
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
      joueurs: []
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
          this.fetchJoueurs();
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
        })
        .catch(error => {
          console.error("Erreur lors de la récupération des tournois", error);
        });
    },

    // Fonction pour récupérer la liste des joueurs d'un tournoi
    fetchJoueurs() {
      axios.get(`http://localhost:5000/tournois/nom/${this.tournoiNom}/id/`)
        .then(response => {
          const tournoiId = response.data.id;
          return axios.get(`http://localhost:5000/tournois/${tournoiId}/joueurs/`);
        })
        .then(response => {
          this.joueurs = response.data;
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
form {
  margin-bottom: 20px;
}

input {
  margin-right: 10px;
}

button {
  padding: 5px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

ul {
  list-style-type: none;
  padding-left: 0;
}
</style>