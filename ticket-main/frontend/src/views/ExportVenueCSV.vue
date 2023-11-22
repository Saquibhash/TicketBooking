<template>
    <div>
      <h1>Venue CSV Export</h1>
  
      <!-- Export CSV Form -->
      <form @submit.prevent="exportCSV">
        <label for="selected_venue">Select Venue:</label>
        <select v-model="selectedVenue" id="selected_venue">
          <option v-for="venue in venues" :key="venue.id" :value="venue.id">
            {{ venue.name }}
          </option>
        </select>
        <button type="submit">Download CSV</button>
      </form>
  
      <!-- Display any messages from the server (e.g., success or error messages) -->
      <div id="message">
        <p>Status: {{ status }}</p>
        <p>{{ message }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        selectedVenue: null,
        venues: [], // You need to populate this array with venue data
        status: "",
        message: "",
      };
    },
    methods: {
      async exportCSV() {
        // Send a request to the server to export CSV for the selected venue
        try {
          const response = await fetch("/export_venue_csv", {
            method: "POST",
            body: JSON.stringify({ selectedVenue: this.selectedVenue }),
            headers: {
              "Content-Type": "application/json",
            },
          });
  
          if (response.ok) {
            this.status = "success";
            this.message = "CSV file downloaded successfully!";
          } else {
            this.status = "error";
            this.message = "Failed to download CSV file.";
          }
        } catch (error) {
          this.status = "error";
          this.message = "Failed to download CSV file.";
          console.error("Error exporting CSV:", error);
        }
      },
    },
  };
  </script>
  
  <style>
  /* Add your CSS styles here */
  </style>
  