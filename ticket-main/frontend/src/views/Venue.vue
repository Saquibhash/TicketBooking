<template>
  <div class="w-full pb-10">
    <h2 class="text-center w-full py-5 text-2xl font-bold">Venues</h2>
    <!-- Add Venue Dropdown -->
    <div class="relative inline-flex">
      <select v-model="selectedVenue" class="border border-black rounded-2xl px-3 py-1">
        <option value="">Select a Venue</option>
        <option v-for="venue in venues" :key="venue.id" :value="venue.id">{{ venue.name }}</option>
      </select>
    </div>
    <button
      type="button"
      class="border border-black px-3 py-1 rounded-2xl ml-3"
      @click="downloadCSV"
    >
      Download CSV
    </button>
    <div class="buttom hover:cursor-pointer" @click="addVenue">
      <a class="submit">Add Venue</a>
    </div>
    <div class="pt-5 w-full"></div>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Location</th>
          <th>Capacity</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="venue in venues" :key="venue.id">
          <td>{{ venue.id }}</td>
          <td>{{ venue.name }}</td>
          <td>{{ venue.location }}</td>
          <td>{{ venue.num_total_seats }}</td>
          <td>
            <router-link :to="`/update-venue/${venue.id}`" class="border-blue-500 border px-1 bg-white">Edit</router-link>
            <a class="border-blue-500 border px-1 bg-white" @click="confirmDelete(venue.id)">Delete</a>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- Add New Venue Modal -->
  <div v-if="showModal" class="fixed inset-0 bg-opacity-70 bg-black flex items-center justify-center">
    <div class=" bg-white p-5 rounded-lg">
      <h5 class="text-2xl font-semibold mb-4">Create New Venue</h5>
      <form @submit.prevent="createVenue">
        <div class="form w-[400px] h-max text-center p-5 flex flex-col rounded-xl">
          <div class="form-group">
            <label for="name">Name</label>
            <input v-model="newVenue.name" type="text" class="w-full px-5 py-4 my-2 border border-black rounded-2xl" name="name" id="name" placeholder="Enter name" required />
          </div>
          <div class="form-group">
            <label for="location">Location</label>
            <input v-model="newVenue.location" type="text" class="w-full px-5 py-4 my-2 border border-black rounded-2xl" name="location" id="location" placeholder="Enter location" required />
          </div>
          <div class="form-group">
            <label for="num_total_seats">Capacity</label>
            <input v-model="newVenue.num_total_seats" type="number" class="w-full px-5 py-4 my-2 border border-black rounded-2xl" name="num_total_seats" id="num_total_seats" placeholder="Enter capacity" required />
          </div>
        </div>
        <div class="flex justify-end pt-8 gap-4">
          <button type="submit" class="border bg-blue-500 text-white px-4 py-2 rounded-md">Create</button>
          <button type="button" class="border bg-gray-300 text-gray-700 px-4 py-2 ml-4 rounded-md" @click="closeModal">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      venues: [],
      selectedVenue: "", // Added to store the selected venue ID
      showModal: false,
      newVenue: {
        name: "",
        location: "",
        num_total_seats: "",
      },
    };
  },
  methods: {
    async fetchVenues() {
      try {
        const accessToken = localStorage.getItem("accessToken");
        const response = await axios.get("http://localhost:5000/venue", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.venues = response.data.venues;
      } catch (error) {
        console.error("Error fetching venues:", error);
      }
    },

    confirmDelete(venueId) {
      const confirmDelete = window.confirm("Are you sure you want to delete this venue?");
      if (confirmDelete) {
        this.deleteVenue(venueId);
      }
    },

    async deleteVenue(venueId) {
      try {
        const accessToken = localStorage.getItem("accessToken");
        await axios.delete(`http://localhost:5000/delete_venue/${venueId}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        // Refresh the list of venues after deletion
        this.fetchVenues();
      } catch (error) {
        console.error("Error deleting venue:", error);
      }
    },

    addVenue() {
      this.showModal = true;
    },

    closeModal() {
      this.showModal = false;
      this.newVenue = {
        name: "",
        location: "",
        num_total_seats: "",
      };
    },

    async createVenue() {
      try {
        const accessToken = localStorage.getItem("accessToken");
        await axios.post("http://localhost:5000/create_venue", this.newVenue, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        // Clear the form data and close the modal after successful creation
        this.newVenue = {
          name: "",
          location: "",
          num_total_seats: "",
        };
        this.showModal = false;
        // Refresh the venue list after successful creation
        this.fetchVenues();
      } catch (error) {
        console.error("Error creating venue:", error);
      }
    },

    async downloadCSV() {
      if (!this.selectedVenue) {
        // Handle case where no venue is selected
        console.error("No venue selected for CSV download.");
        return;
      }

      try {
        const accessToken = localStorage.getItem("accessToken");
        const response = await axios.get(`http://localhost:5000/export_venue_csv/${this.selectedVenue}`, {
          responseType: "blob",
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        const blob = new Blob([response.data], { type: "text/csv" });
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = "venue.csv";
        a.style.display = "none";

        document.body.appendChild(a);
        a.click();

        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } catch (error) {
        console.error("Error downloading CSV:", error);
      }
    },
  },
  mounted() {
    this.fetchVenues();
  },
};
</script>

<style>
/* Style for the modal box */
</style>
