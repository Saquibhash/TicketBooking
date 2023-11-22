<template>
  <div>
    <div class="flex items-center justify-center pt-5">
      <section class="form w-[400px] h-max" v-if="show !== null">
        <div class="w-full p-2">
          <h2>&nbsp;&nbsp;Book Tickets&nbsp;&nbsp;</h2>
        </div>
        <form class="flex flex-col w-full justify-center items-center">
          <div>
            <img
              :src="show?.movie?.img"
              height="200"
              width="200"
              style="border-radius: 15px"
            />
          </div>
          <label><br />{{ show?.movie?.title }}<br /></label>
          <div>
            <select
              id="show"
              name="show"
              @change="interactiveForm"
              class="w-full border border-black rounded-2xl"
            >
              <option
                v-for="sh in shows?.showtimes"
                :key="sh.id"
                :value="sh.id"
                :selected="sh.id === show.id"
                class="w-full border border-black rounded-2xl"
              >
                <b>Day:</b> {{ formatDate(sh.day) }} Time:
                {{ formatTime(sh.time) }} Venue: {{ sh.venue_id }}
              </option>
            </select>
          </div>

          <div class="more-seats flex flex-col items-center justify-center">
            <div>
              <label><br />Number of seats<br /></label>
              <input
                type="number"
                v-model="selectedSeats"
                name="seats"
                id="seats"
                min="1"
                :max= "show.seats_available"
                class="w-full px-4 py-2 my-2 border border-black rounded-2xl"
              />
            </div>
            <br />

            <div class="p-2 rounded-full border w-max">
              Price: ({{ show?.movie?.price }} * {{ selectedSeats }}) =
              {{ totalPrice }}
            </div>
            <div class="p-2 w-full">
              <button
                @click.prevent="createBookingFromBookTicket(show.id)"
                class="buttom w-full"
                :disabled="show.seats_available === 0"
              >
              {{ show.seats_available === 0 ? "House Full" : "Buy Now" }}
              </button>
            </div>
          </div>

          <div id="no-more-seats" v-if="show.seats_available === 0">
            <p>HOUSE FULL!</p>
          </div>
        </form>
      </section>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { format } from "date-fns";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      shows: [],
      show: null,
      selectedSeats: 1,
    };
  },
  computed: {
    totalPrice() {
      if (this.show) {
        return this.show.movie.price * this.selectedSeats;
      }
      return "";
    },
  },
  methods: {
    async fetchData() {
      try {
        const showId = parseInt(this.$route.params.id);
        const accessToken = localStorage.getItem("accessToken");
        const response = await axios.get(
          `http://localhost:5000/show/${showId}`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        console.log(response);
        this.show = response?.data?.show;
        const movieId = this.show.movie_id;
        const movieResponse = await axios.get(
          `http://localhost:5000/movie/${movieId}`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        this.shows = movieResponse?.data;
        console.log(this.shows);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    async createBookingFromBookTicket(showId) {
      const numSeats = this.selectedSeats;
      try {
        const accessToken = localStorage.getItem("accessToken");
        if (!accessToken) {
          Swal.fire({
            icon: "error",
            title: "Login First",
          });
        } else {
          const response = await axios.post(
            "http://localhost:5000/booking/",
            {
              shw: showId,
              seats: numSeats,
            },
            {
              headers: {
                Authorization: `Bearer ${accessToken}`,
              },
            }
          );
          if (response.status == 200) {
            Swal.fire({
              icon: "success",
              title: "Ticket Booked!",
              text: "Your ticket has been successfully booked.",
              confirmButtonColor: "#3085d6",
              confirmButtonText: "OK",
            });
            this.$router.push("/");
          }

        }
      } catch (error) {
        console.error("Error creating booking:", error);
      }
    },
    formatDate(dateStr) {
      return format(new Date(dateStr), "yyyy-MM-dd");
    },
    formatTime(timeStr) {
      return format(new Date(`1970-01-01T${timeStr}`), "HH:mm");
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