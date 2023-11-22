<template>
    <div class="w-full flex items-center justify-center pt-3">
      <section class="form w-[400px] h-max text-center p-5 flex flex-col rounded-xl">
        <h2 class="text-xl font-bold py-5">&nbsp;&nbsp;Sign Up&nbsp;&nbsp;</h2>
        <div v-if="showError" class="error text-red-500">
          {{ errorMessage }}
        </div>
  
        <form @submit.prevent="signup">
          <div>
            <label>Email: <input v-model="email" type="email" placeholder="Enter email..." required class="w-full py-3 px-5 my-2 border-2 border-black rounded-2xl" /></label>
          </div>
          <div>
            <label>User name: <input v-model="username" type="text" placeholder="Enter username..." required class="w-full py-3 px-5 my-2 border-2 border-black rounded-2xl" /></label>
          </div>
          <div>
            <label>Password: <input v-model="password" type="password" placeholder="Enter password..." required class="w-full py-3 px-5 my-2 border-2 border-black rounded-2xl" /></label>
          </div>
          <div>
            <label>Re-enter Password: <input v-model="passwordRepeat" type="password" placeholder="Re-enter password..." required class="w-full py-3 px-5 my-2 border-2 border-black rounded-2xl" /></label>
          </div>
          <div>
            <input type="radio" v-model="role" value="manager" id="manager" required />
            <label for="manager">I am a manager</label>
            <input type="radio" v-model="role" value="customer" id="customer" required />
            <label for="customer">I am a customer</label>
          </div>
  
          <div>
            <button class="submit w-full py-3 px-5 border-2 border-pink-200 rounded-2xl my-5 mx-auto hover:cursor-pointer text-pink-200 bg-black hover:border-black hover:bg-red-700" type="submit">
              Sign Up
            </button>
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
        username: "",
        password: "",
        passwordRepeat: "",
        role: "manager", // Default value for radio buttons
        showError: false,
        errorMessage: "",
      };
    },
    methods: {
      async signup() {
        try {
          if (this.password !== this.passwordRepeat) {
            this.showError = true;
            this.errorMessage = "Passwords do not match.";
            return;
          }
          console.log(this.password);
          const response = await axios.post("http://localhost:5000/signup", {
            email: this.email,
            username: this.username,
            password: this.password,
            role: this.role,
          });
  
          if (!response.data.error) {
            Swal.fire({
              icon: "success",
              title: "Success",
              text: "You have successfully signed up.",
            });
  
            this.$router.push("/login"); // Redirect to the login page after successful signup
          } else {
            this.showError = true;
            this.errorMessage = response.data.message;
          }
        } catch (error) {
          this.showError = true;
          this.errorMessage = "An error occurred during sign up.";
          console.error(error);
        }
      },
    },
  };
  </script>
  
  <style>
  /* Your Tailwind CSS styles */
  </style>
  