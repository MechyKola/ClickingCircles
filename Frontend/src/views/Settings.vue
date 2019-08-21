<template>
  <div class="settings">
    <v-snackbar v-model="skinUploaded" :timeout="2000" top>
      <span>{{ this.skinUploadMessage }}</span>
      <v-btn flat @click="skinUploaded = false">Close</v-btn>
    </v-snackbar>
    <v-container my-5>
      <div v-show="checkLogin">
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
              <v-btn
                @click="removeUser(skin.name)"
                depressed
                :loading="skin.loading"
              >
                Remove
              </v-btn>
            </v-flex>
          </v-layout>
          <v-divider></v-divider>
        </v-card>
      </div>
      <v-expansion-panel>
        <v-expansion-panel-content>
          <div slot="header">Current skin settings and preview</div>
          <div class="area" id="testArea">
            <button class="circle" id="displayCircle" ma-5></button>
          </div>
          <v-card>
            <v-card-title class="title">
              General settings
            </v-card-title>
            <v-card-text>
              <v-form ref="settingsEdit">
                <v-container>
                  <v-layout row wrap>
                    <v-flex xs12 sm6 md3 pa-2>
                      <v-text-field
                        label="Width"
                        hint="How wide the play area should be, in pixels"
                        v-model.number="skin.width"
                        :rules="[rules.number]"
                      ></v-text-field>
                    </v-flex>
                    <v-flex xs12 sm6 md3 pa-2>
                      <v-text-field
                        label="Height"
                        hint="How tall the play area should be, in pixels"
                        v-model.number="skin.height"
                        :rules="[rules.number]"
                      ></v-text-field>
                    </v-flex>
                    <v-flex xs12 sm6 md3 pa-2>
                      <v-text-field
                        label="Circle size"
                        hint="The diameter of the circles, in pixels"
                        v-model.number="skin.circleSize"
                        :rules="[rules.circleSize]"
                      ></v-text-field>
                    </v-flex>
                    <v-flex xs12 sm6 md3 pa-2>
                      <v-text-field
                        label="Background color"
                        hint="Enter a hex code starting with '#', or name a color"
                        v-model="skin.background"
                      ></v-text-field>
                    </v-flex>
                  </v-layout>
                </v-container>
              </v-form>
            </v-card-text>
          </v-card>
          <v-card>
            <v-card-title class="title">Circle settings</v-card-title>
            <v-card-text>
              <v-menu offset-y>
                <v-btn slot="activator" depressed>
                  Circle {{ currentCircle + 1 }}
                </v-btn>
                <v-list>
                  <v-list-tile
                    v-for="(circle, index) in skin.circles"
                    :key="index"
                    @click="currentCircle = index"
                  >
                    <v-list-tile-title
                      >Circle {{ index + 1 }}</v-list-tile-title
                    >
                  </v-list-tile>
                </v-list>
              </v-menu>
              <v-form ref="circleEdit">
                <v-container>
                  <v-layout>
                    <v-flex xs12 sm6 md3 pa-2>
                      <v-slider
                        v-model="skin.circles[currentCircle].borderSize"
                        label="Border size"
                      >
                      </v-slider>
                    </v-flex>
                    <v-flex xs12 sm6 md3 pa-2>
                      <v-text-field
                        label="Border color"
                        hint="Enter a hex code starting with '#', or name a color"
                        v-model="skin.circles[currentCircle].borderColor"
                      ></v-text-field>
                    </v-flex>
                    <v-flex xs12 sm6 md3 pa-2>
                      <v-text-field
                        label="Background color"
                        hint="Enter a hex code starting with '#', or name a color"
                        v-model="skin.circles[currentCircle].backgroundColor"
                      ></v-text-field>
                    </v-flex>
                  </v-layout>
                </v-container>
              </v-form>
            </v-card-text>
          </v-card>
          <v-card>
            <v-card-text>
              <v-btn @click="updateCurrentSkin" depressed>
                Check in preview
              </v-btn>
              <v-btn @click="saveCurrentSkin" depressed>Save</v-btn>
              <v-dialog max-width="800px" v-model="skinForm">
                <v-btn depressed slot="activator" v-show="checkLogin"
                  >Upload currently saved skin</v-btn
                >
                <v-card>
                  <v-alert :value="skinUploadError" type="error">
                    Unable to upload skin. Please make sure the name is unique.
                  </v-alert>
                  <v-card-text>
                    <v-form ref="uploadSkinForm">
                      <v-text-field
                        label="Skin name"
                        hint="Enter what you want the skin to be called"
                        v-model="skinName"
                        :rules="[]"
                      ></v-text-field>
                    </v-form>
                    <v-btn
                      depressed
                      @click="uploadSkin"
                      :loading="skinUploading"
                      >Upload</v-btn
                    >
                    <v-btn depressed @click="skinForm = false">Cancel</v-btn>
                  </v-card-text>
                </v-card>
              </v-dialog>
            </v-card-text>
          </v-card>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-container>
  </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import axios from "axios";

