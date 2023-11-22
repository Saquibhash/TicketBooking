<template>
    <div>
      <h2>Edit Venue</h2>
      <hr />
  
      <form @submit.prevent="updateVenue" class="flex items-center justify-center pb-10">
        <div class="form w-[400px] h-max text-center p-5 flex flex-col rounded-xl">
          <div class="form-group">
            <label for="name">Name</label>
            <input
              v-model="venue.name"
              type="text"
              class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
              name="name"
              id="name"
              required
            />
          </div>
          <div class="form-group">
            <label for="location">Location</label>
            <input
              v-model="venue.location"
              type="text"
              class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
              name="location"
              id="location"
              required
            />
          </div>
          <div class="form-group">
            <label for="num_total_seats">Capacity</label>
            <input
              v-model="venue.num_total_seats"
              type="number"
              class="w-full px-5 py-4 my-2 border border-black rounded-2xl"
              name="num_total_seats"
              id="num_total_seats"
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
        venue: {
          name: "",
          location: "",
          num_total_seats: "",
        },
      };
    },
    methods: {
      async updateVenue() {
        try {
          const venueId = parseInt(this.$route.params.id);
          const accessToken = localStorage.getItem("accessToken");
          const response = await axios.post(
            `http://localhost:5000/edit_venue/${venueId}`,
            this.venue,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
          );
          console.log(response);
  
          if (response.data.success) {
            this.$router.push({ name: "venue" });
          } else {
            Swal.fire({
              icon: "error",
              title: "Error",
              text: "Failed to update the venue.",
            });
          }
        } catch (error) {
          console.error("Error updating venue:", error);
        }
      },
      cancelEdit() {
        this.$router.push({ name: "venue" });
      },
    },
    async beforeRouteEnter(to, from, next) {
      try {
        const venueId = parseInt(to.params.id);
        const accessToken = localStorage.getItem("accessToken");
        const response = await axios.get(`http://localhost:5000/venue/${venueId}`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
        const venueData = response?.data?.venue;
        next((vm) => {
          vm.venue = venueData;
        });
      } catch (error) {
        console.error("Error fetching venue data:", error);
        next();
      }
    },
  };
  </script>
  
  <style>
  </style>
  