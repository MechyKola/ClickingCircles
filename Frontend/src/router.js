import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";
import Rankings from "./views/Rankings.vue";
import Settings from "./views/Settings.vue";
import OwnProfile from "./views/OwnProfile.vue";

Vue.use(Router);

export default new Router({
  mode: "history",
  base: process.env.BASE_URL,
  routes: [
    {
      path: "/",
      name: "home",
      component: Home
    },
    {
      path: "/r",
      name: "rankings",
      component: Rankings
    },
    {
      path: "/s",
      name: "settings",
      component: Settings
    },
    {
      path: "/u",
      name: "ownProfile",
      component: OwnProfile
    }
  ]
});
