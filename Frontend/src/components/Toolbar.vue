<template>
  <div class="toolbar">
    <v-snackbar v-model="snackbar" :timeout="2000" top>
      <span>You're now logged in!</span>
      <v-btn flat @click="snack = false">Close</v-btn>
    </v-snackbar>

    <v-toolbar app dark flat dense>
      <v-toolbar-title class="headline text-uppercase">
        <span>click</span>
        <span class="font-weight-light">yeet</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-toolbar-items>
        <v-btn
          v-for="link in links"
          router
          :key="link.name"
          :to="link.route"
          flat
        >
          {{ link.name }}
        </v-btn>
        <v-btn v-show="checkLogin" router to="/u" flat>
          Welcome back, {{ loginDetails.username }}
        </v-btn>
      </v-toolbar-items>
      <Login v-show="!checkLogin" class="my-0" block />
    </v-toolbar>
  </div>
</template>

<script>
import Login from "./Login";
import { mapGetters } from "vuex";

export default {
  name: "App",
  data() {
    return {
      links: [
        { name: "Home", route: "/" },
        { name: "Rankings", route: "/r" },
        { name: "Settings", route: "/s" }
      ],
      snack: true
    };
  },
  computed: {
    ...mapGetters(["checkLogin", "loginDetails"]),
    snackbar() {
      return this.snack && this.checkLogin;
    }
  },
  components: {
    Login
  }
};
</script>
