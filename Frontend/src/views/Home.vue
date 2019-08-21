<template>
  <div class="home">
    <div class="game" id="playArea" v-show="gameShown">
      <v-card v-show="countdownShown">
        <v-alert :value="positionsError" type="error">
          An error occured, please try again later
        </v-alert>
        <v-card-text>
          <v-form ref="settings">
            <v-layout align-center justify-space-around column fill-height>
              <v-flex xs12 sm6 md3 pa-2>
                <v-slider
                  v-model="settings.spacingMultiplier"
                  label="Spacing of the circles"
                >
                </v-slider>
              </v-flex>
              <v-flex xs12 sm6 md3 pa-2>
                <v-text-field
                  label="Key 1"
                  hint="Enter keyboard key for left click"
                  v-model.number="key1"
                  :rules="[rules.string]"
                ></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md3 pa-2>
                <v-text-field
                  label="Key 2"
                  hint="Enter keyboard key for right click"
                  v-model.number="key2"
                  :rules="[rules.string]"
                ></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md3 pa-2>
                <v-text-field
                  label="Number of circles"
                  hint="Enter the number of circles you want to click"
                  v-model.number="settings.numberOfCircles"
                  :rules="[rules.number]"
                ></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md3>
                <v-btn
                  class="countdown"
                  @click="startCountdown()"
                  :loading="loading"
                  large
                  depressed
                >
                  {{ countdown }}
                </v-btn>
                <v-dialog max-width="600px" v-model="instructionsShown">
                  <v-btn large depressed slot="activator" light
                    >Instructions</v-btn
                  >
                  <v-card>
                    <v-card-text>
                      <div class="title">
                        Instructions
                      </div>
                      <p>
                        <br />
                        The objective is to click circles as quickly as
                        possible, as accurately as possible. <br />
                        The very first circle is always in the top left corner
                        of the game, and by default you need to click the circle
                        with the thickest border. This can be changed in the
                        settings tab in the navigation bar or by using a
                        different skin.
                        <br />In settings, circle 1 is the circle you click, and
                        circle 2 is where circle 1 will move to once you click
                        it, and so on. There are 8 circles showing the path that
                        will be taken, but they can be made invisible by setting
                        the border size to 0, to prevent cluttering the screen.
                        <br />Skins can be accessed via other profiles, which
                        can be found in the rankings tab. <br />
                        You can also click by hovering over the circle and
                        pressing either of the keys specified by Key 1 and Key
                        2. Use the key names specified by the KeyboardEvent.key
                        property.
                      </p>
                      <v-btn depressed light @click="instructionsShown = false"
                        >Close</v-btn
                      >
                    </v-card-text>
                  </v-card>
                </v-dialog>
              </v-flex>
            </v-layout>
          </v-form>
        </v-card-text>
      </v-card>
      <v-card v-show="resultsShown">
        <v-alert :value="!checkLogin" type="error">
          Please make sure to log in to submit scores
        </v-alert>
        <v-card-text>
          <div v-if="checkLogin">
            <div v-show="score.submitted">
              <span>Total: {{ score.total.toPrecision(5) }}</span>
              <v-progress-linear v-model="totalBar"></v-progress-linear>
              <span>Aim: {{ score.aim.toPrecision(5) }}</span>
              <v-progress-linear v-model="aimBar"></v-progress-linear>
              <span>Stamina: {{ score.stamina.toPrecision(5) }}</span>
              <v-progress-linear v-model="staminaBar"></v-progress-linear>
              <span>Speed: {{ score.speed.toPrecision(5) }}</span>
              <v-progress-linear v-model="speedBar"></v-progress-linear>
            </div>
          </div>
          <v-layout align-center justify-space-around column fill-height>
            <v-flex xs12 sm6 md3 v-show="!score.submitted && checkLogin">
              <v-progress-circular
                indeterminate
                color="grey"
              ></v-progress-circular>
            </v-flex>
            <v-flex xs12 sm6 md3 v-show="score.submitted || !checkLogin">
              <v-btn depressed large @click="restart">
                Retry
              </v-btn>
            </v-flex>
          </v-layout>
        </v-card-text>
      </v-card>
      <button
        class="circle"
        id="8"
        v-show="
          !countdownShown &&
            currentCirclesPosition < settings.numberOfCircles - 6
        "
      ></button
      ><button
        class="circle"
        id="7"
        v-show="
          !countdownShown &&
            currentCirclesPosition < settings.numberOfCircles - 5
        "
      ></button
      ><button
        class="circle"
        id="6"
        v-show="
          !countdownShown &&
            currentCirclesPosition < settings.numberOfCircles - 4
        "
      ></button
      ><button
        class="circle"
        id="5"
        v-show="
          !countdownShown &&
            currentCirclesPosition < settings.numberOfCircles - 3
        "
      ></button
      ><button
        class="circle"
        id="4"
        v-show="
          !countdownShown &&
            currentCirclesPosition < settings.numberOfCircles - 2
        "
      ></button
      ><button
        class="circle"
        id="3"
        v-show="
          !countdownShown &&
            currentCirclesPosition < settings.numberOfCircles - 1
        "
      ></button
      ><button
        class="circle"
        id="2"
        v-show="
          !countdownShown && currentCirclesPosition < settings.numberOfCircles
        "
      ></button>
      <button
        class="circle hoverCheck"
        id="1"
        @click="nextPosition()"
        @keydown="keyDownClick"
        @mouseover="beginHover"
        @mouseleave="endHover"
        v-show="!countdownShown && !resultsShown"
      ></button>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import axios from "axios";

