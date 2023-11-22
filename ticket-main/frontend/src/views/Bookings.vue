<template>
  <div>
    <h2 class="text-center text-3xl font-bold pt-4 pb-6">Bookings</h2>

    <template v-if="bookings.length > 0">
      <div class="pb-10">
        <table class="w-full border-collapse">
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
              <th class="py-2"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="booking in bookings" :key="booking.show_id">
              <td class="py-2">{{ booking?.show_id }}</td>
              <td class="py-2">{{ booking?.title }}</td>
              <td class="py-2">{{ booking?.venue }}</td>
              <td class="py-2">{{ booking?.location }}</td>
              <td class="py-2">{{ booking?.total_seats }}</td>
              <td class="py-2 seats">{{ booking?.seats_booked }}</td>
              <td class="py-2">{{ booking?.seats_available }}</td>
              <td class="py-2">{{ booking?.day }}</td>
              <td class="py-2">{{ booking?.time }}</td>
              <td class="py-2">
                <a
                  class="bg-green-600 text-white px-4 py-2 rounded-full"
                  :href="getBookingLink(booking?.show_id)"
                >
                  SEE BOOKINGS
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>
    <template v-else>
      <p class="text-center">THERE ARE NO SHOWS</p>
    </template>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      bookings: [],
    };
  },
  methods: {
    async fetchBookings() {
      try {
        const accessToken = localStorage.getItem("accessToken");
        const response = await axios.get("http://localhost:5000/bookings", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.bookings = response.data;
      } catch (error) {
        console.error("Error fetching bookings data:", error);
      }
    },
    getBookingLink(showId) {
      return `/manage-booking/${showId}`;
    },
  },
  mounted() {
    this.fetchBookings();
  },
};
</script>
