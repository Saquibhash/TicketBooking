<template>
  <div class="mt-4">
    <h2 class="text-3xl font-bold">Our Shows</h2>
    <div class="flex items-center justify-center" @click="openModal">
      <a
        class="buttom text-white font-bold py-2 px-4 rounded inline-block mb-4 w-full text-center"
      >
        ADD A NEW SHOW
      </a>
    </div>

    <template v-if="shws.length > 0">
      <div class="py-10">
        <table class="w-full table-slidedown">
          <thead>
            <tr>
              <th class="py-2">Show Id</th>
              <th class="py-2">Title</th>
              <th class="py-2">Venue</th>
              <th class="py-2">Location</th>
              <th class="py-2">Total Seats</th>
              <th class="py-2">Seats Booked</th>
              <th class="py-2">Seats Available</th>
              <th class="py-2">Day</th>
              <th class="py-2">Time</th>
              <th class="py-2"></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="item in shws"
              :key="item.id"
              class="border-t border-gray-300"
            >
              <td class="py-2">{{ item.shw.id }}</td>
              <td class="py-2">{{ item.shw?.movie?.title }}</td>
              <td class="py-2">{{ item.shw?.venue?.name }}</td>
              <td class="py-2">{{ item.shw?.venue?.location }}</td>
              <td class="py-2">{{ item.shw?.venue?.num_total_seats }}</td>
              <td class="py-2">{{ item.shw?.venue?.seats_available }}</td>
              <td class="py-2">{{ item.shw?.venue?.seats_booked }}</td>
              <td class="py-2">{{ item.shw?.day }}</td>
              <td class="py-2">{{ item.shw?.time }}</td>
              <td v-if="item.shw?.venue?.seats_available > 0" class="py-2">
                Cannot modify shows<br />with bookings
              </td>
              <td v-else class="py-2">
                <a
                  class="bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded inline-block mr-2"
                  @click="deleteShow(item.shw.id)"
                >
                  Delete
                </a>
                <router-link
                  :to="`/update-show/${item.shw.id}`"
                  class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded inline-block mr-2"
                  >Edit</router-link
                >
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
    <template v-else>
      <p class="text-center">THERE ARE NO SCHEDULED SHOWS</p>
    </template>
    <div
      class="fixed inset-0 bg-opacity-70 bg-black flex items-center justify-center"
      v-if="showModal"
    >
      <div class="modal-box bg-white p-5 rounded-lg">
        <h5 class="text-2xl font-semibold mb-4">Add a New Show</h5>
        <form @submit.prevent="createShow">
          <div
            class="form w-[400px] h-max text-center p-5 flex flex-col rounded-xl"
          >
            <div class="form-group">
              <label>Movie:</label>
              <select
                v-model="newShow.movieId"
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

              <!-- ... Other template content ... -->

              <label>Venue:</label>
              <select
                v-model="newShow.venueId"
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
              <label>Date:</label>
              <input
                type="date"
                v-model="newShow.day"
                min="2023-01-01"
                max="2023-12-31"
                required
                class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
              />
            </div>
            <div class="form-group">
              <label>Time:</label>
              <input
                type="time"
                v-model="newShow.time"
                required
                class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
              />
            </div>
          </div>
          <div class="flex justify-end pt-8 gap-4">
            <button
              type="submit"
              class="border bg-blue-500 text-white px-4 py-2 rounded-md"
            >
              Create Show
            </button>
            <button
              type="button"
              class="border bg-gray-300 text-gray-700 px-4 py-2 ml-4 rounded-md"
              @click="closeModal"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      shws: [],
      showModal: false, // Add showModal data property to control modal visibility
      newShow: {
        // Add properties for the new show here
        movieId: "",
        venueId: "",
        day: "",
        time: "",
      },
      movieList: [], // Store the list of movies fetched from the API
      venueList: [], // Store the list of venues fetched from the API
    };
  },
  methods: {
    async deleteShow(showId) {
      const accessToken = localStorage.getItem("accessToken");
      try {
        // Send the request to the server to delete the show
        await axios.delete(`http://localhost:5000/delete_show/${showId}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        // Refresh the show list after successful deletion
        this.fetchShows();
      } catch (error) {
        console.error("Error deleting show:", error);
      }
    },
    async fetchShows() {
      const accessToken = localStorage.getItem("accessToken");
      try {
        const response = await axios.get("http://localhost:5000/shows", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.shws = response.data;
      } catch (error) {
        console.error("Error fetching shows data:", error);
      }
    },
    openModal() {
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
      this.newShow = {
        // Reset the newShow object when the modal is closed
        movieId: "",
        venueId: "",
        day: "",
        time: "",
      };
    },

    async createShow() {
      const accessToken = localStorage.getItem("accessToken");
      try {
        // Send the new show data to the server to create a new show
        await axios.post("http://localhost:5000/create_show", this.newShow, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        // Clear the form data and close the modal after successful creation
        this.newShow = {
          movieId: "",
          venueId: "",
          day: "",
          time: "",
        };
        this.showModal = false;

        // Refresh the show list after successful creation
        this.fetchShows();
      } catch (error) {
        console.error("Error creating show:", error);
      }
    },
    async fetchMovieList() {
      const accessToken = localStorage.getItem("accessToken");
      try {
        const response = await axios.get("http://localhost:5000/movie", {
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
        const response = await axios.get("http://localhost:5000/venue", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.venueList = response.data?.venues;
      } catch (error) {
        console.error("Error fetching venue list:", error);
      }
    },
  },
  mounted() {
    this.fetchShows();
    this.fetchMovieList();
    this.fetchVenueList();
  },
  // ... Other script content ...
};
</script>