export default {
  data() {
    return {
      skinName: "",
      skinForm: false,
      skinUploading: false,
      skinUploaded: false,
      skinUploadError: false,
      skinUploadMessage: "",
      currentCircle: 0,
      user: {},
      rules: {
        number: input =>
          (input > 0 && input < 9999 && Number.isInteger(input)) ||
          "Please enter a positive integer value below 9999",
        circleSize: input =>
          (input > 0 &&
            input < 9999 &&
            Number.isInteger(input) &&
            input < this.skin.height &&
            input < this.skin.width) ||
          "Please enter a positive integer value below 9999 smaller than height and width"
      }
    };
  },
  methods: {
    updateCurrentSkin() {
      if (
        this.$refs.circleEdit.validate() &&
        this.$refs.settingsEdit.validate()
      ) {
        document.getElementById("testArea").style.width =
          this.skin.width + "px";
        document.getElementById("testArea").style.height =
          this.skin.height + "px";
        document.getElementById(
          "testArea"
        ).style.backgroundColor = this.skin.background;
        document.getElementById("displayCircle").style.height =
          this.skin.circleSize + "px";
        document.getElementById("displayCircle").style.width =
          this.skin.circleSize + "px";
        document.getElementById(
          "displayCircle"
        ).style.background = this.skin.circles[
          this.currentCircle
        ].backgroundColor;

        let checkedBorderSize;

        if (
          this.skin.circles[this.currentCircle].borderSize * 2 >
          this.skin.circleSize
        ) {
          checkedBorderSize = Math.floor(this.skin.circleSize / 2);
        } else {
          checkedBorderSize = this.skin.circles[this.currentCircle].borderSize;
        }

        document.getElementById("displayCircle").style.border =
          checkedBorderSize +
          "px solid " +
          this.skin.circles[this.currentCircle].borderColor;
      }
    },
    saveCurrentSkin() {
      if (this.$refs.settingsEdit.validate()) {
        this.saveSkin(this.skin);
      }
    },
    uploadSkin() {
      if (this.$refs.uploadSkinForm.validate() && this.checkLogin) {
        var skinToUpload = this.skin;
        skinToUpload.name = this.skinName;
        skinToUpload.creator = this.loginDetails.userID.toString();
        skinToUpload.password = this.loginDetails.password;

        this.skinUploading = true;
        this.skinUploaded = false;

        axios
          .post("https://clickyeet-api.herokuapp.com/skins", skinToUpload)
          .then(response => {
            this.skinUploadMessage = response.data.message;
            this.skinUploaded = true;
            this.skinUploading = false;
            this.skinForm = false;

            axios
              .put("https://clickyeet-api.herokuapp.com/skins", {
                option: "add",
                name: this.skinName,
                userID: this.loginDetails.userID,
                password: this.loginDetails.password
              })
              .then(() => {
                this.updateUser();
              });
          })
          .catch(() => {
            this.skinUploadError = true;
            this.skinUploading = false;
          });
      }
    },
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
    removeUser(name) {
      axios
        .put("https://clickyeet-api.herokuapp.com/skins", {
          option: "remove",
          name: name,
          userID: this.loginDetails.userID,
          password: this.loginDetails.password
        })
        .then(response => {
          this.message = response.data;
          this.updateUser();
        })
        .catch(() => {
          this.message = "error";
          this.updateUser();
        });
    },
    updateUser() {
      axios
        .get(
          "https://clickyeet-api.herokuapp.com/profile?userID=" +
            this.loginDetails.userID.toString() +
            "&scorePage=1"
        )
        .then(response => {
          this.user = response.data;
        })
        .catch(() => {
          this.user = "error";
        });
    },
    ...mapActions(["saveSkin"])
  },
  computed: {
    ...mapGetters(["skin", "loginDetails", "checkLogin"])
  },
  mounted() {
    if (this.checkLogin) {
      this.updateUser();
    }
  }
};
</script>

<style>
.area {
  background-color: black;
  margin: auto auto;
  padding: 0 0;
  width: 800px;
  height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.circle {
  border-radius: 50%;
  border: 10px solid white;
  cursor: pointer;
  position: absolute;
  outline: none;
  height: 10px;
  width: 10px;
  left: 0px;
  top: 0px;
}
</style>