export default {
  data: function() {
    return {
      positionsError: false,
      hover: false,
      key1: "KeyZ",
      key2: "KeyX",
      gameShown: true,
      countdown: "Start",
      countdownShown: true,
      instructionsShown: false,
      resultsShown: false,
      loading: false,
      blockStart: false,
      blockCircle: false,
      coordinateSet: [0, 0],
      currentCirclesPosition: 0,
      settings: {
        numberOfCircles: 10,
        spacingMultiplier: 100
      },
      score: {
        startTime: 0,
        endTime: 0,
        total: 0,
        aim: 0,
        stamina: 0,
        speed: 0,
        submitted: false
      },
      rules: {
        number: input =>
          (Number.isInteger(input) && input > 0 && input < 99999) ||
          "Please enter an positive integer value below 99999",
        string: input =>
          (input.length > 0 && input.length < 20) ||
          "Please enter a string between 1 and 20 characters"
      }
    };
  },
  methods: {
    applySetup: function() {
      document.getElementById("playArea").style.width = this.skin.width + "px";
      document.getElementById("playArea").style.height =
        this.skin.height + "px";
      document.getElementById(
        "playArea"
      ).style.backgroundColor = this.skin.background;

      for (var i = 1; i < 9; i++) {
        document.getElementById(i.toString()).style.height =
          this.skin.circleSize + "px";
        document.getElementById(i.toString()).style.width =
          this.skin.circleSize + "px";
        document.getElementById(
          i.toString()
        ).style.backgroundColor = this.skin.circles[i - 1].backgroundColor;

        let checkedBorderSize;

        if (this.skin.circles[i - 1].borderSize * 2 > this.skin.circleSize) {
          checkedBorderSize = Math.floor(this.skin.circleSize / 2);
        } else {
          checkedBorderSize = this.skin.circles[i - 1].borderSize;
        }

        document.getElementById(i.toString()).style.border =
          checkedBorderSize +
          "px solid " +
          this.skin.circles[i - 1].borderColor;
      }
    },
    startCountdown: function() {
      // start request for array of positions
      // sending playarea, circlesize and spacing
      if (this.$refs.settings.validate()) {
        if (this.blockStart) {
          return;
        }
        this.blockStart = true;
        var that = this;
        this.loading = true;
        this.applySetup();
        axios
          .post("https://clickyeet-api.herokuapp.com/positions", {
            settings: {
              areaWidth: this.skin.width,
              areaHeight: this.skin.height,
              circleSize: this.skin.circleSize,
              numberOfCircles: this.settings.numberOfCircles,
              spacing: this.spacing
            }
          })
          .then(response => {
            this.coordinateSet = response.data.positions;
            this.loading = false;
            that.countdown = 3;
            var countdownFunction = setInterval(function() {
              that.countdown--;
              if (that.countdown == 0) {
                clearInterval(countdownFunction);
                that.countdownShown = false;
                that.blockStart = false;
                that.score.startTime = performance.now();
                that.nextPosition();
              }
            }, 1000);
          })
          .catch(() => {
            this.positionsError = true;
            this.loading = false;
          });
      }
    },
    keyDownClick: function(e) {
      if (this.keys.includes(e.code) && this.hover && !e.repeat) {
        this.nextPosition();
      }
    },
    beginHover: function() {
      document.getElementById("1").focus();
      this.hover = true;
    },
    endHover: function() {
      document.getElementById("1").blur();
      this.hover = false;
    },
    nextPosition: function() {
      if (this.blockCircle) {
        return;
      }
      this.blockCircle = true;
      if (
        window
          .getComputedStyle(document.getElementById("1"))
          .getPropertyValue("font-weight") === "1"
      ) {
        document.getElementById("1").blur();
      }

      var position = this.currentCirclesPosition;
      var circle = 1;
      for (; position < this.settings.numberOfCircles; position++) {
        if (circle < 9) {
          this.changeCoordinates(circle, position);
        } else break;
        circle++;
      }

      if (this.currentCirclesPosition === this.settings.numberOfCircles) {
        this.score.endTime = performance.now();
        this.displayResults();
      }

      this.currentCirclesPosition++;
      this.blockCircle = false;
    },
    changeCoordinates: function(circle, position) {
      document.getElementById(circle.toString()).style.left =
        this.coordinateSet[position][0] + "px";
      document.getElementById(circle.toString()).style.top =
        this.coordinateSet[position][1] + "px";
    },
    displayResults() {
      this.resultsShown = true;
      if (this.checkLogin) {
        axios
          .post("https://clickyeet-api.herokuapp.com/scores", {
            settings: {
              areaWidth: this.skin.width,
              areaHeight: this.skin.height,
              circleSize: this.skin.circleSize,
              numberOfCircles: this.settings.numberOfCircles,
              spacing: this.spacing
            },
            score: {
              timeTaken: this.score.endTime - this.score.startTime
            },
            userID: this.loginDetails.userID,
            password: this.loginDetails.password
          })
          .then(response => {
            this.score.total = response.data.total;
            this.score.aim = response.data.aim;
            this.score.stamina = response.data.stamina;
            this.score.speed = response.data.speed;
            this.score.submitted = response.data.submissionSuccess;
          });
      }
    },
    restart() {
      this.positionsError = false;
      this.hover = false;
      this.key1 = "KeyZ";
      this.key2 = "KeyX";
      this.gameShown = true;
      this.countdown = "Start";
      this.countdownShown = true;
      this.instructionsShown = false;
      this.resultsShown = false;
      this.loading = false;
      this.coordinateSet = [0, 0];
      this.currentCirclesPosition = 0;

      this.score = {
        startTime: 0,
        endTime: 0,
        total: 0,
        aim: 0,
        stamina: 0,
        speed: 0,
        submitted: false
      };
    }
  },
  computed: {
    ...mapGetters(["skin", "loginDetails", "checkLogin"]),
    spacing() {
      if (this.skin.height < this.skin.width) {
        return Math.round(
          (this.settings.spacingMultiplier *
            (this.skin.height - this.skin.circleSize)) /
            200
        );
      } else {
        return Math.round(
          (this.settings.spacingMultiplier *
            (this.skin.width - this.skin.circleSize)) /
            200
        );
      }
    },
    totalBar() {
      return 100;
    },
    aimBar() {
      return (100 * this.score.aim) / this.score.total;
    },
    staminaBar() {
      return (100 * this.score.stamina) / this.score.total;
    },
    speedBar() {
      return (100 * this.score.speed) / this.score.total;
    },
    keys() {
      return [this.key1, this.key2];
    }
  }
};
</script>

<style>
.game {
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
  cursor: pointer;
  position: absolute;
  outline: none;
  height: 0px;
  width: 0px;
  left: 0px;
  top: 0px;
}
.hoverCheck {
  font-weight: 1;
}
.hoverCheck:hover {
  font-weight: 2;
}
</style>
