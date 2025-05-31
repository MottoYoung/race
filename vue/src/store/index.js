import { createStore } from 'vuex'

export default createStore({
  state: {
  },
  getters: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    imageModule: {
      namespaced: true,
      state: {
        mode: "normal",
        inputText: "",
        selectedResolution: "512x512",
        selectedStyle: "realistic",
        imageUrl: "",
      },
      mutations: {
        setMode(state, mode) {
          state.mode = mode;
        },
        setInputText(state, text) {
          state.inputText = text;
        },
        setSelectedResolution(state, resolution) {
          state.selectedResolution = resolution;
        },
        setSelectedStyle(state, style) {
          state.selectedStyle = style;
        },
        setImageUrl(state, url) {
          state.imageUrl = url;
        },
        resetState(state) {
          state.inputText = "";
          state.imageUrl = "";
        }
      }
    }
  }
})
