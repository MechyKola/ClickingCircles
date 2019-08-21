<template>
  <div class="profile" style="word-break: break-all">
    <v-card>
      <v-card-text>
        <div class="title">{{ user.username }}</div>
        <p></p>
        <div>
          <span class="grey--text">First seen </span>
          <span>{{ user.joinDate.substring(0, 19) }}</span>
        </div>
        <div>
          <span class="grey--text">Last seen </span>
          <span>{{ user.lastSeen.substring(0, 19) }}</span>
        </div>
        <div>
          <span>{{ user.playcount }}</span>
          <span class="grey--text"> Plays</span>
        </div>
        <div>
          <span>{{ user.hitcount }}</span>
          <span class="grey--text"> Total hits</span>
        </div>
      </v-card-text>
    </v-card>
    <v-expansion-panel>
      <v-expansion-panel-content>
        <div slot="header">Skins</div>
        <v-card v-for="skin in user.skins" :key="skin.name">
          <v-layout row>
            <v-flex xs4 class="my-1 mx-2">
              <div class="caption grey--text">Name</div>
              <div>{{ skin.name }}</div>
            </v-flex>
            <v-flex xs4 class="my-1 mx-2">
              <div class="caption grey--text">Uploaded</div>
              <div>{{ skin.created.substring(0, 19) }}</div>
            </v-flex>
            <v-flex xs2>
              <v-btn @click="loadSkin(skin.name)" depressed>
                Load
              </v-btn>
            </v-flex>
            <v-flex xs2 class="text-xs-right">
              <v-btn @click="addUser(skin.name)" depressed>
                Save
              </v-btn>
            </v-flex>
          </v-layout>
          <v-divider></v-divider>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
    <v-expansion-panel>
      <v-expansion-panel-content>
        <div slot="header">Scores</div>
        <v-card v-for="score in user.scores" :key="score.datetime">
          <v-layout row>
            <v-flex xs4 class="my-1 mx-2">
              <div class="caption grey--text">Total</div>
              <div>{{ score.total.toFixed(0) }}</div>
            </v-flex>
            <v-flex xs2 class="my-1 mx-2">
              <div class="caption grey--text">Aim</div>
              <div>{{ score.aim.toFixed(0) }}</div>
            </v-flex>
            <v-flex xs2 class="my-1 mx-2">
              <div class="caption grey--text">Stamina</div>
              <div>{{ score.stamina.toFixed(0) }}</div>
            </v-flex>
            <v-flex xs2 class="my-1 mx-2">
              <div class="caption grey--text">Speed</div>
              <div>{{ score.speed.toFixed(0) }}</div>
            </v-flex>
            <v-flex xs2 class="my-1 mx-2">
              <div class="caption grey--text">Date and Time</div>
              <div>{{ score.datetime.substring(0, 19) }}</div>
            </v-flex>
          </v-layout>
          <v-divider></v-divider>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import axios from "axios";

export default {
  data() {
    return {
      user: {},
      message: "uh"
    };
  },
  methods: {
    ...mapActions(["saveSkin"]),
    loadSkin(name) {
      axios
        .get(
          "https://clickyeet-api.herokuapp.com/skins?name=" + name.toString()
        )
        .then(response => {
          var newSkin = response.data;
          delete newSkin.created;
          delete newSkin.name;
          this.saveSkin(newSkin);
        })
        .catch(() => {
          this.message = "error";
        });
    },
    addUser(name) {
      axios
        .put("https://clickyeet-api.herokuapp.com/skins", {
          option: "add",
          name: name,
          userID: this.loginDetails.userID,
          password: this.loginDetails.password
        })
        .then(response => {
          this.message = response.data;
        })
        .catch(() => {
          this.message = "error";
        });
    }
  },
  computed: {
    ...mapGetters(["skin", "loginDetails"])
  },
  mounted() {
    if (this.userID === 0) {
      this.userID = this.loginDetails.userID;
    }
    axios
      .get(
        "https://clickyeet-api.herokuapp.com/profile?userID=" +
          this.userID.toString() +
          "&scorePage=1"
      )
      .then(response => {
        this.user = response.data;
      })
      .catch(() => {
        this.user = "error";
      });
  },
  props: {
    userID: {
      type: Number,
      default: 0
    }
  }
};
</script>
