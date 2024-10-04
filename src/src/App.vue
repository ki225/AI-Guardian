<script setup>
import { ref, provide, onMounted } from 'vue'
import router from './router/index.js'

const isAuthenticated = ref(false)
const uid = ref(null)
const showButton = ref(false)
const submitFailed = ref(true)
const submitSuccess = ref(true)
const openChatBox = ref(false)
const aiMode = ref(true)
const aiMode = ref(true)

const login = () => {
  isAuthenticated.value = true
  localStorage.setItem('isAuthenticated', 'true')
  router.push('/waf-manager/chat')
  router.push('/waf-manager/chat')
}

const logout = () => {
  isAuthenticated.value = false
  aiMode.value = true;
  aiMode.value = true;
  localStorage.setItem('isAuthenticated', 'false')
  router.push('/login')
}

const peek = () => {
  showButton.value = false
  router.push('/build-progress')
}

const switchAiMode = () => {
  aiMode.value = true;
  router.push('/waf-manager/chat')
}

const switchManualMode = () => {
  aiMode.value = false;
  router.push('/waf-manager')
const switchAiMode = () => {
  aiMode.value = true;
  router.push('/waf-manager/chat')
}

const switchManualMode = () => {
  aiMode.value = false;
  router.push('/waf-manager')
}

provide('isAuthenticated', isAuthenticated)

provide('user_id', uid)

provide('login', login)
provide('logout', logout)

provide('showButton', showButton)
provide('submitFailed', submitFailed)
provide('submitSuccess', submitSuccess)

onMounted(() => {
  isAuthenticated.value = localStorage.getItem('isAuthenticated') === 'true'
})

</script>

<template>
  <div id="app">
    <main>
       <header v-if="isAuthenticated">
        <h1 class="nav-title">WAF Manager</h1>
        <nav>
          <button @click="peek" class="logout-button" v-show="showButton && !submitFailed && submitSuccess">Peek building progress</button>
          <button 
          @click="switchAiMode" 
          class="logout-button" 
          :class="{ 'bg-bright': aiMode, 'bg-dark': !aiMode }"
          >
            AI mode
            </button>
          <button 
          @click="switchManualMode"
          class="logout-button"
          :class="{ 'bg-bright': !aiMode, 'bg-dark': aiMode }"
          >
            Manual mode
            </button>
          <button 
          @click="switchAiMode" 
          class="logout-button" 
          :class="{ 'bg-bright': aiMode, 'bg-dark': !aiMode }"
          >
            AI mode
            </button>
          <button 
          @click="switchManualMode"
          class="logout-button"
          :class="{ 'bg-bright': !aiMode, 'bg-dark': aiMode }"
          >
            Manual mode
            </button>
          <button @click="logout" class="logout-button">Logout</button>
        </nav>
      </header>
      <router-view></router-view>
    </main>
    <footer>
    </footer>
  </div>
</template>

<style>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

header {
  position: fixed;
  top: 0;
  right: 0;
  padding: 10px;
  z-index: 1000;
  width: 100%;
  height: 70px;
  background-color: #000;
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid white;
  margin-bottom: 50px;
}
 .bg-bright{
  color: white;
 }
 
 .bg-dark{
   color: transparent;
  -webkit-text-stroke: 0.3px white;
  text-stroke: 0.3px white;
 }
 
 
.nav-title {
  font-family: impact;
  font-size: xx-large;
  color: white;
}

footer {
  position: fixed;
  bottom: 0;
  right: 0;
  padding: 10px;
  z-index: 999;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  margin-bottom: 30px;
  margin-bottom: 30px;
}


.round-button {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 14px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
  box-shadow: -1px -1px 9px rgba(54, 23, 66, 0.2);;
  background-color: #000;
  color: #fff;
  
  margin-top: 15px;
}


.round-button:hover {
  transform: scale(1.05);
}

.round-button.active {
  background-color: #fff;
  color: #000;
  transform: scale(1.1);
}

.logout-button {
  padding: 5px 10px;
  background-color: #000;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;

  font-family: impact;
  font-size: xx-large;
}

main {
  flex-grow: 1;
  box-sizing: border-box;
}

.app-container {
  width: 100%;
  max-width: 800px;
}

body {
  font-family: arial, sans-serif;
  line-height: 1.6;
  margin: 0;
  padding: 0;
  background-color: #fff;
}

h1,
h2,
h3 {
  color: #333;
  margin-bottom: 20px;
  font-family: arial black;
}

h1,
h2 {
  margin-bottom: 30px;
}

h3 {
  margin-top: 30px;

}

input:invalid {
            border-color: red;
        }
input:valid {
            border-color: green;
        }

.section {
  margin-bottom: 20px;
  padding: 20px;
  border-radius: 15px;
  box-shadow: -5px -2px 10px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
  
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.section::-webkit-scrollbar {
  display: none;
  
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.section::-webkit-scrollbar {
  display: none;
}

.buttons {
  margin-bottom: 20px;
  padding: 20px 0px 20px 20px;
  display: flex;
  justify-content: end;
}

.input-group {
  margin-bottom: 15px;
  width: 720px;

}

.input-group>div {
  margin-bottom: 10px;
}

label {
  display: inline-block;
  width: 200px;
  margin-right: 10px;
  vertical-align: middle;
}

input[type="text"],
select {
  width: calc(100% - 320px);
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  vertical-align: middle;
}

.button-container {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  background-color: #6c6d6e;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-right: 15px;
}

.submitButton {
  margin-right: 0px;

}

.selected {
  background-color: #2c3e50;
}

.remove-btn {
  background-color: #dc3545;
  padding: 7.5px 5px 5.5px 5px;
}

.remove-btn:hover {
  background-color: #c82333;
}

.rule-content {
  padding: 10px;
  background-color: #f8f8f8;
  border-radius: 4px;
  margin-bottom: 10px;
}

#regional-resource-type {
  margin-top: 10px;
  margin-left: 210px;
  width: 400px;

}

.form-field-container {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 10px;
  margin-bottom: 10px;
}

.option-button {
  display: inline-flex;
  align-items: center;
  background-color: #3490dc;
  color: white;
  padding: 5px 10px;
  margin: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.option-button::after {
  content: "✕";
  margin-left: 5px;
  font-size: 12px;
}


@media (max-width: 600px) {
  .app-container {
    padding: 10px;
  }

  label,
  input[type="text"],
  select {
    width: 100%;
  }

  input[type="text"],
  select {
    margin-left: 0;
  }

  .button-container {
    flex-direction: column;
  }
}

html {
  scrollbar-width: none;
  -ms-overflow-style: none;
}

html::-webkit-scrollbar {
  display: none;
}

html {
  scrollbar-width: none;
  -ms-overflow-style: none;
}

html::-webkit-scrollbar {
  display: none;
}
</style>