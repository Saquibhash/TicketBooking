<template>
  <div>
    <div class="w-full space-y-8">
      <section>
        <h2 class="pt-6 text-center text-2xl font-semibold pb-6">
          See Other Options
        </h2>
        <table class="table-movies">
          <thead>
            <tr>
              <th>Movie Poster</th>
              <th>Title</th>
              <th>Venue</th>
              <th>Location</th>
              <th>Seats Available</th>
              <th>Day</th>
              <th>Time</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="show in todayShowsData"
              :key="show.id"
              :id="'sh' + show.id"
            >
              <td>
                <a href="#"
                  ><img
                    :src="show.movie.img"
                    width="80"
                    style="border-radius: 15px"
                /></a>
              </td>
              <td>{{ show.movie?.title }}</td>
              <td>{{ show.venue?.name }}</td>
              <td>{{ show.venue?.location }}</td>
              <td>{{ show?.seats_available }}</td>
              <td>{{ show.day }}</td>
              <td>{{ show.time }}</td>
              <td class="sold">
                <a class="buttom" :href="getBuyTicketLink(show?.id)">
                  Buy Ticket
                </a>
              </td>
            </tr>
            <tr
              v-for="show in comingSoonData"
              :key="show.id"
              :id="'sh' + show.id"
            >
              <td>
                <a href="#"
                  ><img
                    :src="show.movie.img"
                    width="80"
                    style="border-radius: 15px"
                /></a>
              </td>
              <td>{{ show.movie?.title }}</td>
              <td>{{ show.venue?.name }}</td>
              <td>{{ show.venue?.location }}</td>
              <td>{{ show?.seats_available }}</td>
              <td>{{ show.day }}</td>
              <td>{{ show.time }}</td>
              <td class="sold">
                <a v-if="show.seats_available > 0" class="buttom" :href="getBuyTicketLink(show?.id)">
                  Buy Ticket
                </a>
                <span v-else class="house-full">House Full</span>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="comingSoonData.length === 0" class="text-center mt-4">
          <p>No shows coming soon.</p>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      searchQuery: "",
      moviesData: [],
      todayShowsData: [],
      comingSoonData: [],
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    getBuyTicketLink(showId) {
      return `/book-ticket/${showId}`;
    },
    async fetchData() {
      try {
        const accessToken = localStorage.getItem("accessToken");
        const response = await axios.get("http://localhost:5000/", {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.moviesData = response.data.all_movies;
        this.todayShowsData = response.data.today_shws;
        this.comingSoonData = response.data.next_shws;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    async createBookingonID(showId, numSeats) {
      try {
        const accessToken = localStorage.getItem("accessToken");
        if (!accessToken) {
          Swal.fire({
            icon: "error",
            title: "Login First",
          });
        } else {
          const response = await axios.post(
            "http://localhost:5000/booking/",
            {
              shw: showId,
              seats: show?.seats_available,
            },
            {
              headers: {
                Authorization: `Bearer ${accessToken}`,
              },
            }
          );
          Swal.fire({
            icon: "success",
            title: "Ticket Booked!",
            text: "Your ticket has been successfully booked.",
            confirmButtonColor: "#3085d6",
            confirmButtonText: "OK",
          });
        }
      } catch (error) {
        console.error("Error creating booking:", error);
      }
    },
  },
};
</script>

<style>
.horizontal-movies {
  margin: 0 auto;
  display: grid;
  grid-auto-flow: column;
  gap: 1rem;
  padding: 1rem;
  width: 100%;
  overflow-y: auto;
  overscroll-behavior-x: contain;
  scroll-snap-type: x mandatory;
}
.horizontal-movies > a {
  scroll-snap-align: center;
}

.horizontal-movies img {
  width: 180px;
  max-width: none;
  object-fit: contain;
  border-radius: 15px;
}
table {
  display: table;
  margin-right: auto;
  margin-left: auto;
  width: 100%;
}
table td,
table th {
  text-align: center;
  border: 1px solid rgb(178, 255, 230);
}

td {
  height: 75px; /*min height*/
}

.buttom {
  overflow: hidden;
  white-space: nowrap; /*avoids the bad resizing when window smaller*/
  color: white;
  text-align: center;
  padding: 12px;
  text-decoration: none; /* without link line*/
  font-size: 12px;
  line-height: 25px;
  border-radius: 12px;
  background-color: rgb(8, 4, 21);
  border: 2px solid rgba(183, 26, 94, 1);
}
/* Change the background color on mouse-over */
.buttom:hover {
  background-color: rgba(183, 26, 94, 1);
  border: 2px solid rgb(8, 4, 21);
}
</style>
