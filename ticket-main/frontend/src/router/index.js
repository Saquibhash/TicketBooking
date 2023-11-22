import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue'
import BuyTickets from '../views/BuyTickets.vue'
import Profile from '../views/Profile.vue'
import Movies from '../views/Movies.vue'
import MovieDetails from '../views/MovieDetails.vue'
import Bookings from "../views/Bookings.vue";
import ManageBooking from '../views/ManageBooking.vue'
import Show from '../views/Show.vue'
import Venue from '../views/Venue.vue'
import UpdateVenue from '../views/UpdateVenue.vue'
import UpdateShow from '../views/UpdateShow.vue'
import BookTicket from '../views/BookTicket.vue'
import GetMovie from '../views/GetMovie.vue'
import SearchResult from '../views/SearchResult.vue'
import axios from 'axios';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile
    },
    {
      path: '/movies',
      name: 'movies',
      component: Movies
    },
    {
      path: '/buy-tickets',
      name: 'buy-ticket',
      component: BuyTickets
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup,
    },
    {
      path: '/update-movie/:id', 
      name: 'movie-details', 
      component: MovieDetails,
      props: true,
    },
    {
      path: '/bookings', 
      name: 'bookings', 
      component: Bookings,
    },
    {
      path: '/manage-booking/:id', 
      name: 'manage-booking', 
      component: ManageBooking,
      props: true,
    },
    {
      path: '/shows', 
      name: 'shows', 
      component: Show,
    },
    {
      path: '/venue', 
      name: 'venue', 
      component: Venue,
    },
    {
      path: '/search', 
      name: 'search', 
      component: SearchResult,
    },
    {
      path: '/update-venue/:id', 
      name: 'venue-update', 
      component: UpdateVenue,
      props: true,
    },
    {
      path: '/update-show/:id', 
      name: 'venue-show', 
      component: UpdateShow,
      props: true,
    },
    {
      path: '/book-ticket/:id', 
      name: 'book-ticket', 
      component: BookTicket,
      props: true,
    },
    {
      path: '/movies/:id', 
      name: 'movie-byid', 
      component: GetMovie,
      props: true,
    },
  ]
})
router.beforeEach(async (to, from, next) => {
  const publicPages = ['/login', '/signup', '/'];
  const authRequired = !publicPages.includes(to.path);
  const accessToken = localStorage.getItem('accessToken');

  if (authRequired && !accessToken) {
    next('/login');
  } else if (accessToken && (to.path === '/login' || to.path === '/signup')) {
    next('/');
  } else {
    if (accessToken) {
      try {
        const response = await axios.get('http://localhost:5000/validate', {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        if (response.data.success) {
          next();
        } else {
          console.error('Token is expired or not valid, or user is not authorized. Redirecting to login page.');
          next('/login');
        }
      } catch (error) {
        console.error('Error fetching user role:', error);
        next('/login');
      }
    } else {
      next(); 
    }
  }
});
export default router
