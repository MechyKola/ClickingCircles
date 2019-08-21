import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    username: "",
    password: "",
    userID: "",
    loggedIn: false,
    skin: {
      background: "black",
      width: 800,
      height: 600,
      circleSize: 100,
      circles: [
        {
          backgroundColor: "black",
          borderColor: "white",
          borderSize: 10
        },
        {
          backgroundColor: "black",
          borderColor: "white",
          borderSize: 4
        },
        {
          backgroundColor: "black",
          borderColor: "grey",
          borderSize: 2
        },
        {
          backgroundColor: "black",
          borderColor: "grey",
          borderSize: 1
        },
        {
          backgroundColor: "black",
          borderColor: "white",
          borderSize: 0
        },
        {
          backgroundColor: "black",
          borderColor: "white",
          borderSize: 0
        },
        {
          backgroundColor: "black",
          borderColor: "white",
          borderSize: 0
        },
        {
          backgroundColor: "black",
          borderColor: "white",
          borderSize: 0
        }
      ]
    }
  },
  getters: {
    checkLogin: state => {
      return state.loggedIn;
    },
    loginDetails: state => {
      return {
        userID: state.userID,
        username: state.username,
        password: state.password
      };
    },
    skin: state => {
      return state.skin;
    }
  },
  mutations: {
    LOG_IN: (state, data) => {
      state.username = data.username;
      state.password = data.password;
      state.userID = data.userID;
      state.loggedIn = true;
    },
    LOG_OUT: state => {
      state.username = "";
      state.password = "";
    },
    SAVE_SKIN: (state, data) => {
      state.skin = data;
    }
  },
  actions: {
    logOut: context => {
      context.commit("LOG_OUT");
    },
    logIn: (context, data) => {
      context.commit("LOG_IN", {
        username: data.username,
        password: data.password,
        userID: data.userID
      });
    },
    saveSkin: (context, data) => {
      context.commit("SAVE_SKIN", data);
    }
  }
});
