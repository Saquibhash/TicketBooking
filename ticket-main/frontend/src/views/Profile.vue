<template>
  <section>
    <h3
      style="
        text-align: center;
        background-color: rgba(255, 0, 0, 0.363);
        height: 50px;
        line-height: 50px;
        font-family: 'Courier New', monospace;
      "
    >
      &nbsp;&nbsp;Welcome to Your Profile
      {{ user?.name.toUpperCase() }}&nbsp;&nbsp;
    </h3>
    <h2>&nbsp;&nbsp;Current bookings&nbsp;&nbsp;</h2>
    <template v-if="now_bookings.length > 0">
      <table class="table-bookings">
        <thead>
          <tr>
            <th>Movie Poster</th>
            <th>Title</th>
            <th>Venue</th>
            <th>Location</th>
            <th>Seats Reserved</th>
            <th>Day</th>
            <th>Time</th>
            <th>Booked Day</th>
            <!-- Add more table headers if needed -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="booking in now_bookings" :key="booking.id">
            <td>
              <img
                :src="booking.movie.img"
                width="120"
                style="border-radius: 15px"
              />
            </td>
            <td>{{ booking.movie.title }}</td>
            <td>{{ booking.venue.name }}</td>
            <td>{{ booking.venue.location }}</td>
            <td>{{ booking.num_seats }}</td>
            <td>{{ booking.show.day}}</td>
            <td>{{ booking.show.time }}</td>
            <td>{{ booking.date_time }}</td>
            <!-- Add more table cells if needed -->
          </tr>
        </tbody>
      </table>
    </template>
    <template v-else>
      <p style="text-align: center">YOU DON'T HAVE BOOKED BOOKINGS.</p>
    </template>
    <h2>&nbsp;&nbsp;Past bookings&nbsp;&nbsp;</h2>
    <template v-if="past_bookings.length > 0">
      <table class="table-bookings">
        <thead>
          <tr>
            <th>Movie Poster</th>
            <th>Title</th>
            <th>Venue</th>
            <th>Location</th>
            <th>Seats Reserved</th>
            <th>Day</th>
            <th>Time</th>
            <th>Booked Day</th>
            <!-- Add more table headers if needed -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="booking in past_bookings" :key="booking.id">
            <td>
                <img
                  :src="booking.movie.img"
                  width="120"
                  style="border-radius: 15px"
                />
            </td>
            <td>{{ booking.movie.title }}</td>
            <td>{{ booking.venue.name }}</td>
            <td>{{ booking.venue.location }}</td>
            <td>{{ booking.num_seats }}</td>
            <td>{{ booking.show.day }}</td>
            <td>{{ booking.show.time }}</td>
            <td>{{ booking.date_time }}</td>
            <!-- Add more table cells if needed -->
          </tr>
        </tbody>
      </table>
    </template>
    <template v-else>
      <p style="text-align: center">YOU DON'T HAVE PAST BOOKED BOOKINGS.</p>
    </template>
  </section>
</template>

<script setup>
import axios from "axios";
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";

const user = ref(null);
const now_bookings = ref([]);
const past_bookings = ref([]);

const router = useRouter();

onMounted(async () => {
  try {
    const accessToken = localStorage.getItem("accessToken");
    const userResponse = await axios.get("http://localhost:5000/user", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    user.value = userResponse.data?.user;
    now_bookings.value = userResponse.data?.now_bookings;
    past_bookings.value = userResponse.data?.past_bookings;
    console.log(userResponse, "----------------");
  } catch (error) {
    console.error("Error fetching data:", error);
  }
});
</script>

<style>
/* Your header styles and table styles */
</style>
