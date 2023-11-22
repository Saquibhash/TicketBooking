<template>
  <div>
    <h1>Search Results for '{{ query }}'</h1>

    <h2>Movies</h2>
    <ul>
      <li v-for="movie in moviesData" :key="movie?.id">
        <a :href="getMovieUrl(movie.id)">
          <img
            :src="movie?.img"
            class="card-img-top"
            width="150"
            style="border-radius: 15px"
          />
        </a>
      </li>
    </ul>

    <h2>Venues</h2>
    <ul>
      <li v-for="venue in venues" :key="venue.id">
        {{ venue.name }} - {{ venue.location }} - {{ venue.num_total_seats }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
    return {
      query: "",
      moviesData:[],
    };
  },
  methods: {
    getMovieUrl(movieId) {
      return `/movies/${movieId}`;
    },
    async searchMovies(Query) {
      try {
        const accessToken = localStorage.getItem("accessToken");
        const response = await axios.get("http://localhost:5000/search", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
          params: {
            query: Query, // Use 'this.query' instead of 'this.searchQuery'
          },
        });
        console.log(response);
        this.moviesData = response.data.movies;
        console.log(this.moviesData);
        this.todayShowsData = response.data.today_shows;
        this.comingSoonData = response.data.coming_soon_shows;
      } catch (error) {
        console.error("Error searching movies:", error);
      }
    },
  },
  created() {
    const queryParam = this.$route.query.q;
    this.query = queryParam;
    this.searchMovies(queryParam);
  },
};
</script>

<style>
/* Add your styles here */
</style>
