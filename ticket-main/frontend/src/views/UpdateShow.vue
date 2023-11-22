<template>
  <div>
    <h2>Edit Show</h2>
    <hr />

    <form
      @submit.prevent="updateShow"
      class="flex items-center justify-center pb-10"
    >
      <div class="form w-[400px] h-max text-center p-5 flex flex-col rounded-xl">
        <div class="form-group">
          <label for="movie">Movie:</label>
          <select
            v-model="show.movie_id"
            required
            class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
          >
            <option
              v-for="movie in movieList"
              :value="movie.id"
              :key="movie.id"
            >
              {{ movie.title }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="venue">Venue:</label>
          <select
            v-model="show.venue_id"
            required
            class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
          >
            <option
              v-for="venue in venueList"
              :value="venue.id"
              :key="venue.id"
            >
              {{ venue.name }} {{ venue.location }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label for="day">Date:</label>
          <input
            type="date"
            v-model="show.day"
            min="2023-01-01"
            max="2023-12-31"
            required
            class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
          />
        </div>
        <div class="form-group">
          <label for="time">Time:</label>
          <input
            type="time"
            v-model="show.time"
            required
            class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
          />
        </div>
        <div class="flex justify-end pt-8 gap-4">
          <button
            type="submit"
            class="border bg-blue-500 text-white px-4 py-2 rounded-md"
          >
            Update
          </button>
          <button
            type="button"
            class="border bg-gray-300 text-gray-700 px-4 py-2 ml-4 rounded-md"
            @click="cancelEdit"
          >
            Cancel
          </button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";
import moment from "moment";

export default {
  data() {
    return {
      show: {
        movie_id: "",
        venue_id: "",
        day: "",
        time: "",
      },
      movieList: [], // Initialize movieList as an empty array
      venueList: [], // Initialize venueList as an empty array
    };
  },

  methods: {
    async fetchMovieList() {
      const accessToken = localStorage.getItem("accessToken");
      try {
        const response = await axios.get("http://localhost:5000/movie",
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
        this.movieList = response.data;
      } catch (error) {
        console.error("Error fetching movie list:", error);
      }
    },

    async fetchVenueList() {
      const accessToken = localStorage.getItem("accessToken");
      try {
        const response = await axios.get("http://localhost:5000/venue",
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
        this.venueList = response.data?.venues;
      } catch (error) {
        console.error("Error fetching venue list:", error);
      }
    },
    async updateShow() {
      const accessToken = localStorage.getItem("accessToken");
      const formattedDate = moment(this.show.day).format("YYYY-MM-DD");
      const formattedTime = moment(this.show.time, "HH:mm").format("HH:mm:ss");

      // Update the show object with the formatted values
      this.show.day = formattedDate;
      this.show.time = formattedTime;
      try {
        const showId = parseInt(this.$route.params.id);
        const response = await axios.post(
          `http://localhost:5000/edit_show/${showId}`,
          this.show,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        console.log(response);

        if (response.data.success) {
          this.$router.push({ name: "shows" });
        } else {
          Swal.fire({
            icon: "error",
            title: "Error",
            text: "Failed to update the show.",
          });
        }
      } catch (error) {
        console.error("Error updating show:", error);
      }
    },
    cancelEdit() {
      this.$router.push({ name: "shows" });
    },
  },
  async beforeRouteEnter(to, from, next) {
    const accessToken = localStorage.getItem("accessToken");
    try {
      const showId = parseInt(to.params.id);
      const response = await axios.get(`http://localhost:5000/show/${showId}`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
      const showData = response?.data?.show;
      console.log(showData);
      next((vm) => {
        vm.show = showData;
      });
    } catch (error) {
      console.error("Error fetching show data:", error);
      next();
    }
  },
  mounted() {
    this.fetchMovieList();
    this.fetchVenueList();
  },
};
</script>

<style>

</style>
