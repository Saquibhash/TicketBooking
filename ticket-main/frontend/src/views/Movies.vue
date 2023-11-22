<template>
  <div>
    <h2>Movies</h2>

    <!-- Add New Movie Button -->
    <div class="row p-5">
      <center>
        <button
          type="button"
          class="border border-black px-3 py-1 rounded-2xl"
          @click="openModal"
        >
          Add New Movie
        </button>
      </center>
    </div>

    <!-- Add New Movie Modal -->
    <div
      class="fixed inset-0 bg-opacity-70 bg-black flex items-center justify-center"
      v-if="showModal"
    >
      <div class="modal-box bg-white p-5 rounded-lg">
        <h5 class="text-2xl font-semibold mb-4">Create New Movie</h5>
        <form @submit.prevent="createMovie">
          <div
            class="form w-[400px] h-max text-center p-5 flex flex-col rounded-xl"
          >
            <div class="form-group">
              <label for="title">Title</label>
              <input
                v-model="newMovie.title"
                type="text"
                class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
                name="title"
                id="title"
                placeholder="Enter title"
                required
              />
            </div>
            <div class="form-group">
              <label for="director">Director</label>
              <input
                v-model="newMovie.director"
                type="text"
                class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
                name="director"
                id="director"
                rows="3"
                placeholder="Enter director"
                required
              />
            </div>
            <div class="form-group">
              <label for="duration">Duration</label>
              <input
                v-model="newMovie.duration"
                type="number"
                class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
                name="duration"
                id="duration"
                placeholder="Enter duration"
                required
              />
            </div>
            <div class="form-group">
              <label for="cast">Cast</label>
              <input
                v-model="newMovie.cast"
                type="text"
                class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
                name="cast"
                id="cast"
                placeholder="Enter cast"
                required
              />
            </div>
            <div class="form-group">
              <label for="rating">Rating</label>
              <input
                v-model="newMovie.rating"
                type="number"
                class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
                name="rating"
                id="rating"
                min="0"
                max="5"
                placeholder="Enter rating"
                required
              />
            </div>
            <div class="form-group">
              <label for="price">Price</label>
              <input
                v-model="newMovie.price"
                type="number"
                class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
                name="price"
                id="price"
                placeholder="Enter price"
                required
              />
            </div>
            <div class="form-group">
              <label for="poster">Poster</label>
              <input
                v-model="newMovie.img"
                type="text"
                class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
                name="img"
                id="img"
                placeholder="Enter URL for poster"
                required
              />
            </div>
          </div>
          <div class="flex justify-end pt-8 gap-4">
            <button
              type="submit"
              class="border bg-blue-500 text-white px-4 py-2 rounded-md"
            >
              Create
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

    <template v-if="movies.length > 0">
      <div class="flex flex-wrap pb-12">
        <div
          class="col-md-4 w-full md:w-1/2 lg:w-1/3 px-4"
          v-for="movie in movies"
          :key="movie.id"
        >
          <div class="card mb-4 box-shadow">
            <a :href="getMovieUrl(movie.id)">

            <img
              class="card-img-top"
              :src="movie.img"
              :alt="movie.title"
              width="150"
              style="border-radius: 15px"
            /></a>
            <div class="card-body">
              <h3 class="card-title">{{ movie.title }}</h3>
              <div class="d-flex justify-content-between align-items-center">
                <!-- Add any additional content you want to display in each movie card -->
              </div>
              <div class="flex gap-2">
                <router-link
                  :to="`/update-movie/${movie.id}`"
                  class="border-blue-500 border px-1 bg-white"
                  >Edit</router-link
                >
                <a
                  href="#"
                  class="border-blue-500 border px-1 bg-white"
                  @click="confirmDelete(movie.id, movie.title)"
                  >Delete</a
                >
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    <template v-else>
      <div class="flex flex-wrap mt-4">
        <div class="col-md-12">
          <p>No Movies found.</p>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import axios from "axios"; // Import axios here
import Swal from "sweetalert2";

export default {
  data() {
    return {
      movies: [],
      showModal: false, // Add showModal data property to control modal visibility
      newMovie: {
        title: "",
        director: "",
        duration: "",
        cast: "",
        rating: "",
        price: "",
        img: "",
      },
    };
  },

  mounted() {
    this.fetchData();
  },
  methods: {
     getMovieUrl(movieId) {
      return `/movies/${movieId}`;
    },
    async fetchData() {
      const accessToken = localStorage.getItem("accessToken");
      try {
        const response = await axios.get("http://localhost:5000/movie", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.movies = response.data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    async createMovie() {
      const accessToken = localStorage.getItem("accessToken");
      try {
        // Send the new movie data to the server to create a new movie
        await axios.post("http://localhost:5000/create_movie", this.newMovie, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        // Clear the form data and close the modal after successful creation
        this.newMovie = {
          title: "",
          director: "",
          duration: "",
          cast: "",
          rating: "",
          price: "",
          img: "",
        };
        this.showModal = false;

        // Refresh the movie list after successful creation
        this.fetchData();
      } catch (error) {
        console.error("Error creating movie:", error);
      }
      
    },

    openModal() {
      console.log("open modal hit");
      this.showModal = true;
    },
    closeModal() {
      this.showModal = false;
      this.newMovie = {
        title: "",
        director: "",
        duration: "",
        cast: "",
        rating: "",
        price: "",
        img: "",
      };
    },
    
    async confirmDelete(movieId, movieTitle) {
      try {
        const result = await Swal.fire({
          title: "Are you sure?",
          text: `Do you want to delete the movie "${movieTitle}"?`,
          showCancelButton: true,
          confirmButtonColor: "#3085d6",
          cancelButtonColor: "#d33",
          confirmButtonText: "Yes, delete it!",
        });

        if (result.isConfirmed) {
          await this.deleteMovie(movieId);
        }
      } catch (error) {
        console.error("Error displaying SweetAlert:", error);
      }
    },
    async deleteMovie(movieId) {
  try {
    const accessToken = localStorage.getItem("accessToken");
    let response; // Declare the response variable here
    
    // Make the HTTP request to delete the movie
    try {
      response = await axios.post(
        `http://localhost:5000/delete_movie/${movieId}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
    } catch (error) {
      console.error("Error deleting data:", error);
    }

    if (response.data.success) {
      Swal.fire({
        title: "Deleted!",
        text: response.data.message,
        icon: "success",
      });

      // Reload the movie list after successful deletion
      this.fetchData();
    } else {
      Swal.fire({
        title: "Error",
        text: "Failed to delete the movie.",
        icon: "error",
      });
    }
  } catch (error) {
    console.error("Error deleting movie:", error);
    Swal.fire({
      title: "Error",
      text: "Failed to delete the movie.",
      icon: "error",
    });

  
  }
},
  },
};
</script>

<style>
/* Style for the modal box */
.modal-box {
  max-width: 500px;
  background-color: white;
  box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
