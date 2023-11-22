<template>
  <div>
    <div class="w-full space-y-8">
      <!-- Search Form -->
      <form @submit.prevent="searchMovies" class="mt-8 space-y-6">
        <div
          class="rounded-full shadow-sm -space-y-px w-full flex flex-col items-center justify-center"
        >
          <div class="w-full flex items-center justify-center">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search Location, Movie, Ratings"
              class="w-1/6 appearance-none rounded-2xl relative block px-3 py-2 border border-black placeholder-gray-500 text-gray-900 focus:outline-none sm:text-sm"
            />
          </div>
          <button
            type="submit"
            class="group relative w-max flex justify-center py-1 px-2 bg-gray-200 border-black border border-transparent text-sm font-medium rounded-md text-black"
          >
            Search
          </button>
        </div>
      </form>

      <!-- Movies Section -->
      <section>
        <h2 class="mt-6 text-center text-2xl font-semibold">Movies</h2>
        <div v-if="moviesData.length > 0" class="flex">
          <div
            v-for="movie in moviesData"
            :key="movie.id"
            class="horizontal-movies"
          >
            <div class="flex flex-col">
              <a :href="getMovieUrl(movie.id)">
                <img
                  :src="movie?.img"
                  alt="poster"
                  class=""
                  height="200"
                  width="200"
              /></a>
            </div>
          </div>
        </div>
        <div v-else>
          <p class="text-center">No movies available.</p>
        </div>
      </section>

      <!-- Shows Today Section -->
      <section>
        <h2 class="mt-6 text-center text-2xl font-semibold pb-6">
          Shows Today
        </h2>
        <table class="table-movies">
          <thead>
            <tr>
              <th>Movie Poster</th>
              <th>Title</th>
              <th>Venue</th>
              <th>Location</th>
              <th>Seats Available</th>
              <th>Day</th>
              <th>Time</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <!-- Loop through the 'todayShowsData' array and display the table rows -->
            <tr
              v-for="show in todayShowsData"
              :key="show.id"
              :id="'sh' + show.id"
            >
              <td>
                <a href="#"
                  ><img
                    :src="show?.movie?.img"
                    width="80"
                    style="border-radius: 15px"
                /></a>
              </td>
              <td>{{ show.movie?.title }}</td>
              <td>{{ show.venue?.name }}</td>
              <td>{{ show.venue?.location }}</td>
              <td>{{ show?.seats_available }}</td>
              <td>{{ show.day }}</td>
              <td>{{ show.time }}</td>
              <td class="sold">
                <a class="buttom" :href="getBuyTicketLink(show?.id)">
                  Buy Ticket
                </a>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="todayShowsData.length === 0" class="text-center mt-4">
          <p>No shows available for today.</p>
        </div>
      </section>

      <!-- Coming Soon Section -->
      <section>
        <h2 class="pt-6 text-center text-2xl font-semibold pb-6">
          Coming Soon
        </h2>
        <table class="table-movies">
          <thead>
            <tr>
              <th>Movie Poster</th>
              <th>Title</th>
              <th>Venue</th>
              <th>Location</th>
              <th>Seats Available</th>
              <th>Day</th>
              <th>Time</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <!-- Loop through the 'comingSoonData' array and display the table rows -->
            <tr
              v-for="show in comingSoonData"
              :key="show.id"
              :id="'sh' + show.id"
            >
              <td>
                <a href="#"
                  ><img
                    :src="show?.movie?.img"
                    width="80"
                    style="border-radius: 15px"
                /></a>
              </td>
              <td>{{ show.movie?.title }}</td>
              <td>{{ show.venue?.name }}</td>
              <td>{{ show.venue?.location }}</td>
              <td>{{ show?.seats_available }}</td>
              <td>{{ show.day }}</td>
              <td>{{ show.time }}</td>
              <td class="sold">
                <a v-if="show.seats_available > 0" class="buttom" :href="getBuyTicketLink(show?.id)">
                  Buy Ticket
                </a>
                <span v-else class="house-full">House Full</span>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="comingSoonData.length === 0" class="text-center mt-4">
          <p>No shows coming soon.</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      searchQuery: "",
      moviesData: [],
      todayShowsData: [],
      comingSoonData: [],
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    getMovieUrl(movieId) {
      return `/movies/${movieId}`;
    },
    getBuyTicketLink(showId) {
      return `/book-ticket/${showId}`;
    },
    searchMovies() {
      this.$router.push({ name: "search", query: { q: this.searchQuery } });
    },
    async fetchData() {
      try {
        const accessToken = localStorage.getItem("accessToken");
        const response = await axios.get("http://localhost:5000/", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.moviesData = response.data.all_movies;
        this.todayShowsData = response.data.today_shws;
        this.comingSoonData = response.data.next_shws;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
};
</script>

<style>
.horizontal-movies {
  margin: 0 auto;
  display: grid;
  grid-auto-flow: column;
  gap: 1rem;
  padding: 1rem;
  width: 100%;
  overflow-y: auto;
  overscroll-behavior-x: contain;
  scroll-snap-type: x mandatory;
}
.horizontal-movies > a {
  scroll-snap-align: center;
}

.horizontal-movies img {
  width: 180px;
  max-width: none;
  object-fit: contain;
  border-radius: 15px;
}
table {
  display: table;
  margin-right: auto;
  margin-left: auto;
  width: 100%;
}
table td,
table th {
  text-align: center;
  border: 1px solid rgb(178, 255, 230);
}

td {
  height: 75px; /*min height*/
}

.buttom {
  overflow: hidden;
  white-space: nowrap; /*avoids the bad resizing when window smaller*/
  color: white;
  text-align: center;
  padding: 12px;
  text-decoration: none; /* without link line*/
  font-size: 12px;
  line-height: 25px;
  border-radius: 12px;
  background-color: rgb(8, 4, 21);
  border: 2px solid rgba(183, 26, 94, 1);
}
/* Change the background color on mouse-over */
.buttom:hover {
  background-color: rgba(183, 26, 94, 1);
  border: 2px solid rgb(8, 4, 21);
}
</style>
