<template>
  <div>
    <section>
      <h2>&nbsp;&nbsp;{{ movie.title }}&nbsp;&nbsp;</h2>
      <section class="movie-description">
        <div
          class="form flex items-center justify-center p-5"
          style="width: 100%; height: auto"
        >
          <img
            :src="movie?.img"
            height="200"
            width="200"
            style="border-radius: 15px"
          />
          <p style="padding-left: 25px; text-align: left">
            <b>Title:</b>&nbsp;{{ movie.title }}<br /><br />
            <b>Duration:</b>&nbsp;{{ movie.duration }} min<br /><br />
            <b>Director:</b>&nbsp;{{ movie.director }}<br /><br />
            <b>Cast:</b>&nbsp;{{ movie.cast }}<br /><br />
            <b>Ratings:</b>&nbsp;{{ movie.rating }}<br /><br />
          </p>
        </div>
      </section>
      <section class="movie-shws">
        <h2>&nbsp;&nbsp;SHOWS&nbsp;&nbsp;</h2>
        <div v-if="shws.length > 0">
          <table class="table-movies">
            <thead>
              <tr>
                <th>Movie Poster</th>
                <th>Title</th>
                <th>Venue</th>
                <th>Location</th>
                <th>Seats</th>
                <th>Day</th>
                <th>Time</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="shw in shws" :key="shw.id" :id="'sh' + shw.id">
                <td>
                  <a :href="shw?.movie_id">
                    <img
                      :src="movie?.img"
                      width="120"
                      style="border-radius: 15px"
                    />
                  </a>
                </td>
                <td>{{ movie?.title }}</td>
                <td>{{ shw?.venue?.name }}</td>
                <td>{{ shw?.venue?.location }}</td>
                <td class="seats">{{ shw?.venue?.num_total_seats }}</td>
                <td>{{ formatDate(shw?.day) }}</td>
                <td>{{ formatTime(shw?.time) }}</td>
                <td class="sold">
                  <a class="buttom" :href="getBuyTicketLink(shw?.id)">
                    Buy Ticket
                  </a>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else style="text-align: center">
          THERE ARE NO {{ movie?.title?.toUpperCase() }} SHOWS SOON
        </p>
      </section>
    </section>
  </div>
</template>

<script>
import axios from "axios";
import { format } from "date-fns";

export default {
  data() {
    return {
      movie: {},
      shws: [],
    };
  },
  methods: {
    getBuyTicketLink(showId) {
      return `/book-ticket/${showId}`;
    },
    async fetchData() {
      try {
        const movieId = parseInt(this.$route.params.id);
        const response = await axios.get(
          `http://localhost:5000/movie/${movieId}`
        );
        this.movie = response.data.movie;
        this.shws = response.data.showtimes;
        for (const shw of this.shws) {
          await this.fetchVenueDetails(shw.venue_id, shw);
        }
        console.log(this.shws);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    async fetchVenueDetails(venueId, shw) {
      try {
        const accessToken = localStorage.getItem("accessToken");
        const response = await axios.get(
          `http://localhost:5000/venue/${venueId}`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        // Update the showtime with venue details
        shw.venue = response.data.venue;
      } catch (error) {
        console.error("Error fetching venue details:", error);
      }
    },
    formatDate(dateStr) {
      return format(new Date(dateStr), "dd-MM-yyyy");
    },
    formatTime(timeStr) {
      return format(new Date(`1970-01-01T${timeStr}`), "HH:mm");
    },
    getMovieUrl(movieId) {
      return `#/movie/${movieId}`;
    },
    getBookingUrl(showId) {
      return `#/booking/${showId}`;
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style>
/* Add your styles here */
</style>
