<template>
  <div class="w-full flex items-center justify-center pt-3">
    <section
      class="form w-[400px] h-max text-center p-5 flex flex-col rounded-xl"
    >
      <h2 class="text-xl font-bold py-5">&nbsp;&nbsp;Login&nbsp;&nbsp;</h2>
      <div v-if="showError" class="error">
        Invalid credentials. Please try again.
      </div>

      <form @submit.prevent="login">
        <div>
          <label
            >Email<br /><input
              v-model="email"
              type="email"
              placeholder="Enter email..."
              required
              class="w-full py-3 px-5 my-2 border-2 border-black rounded-2xl"
          /></label>
        </div>
        <div>
          <label
            ><br />Password<br /><input
              v-model="password"
              type="password"
              placeholder="Enter password..."
              required
              class="w-full py-3 px-5 my-2 border-2 border-black rounded-2xl"
          /></label>
        </div>
        <div class="pt-5">
          <button
            class="submit w-full py-3 px-5 border-2 border-pink-200 rounded-2xl my-5 mx-auto hover:cursor-pointer text-pink-200 bg-black hover:border-black hover:bg-red-700"
            type="submit"
          >
            Login
          </button>
        </div>
        <div class="pt-5">
          Don't have an account?
          <router-link to="/authenticate/signup" style="color: red"
            >Sign Up</router-link
          >
        </div>
      </form>
    </section>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

export default {
  data() {
    return {
      email: "",
      password: "",
      showError: false,
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("http://localhost:5000/login", {
          email: this.email,
          password: this.password,
        });

        if (!response.data.error) {
          localStorage.setItem("accessToken", response.data.accessToken);
          window.location.reload();
        } else {
          Swal.fire({
            icon: "error",
            title: "Error",
            text: response.data.message,
          });
        }
      } catch (error) {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: "Something went wrong!",
        });

        console.error(error);
      }
    },
  },
};
</script>

<style>
/* Your provided CSS class */
</style>
