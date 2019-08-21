<template>
  <v-dialog max-width="800px" v-model="showDialog">
    <v-btn depressed slot="activator" round light>Login/Register</v-btn>
    <v-card>
      <v-alert :value="loginError" type="error">
        Log in failed. Please enter a valid username and password.
      </v-alert>
      <v-card-text>
        <v-form ref="loginForm">
          <v-text-field
            label="Username"
            hint="Please enter your username"
            v-model="username"
            :rules="[inputRules.required]"
          ></v-text-field>
          <v-text-field
            v-model="password"
            :append-icon="showPassword1 ? 'visibility_off' : 'visibility'"
            :rules="[inputRules.required]"
            :type="showPassword1 ? 'text' : 'password'"
            label="Password"
            hint="Please enter your password"
            counter
            @click:append="showPassword1 = !showPassword1"
          ></v-text-field>
          <v-btn @click="login" depressed :loading="loginLoading">Log In</v-btn>
          <span class="caption grey--text"
            >Click anywhere outside the popup to close it</span
          >
        </v-form>
      </v-card-text>
    </v-card>
    <v-divider vertical></v-divider>
    <v-expansion-panel>
      <v-expansion-panel-content>
        <div slot="header">Register using this form</div>
        <v-card>
          <v-card-title class="title">
            Register
          </v-card-title>
          <v-alert :value="registerError" type="error">
            Sorry, couldn't register. Please make sure the username isn't taken.
          </v-alert>
          <v-alert
            :value="registrationPassword != confirmPassword"
            type="error"
          >
            Please make sure the passwords match.
          </v-alert>
          <v-card-text>
            <v-form ref="registerForm">
              <v-text-field
                label="Username"
                hint="Please enter your username"
                v-model="registrationUsername"
                :rules="[inputRules.required]"
                counter
                maxlength="20"
              ></v-text-field>
              <v-text-field
                v-model="registrationPassword"
                :append-icon="showPassword2 ? 'visibility_off' : 'visibility'"
                :rules="[inputRules.required]"
                :type="showPassword2 ? 'text' : 'password'"
                label="Password"
                hint="Please enter your password"
                counter
                @click:append="showPassword2 = !showPassword2"
              ></v-text-field>
              <v-text-field
                v-model="confirmPassword"
                :append-icon="showPassword3 ? 'visibility_off' : 'visibility'"
                :rules="[inputRules.required]"
                :type="showPassword3 ? 'text' : 'password'"
                label="Confirm password"
                hint="Please re enter your password to confirm it"
                counter
                @click:append="showPassword3 = !showPassword3"
              ></v-text-field>
              <p class="caption grey--text">
                <br />
                By registering you agree to allow your username and any activity
                on the account to be stored and analysed. The website is subject
                to change without notice and is used entirely at your own risk.
                I am not liable for any damage or harm caused by this website.
              </p>
              <v-btn @click="register" depressed :loading="registerLoading"
                >Register</v-btn
              >
            </v-form>
          </v-card-text>
        </v-card>
      </v-expansion-panel-content>
    </v-expansion-panel>
  </v-dialog>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
import axios from "axios";

export default {
  data: () => ({
    username: "",
    password: "",
    registrationUsername: "",
    registrationPassword: "",
    confirmPassword: "",
    inputRules: {
      required: userInput =>
        userInput.length >= 1 || "Please enter at least one character"
    },
    showPassword1: false,
    showPassword2: false,
    showPassword3: false,
    registerLoading: false,
    registerError: false,
    loginLoading: false,
    loginError: false
  }),
  computed: {
    ...mapGetters(["checkLogin"]),
    showDialog() {
      return !this.checkLogin;
    }
  },
  methods: {
    ...mapActions(["logOut", "logIn"]),
    logout: function() {
      this.logOut();
    },
    login: function() {
      if (this.$refs.loginForm.validate()) {
        this.loginLoading = true;
        axios
          .put("https://clickyeet-api.herokuapp.com/profile", {
            option: "LogIn",
            username: this.username,
            password: this.password
          })
          .then(response => {
            this.logIn({
              username: this.username,
              password: this.password,
              userID: response.data.userID
            });
            this.loginLoading = false;
          })
          .catch(() => {
            this.loginLoading = false;
            this.loginError = true;
          });
      }
    },
    register: function() {
      if (
        this.$refs.registerForm.validate() &&
        this.registrationPassword === this.confirmPassword
      ) {
        this.registerLoading = true;
        axios
          .post("https://clickyeet-api.herokuapp.com/profile", {
            username: this.registrationUsername,
            password: this.registrationPassword
          })
          .then(() => {
            axios
              .put("https://clickyeet-api.herokuapp.com/profile", {
                option: "LogIn",
                username: this.registrationUsername,
                password: this.registrationPassword
              })
              .then(response => {
                this.logIn({
                  username: this.registrationUsername,
                  password: this.registrationPassword,
                  userID: response.data.userID
                });
                this.registerLoading = false;
              })
              .catch(() => {
                this.registerLoading = false;
                this.registerError = true;
              });
          })
          .catch(() => {
            this.registerLoading = false;
            this.registerError = true;
          });
      }
    }
  }
};
</script>

<style></style>
