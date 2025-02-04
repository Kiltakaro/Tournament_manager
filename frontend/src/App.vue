<template>
  <div id="app">
    <h1>Tournois de Paddle</h1>

    <!-- Formulaire pour ajouter un tournoi -->
    <div v-if="!tournoiId">
      <h2>Ajouter un Tournoi</h2>
      <form @submit.prevent="ajouterTournoi">
        <div>
          <label for="nom">Nom du Tournoi:</label>
          <input v-model="nomTournoi" type="text" id="nom" required />
        </div>
        <button type="submit">Ajouter le Tournoi</button>
      </form>
    </div>

  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      nomTournoi: "", // Nom du tournoi à ajouter
      nomJoueur: "", // Nom du joueur à ajouter
      tournoiId: null, // ID du tournoi en cours
      tournoi: {}, // Détails du tournoi
      joueurs: [], // Liste des joueurs du tournoi
      matchs: [], // Liste des matchs du tournoi
    };
  },
  methods: {
    // Fonction pour ajouter un tournoi
    ajouterTournoi() {
      const tournoi = { nom: this.nomTournoi };
      axios
        .post("http://localhost:5000/tournois/", tournoi)
        .then((response) => {
          console.log(response.data.nom);
          console.log(response.data);
        })
        .catch((error) => {
          console.error("Erreur lors de l'ajout du tournoi", error);
        });
    },
  },
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
