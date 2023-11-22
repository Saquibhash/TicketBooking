<template>
  <div>
    <h2>Edit Movie</h2>
    <hr />

    <form
      @submit.prevent="updateMovie"
      class="flex items-center justify-center pb-10"
    >
      <div class="form w-[400px] h-max text-center p-5 flex flex-col rounded-xl">
        <div class="form-group">
          <label for="title">Title</label>
          <input
            v-model="movie.title"
            type="text"
            class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
            name="title"
            id="title"
            required
          />
        </div>
        <div class="form-group">
          <label for="director">Director</label>
          <input
            v-model="movie.director"
            type="text"
            class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
            name="director"
            id="director"
            required
          />
        </div>
        <div class="form-group">
          <label for="duration">Duration</label>
          <input
            v-model="movie.duration"
            type="number"
            class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
            name="duration"
            id="duration"
            required
          />
        </div>
        <div class="form-group">
          <label for="cast">Cast</label>
          <input
            v-model="movie.cast"
            type="text"
            class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
            name="cast"
            id="cast"
            required
          />
        </div>
        <div class="form-group">
          <label for="rating">Rating</label>
          <input
            v-model="movie.rating"
            type="number"
            class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
            name="rating"
            id="rating"
            min="0"
            max="5"
            required
          />
        </div>
        <div class="form-group">
          <label for="price">Price</label>
          <input
            v-model="movie.price"
            type="number"
            class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
            name="price"
            id="price"
            required
          />
        </div>
        <div class="form-group">
          <label for="img">Poster</label>
          <input
            v-model="movie.img"
            type="text"
            class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
            name="img"
            id="img"
            required
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
export default {
  data() {
    return {
      movie: {
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
  methods: {
    async updateMovie() {
      try {
        const movieId = parseInt(this.$route.params.id);
        const accessToken = localStorage.getItem("accessToken");
        const response = await axios.post(
          `http://localhost:5000/edit_movie/${movieId}`,
          this.movie,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        if (response.data.success) {
          this.$router.push({ name: "movies" });
        } else {
          Swal.fire({
            icon: "error",
            title: "Error",
            text: "Failed to update the movie.",
          });
        }
      } catch (error) {
        console.error("Error updating movie:", error);
      }
    },
    cancelEdit() {
      this.$router.push({ name: "movies" });
    },
  },
  async beforeRouteEnter(to, from, next) {
    try {
      const movieId = parseInt(to.params.id);
      const accessToken = localStorage.getItem("accessToken");
      const response = await axios.get(
        `http://localhost:5000/movie/${movieId}`,
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      const movieData = response?.data?.movie;
      next((vm) => {
        vm.movie = movieData;
      });
    } catch (error) {
      console.error("Error fetching movie data:", error);
      next();
    }
  },
};
</script>
