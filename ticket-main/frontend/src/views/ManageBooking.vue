<template>
  <div>
    <h2>Manager Bookings</h2>
    <hr />

    <table v-if="bookings">
      <thead>
        <tr>
          <th class="py-2">Show Id</th>
          <th class="py-2">Title</th>
          <th class="py-2">Venue</th>
          <th class="py-2">Location</th>
          <th class="py-2">Total Seats</th>
          <th class="py-2">Seats Available</th>
          <th class="py-2">Seats Booked</th>
          <th class="py-2">Day</th>
          <th class="py-2">Time</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="bookings">
          <td class="py-2">{{ bookings.show_id }}</td>
          <td class="py-2">{{ bookings.title }}</td>
          <td class="py-2">{{ bookings.venue }}</td>
          <td class="py-2">{{ bookings.location }}</td>
          <td class="py-2">{{ bookings.total_seats }}</td>
          <td class="py-2 seats">{{ bookings.seats_booked }}</td>
          <td class="py-2">{{ bookings.seats_available }}</td>
          <td class="py-2">{{ bookings.day }}</td>
          <td class="py-2">{{ bookings.time }}</td>
        </tr>
      </tbody>
    </table>
    <p v-else style="text-align: center">No bookings found for this show.</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      bookings: null,
    };
  },
  methods: {
    async fetchBookings() {
      try {
        const showId = parseInt(this.$route.params.id);
        const accessToken = localStorage.getItem("accessToken");
        const response = await axios.get(
          `http://localhost:5000/manage_booking/${showId}`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        );
        this.bookings = response.data.booking;
        console.log(this.bookings);
      } catch (error) {
        console.error("Error fetching manager bookings data:", error);
      }
    },
  },
  mounted() {
    this.fetchBookings();
  },
};
</script>
