<script setup>
import { RouterLink, RouterView } from "vue-router";
import { ref, computed, onMounted } from "vue";
import axios from "axios";

const accessToken = localStorage.getItem("accessToken");
const authenticated = ref(accessToken !== null);
const isManager = ref(false); // Initialize isManager as false initially

function logout() {
  localStorage.removeItem("accessToken");
  authenticated.value = false;
}

const isAuthenticated = computed(() => authenticated.value);

// Function to fetch the user role from the API
async function fetchUserRole() {
  try {
    const response = await axios.get("http://localhost:5000/validate", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });
    if (response.data.success) {
      if (response?.data?.manager) {
        isManager.value = true;
      }
    } else {
      isManager.value = false;
    }
  } catch (error) {
    console.error("Error fetching user role:", error);
  }
}

// Fetch user role on component mount
onMounted(() => {
  if (isAuthenticated.value) {
    fetchUserRole();
  }
});
</script>

<template>
  <header class="header overflow-hidden bg-[rgb(61, 35, 40)] p-10 text-center">
    <div>
      <h1 class="text-[40px] font-[palatino] text-pink-200 font-bold">
        BOOK MY TICKET
      </h1>
      <nav>
        <template v-if="authenticated">
          <template v-if="isManager">
            <router-link
              class="text-red-300 p-3 text-lg hover:bg-red-800 hover:text-white rounded-xl"
              to="/"
              >Home</router-link
            >
            <router-link
              class="text-red-300 p-3 text-lg hover:bg-red-800 hover:text-white rounded-xl"
              to="/bookings"
              >Bookings</router-link
            >
            <router-link
              class="text-red-300 p-3 text-lg hover:bg-red-800 hover:text-white rounded-xl"
              to="/shows"
              >Shows</router-link
            >
            <router-link
              class="text-red-300 p-3 text-lg hover:bg-red-800 hover:text-white rounded-xl"
              to="/venue"
              >Venues</router-link
            >
            <router-link
              class="text-red-300 p-3 text-lg hover:bg-red-800 hover:text-white rounded-xl"
              to="/movies"
              >Movies</router-link
            >
            <a
              href="#"
              @click="logout"
              class="text-red-300 p-3 text-lg hover:bg-red-800 hover:text-white rounded-xl"
              >Log out</a
            >
          </template>
          <template v-else>
            <router-link
              class="text-red-300 p-3 text-lg hover:bg-red-800 hover:text-white rounded-xl"
              to="/"
              >Home</router-link
            >
            <router-link
              class="text-red-300 p-3 text-lg hover:bg-red-800 hover:text-white rounded-xl"
              to="/profile"
              >Profile</router-link
            >
            <router-link
              class="text-red-300 p-3 text-lg hover:bg-red-800 hover:text-white rounded-xl"
              to="/buy-tickets"
              >Buy Tickets</router-link
            >
            <a
              href="#"
              @click="logout"
              class="text-red-300 p-3 text-lg hover:bg-red-800 hover:text-white rounded-xl"
              >Log out</a
            >
          </template>
        </template>
        <template v-else>
          <router-link
            class="text-red-300 p-3 text-lg hover:bg-red-800 hover:text-white rounded-xl"
            to="/"
            >Home</router-link
          >
          <router-link
            class="text-red-300 p-3 text-lg hover:bg-red-800 hover:text-white rounded-xl"
            to="/signup"
            >Sign Up</router-link
          >
          <router-link
            class="text-red-300 p-3 text-lg hover:bg-red-800 hover:text-white rounded-xl"
            to="/login"
            >Login</router-link
          >
        </template>
      </nav>
    </div>
  </header>
  <footer
    class="w-full header text-center text-white absolute bottom-0 pb-2 text-sm"
  >
    21f1004600-MAD-1-IITM
  </footer>

  <RouterView />
</template>

<style scoped></style>
