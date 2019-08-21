<template>
  <div class="rankings">
    <v-container class="my-5">
      <v-layout row>
        <v-btn depressed @click="sortUsers('total')">
          <span class="caption">Sort by total</span>
        </v-btn>
        <v-btn depressed @click="sortUsers('aim')">
          <span class="caption">Sort by aim</span>
        </v-btn>
        <v-btn depressed @click="sortUsers('stamina')">
          <span class="caption">Sort by stamina</span>
        </v-btn>
        <v-btn depressed @click="sortUsers('speed')">
          <span class="caption">Sort by speed</span>
        </v-btn>
        <v-btn depressed @click="previousPage()">
          <v-icon>chevron_left</v-icon>
        </v-btn>
        <v-btn depressed @click="nextPage()">
          <v-icon>chevron_right</v-icon>
        </v-btn>
      </v-layout>
      <v-card v-for="user in users" :key="user.total">
        <v-layout row style="word-break: break-all">
          <v-flex xs2 class="my-1 mx-2">
            <div class="caption grey--text">Username</div>
            <div>{{ user.username }}</div>
          </v-flex>
          <v-flex xs2 class="my-1 mx-2">
            <div class="caption grey--text">Total</div>
            <div>{{ user.total.toFixed(0) }}</div>
          </v-flex>
          <v-flex xs2 class="my-1 mx-2">
            <div class="caption grey--text">Aim</div>
            <div>{{ user.aim.toFixed(0) }}</div>
          </v-flex>
          <v-flex xs2 class="my-1 mx-2">
            <div class="caption grey--text">Stamina</div>
            <div>{{ user.stamina.toFixed(0) }}</div>
          </v-flex>
          <v-flex xs2 class="my-1 mx-2">
            <div class="caption grey--text">Speed</div>
            <div>{{ user.speed.toFixed(0) }}</div>
          </v-flex>
          <v-flex xs2 class="text-xs-right">
            <v-dialog>
              <v-btn slot="activator" depressed>
                View profile
              </v-btn>
              <v-card
                ><v-card-text> <Profile :userID="user.userID" /> </v-card-text
              ></v-card>
            </v-dialog>
          </v-flex>
        </v-layout>
        <v-divider></v-divider>
      </v-card>
    </v-container>
  </div>
</template>

<script>
import Profile from "../components/Profile.vue";
import axios from "axios";

export default {
  data() {
    return {
      users: [],
      sortBy: "total",
      page: 1
    };
  },
  methods: {
    sortUsers(byThis) {
      this.sortBy = byThis;
      this.users = this.mergeSort(this.users);
    },
    mergeSort: function(array) {
      if (array.length < 2) return array;
      var middle = Math.floor(array.length / 2);
      var left = array.slice(0, middle);
      var right = array.slice(middle, array.length);

      return this.merge(this.mergeSort(left), this.mergeSort(right));
    },
    merge: function(left, right) {
      var sortedArray = [];

      while (left.length && right.length) {
        if (left[0][this.sortBy] > right[0][this.sortBy]) {
          sortedArray.push(left.shift());
        } else {
          sortedArray.push(right.shift());
        }
      }

      while (left.length) sortedArray.push(left.shift());

      while (right.length) sortedArray.push(right.shift());

      return sortedArray;
    },
    nextPage() {
      if (this.users.length > 49) {
        this.page++;
        this.updateUsers();
      }
    },
    previousPage() {
      if (this.page > 1) {
        this.page--;
        this.updateUsers();
      }
    },
    updateUsers() {
      axios
        .get(
          "https://clickyeet-api.herokuapp.com/rankings?scorePage=" +
            this.page.toString()
        )
        .then(response => {
          this.users = response.data.users;
        })
        .catch(() => {
          this.users = "error";
        });
    }
  },
  created() {
    this.updateUsers();
  },
  components: {
    Profile
  }
};
</script>
