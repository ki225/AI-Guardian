<script setup>
import { ref, inject } from 'vue'

const buttonDisable = ref(false)
const buttonText = ref("Submit");
const login = inject('login');

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const handleSubmit = async () => {
  buttonText.value = 'Processing...';
  buttonDisable.value = true;
  try {
    await sleep(1000);
    login();
  } catch (error) {
    console.error('An error occurred:', error);
  } finally {
    buttonText.value = 'Submit';
    buttonDisable.value = false;
  }
}
</script>

<template>
  <form>
    <div id="login-info-container">
      <div id="login-info">
        <div class="credential-container">
          <h1>Login</h1>
          <div class="credentials">
            <label for="account">Account</label>
            <input type="text" id="account">
          </div>
          <div class="credentials">
            <label for="password">Password</label>
            <input type="password" id="password">
          </div>
          <button type="submit" id="login-submit" :disabled="buttonDisable" @click.prevent="handleSubmit">{{ buttonText }}</button>
        </div>
      </div>
    </div>
  </form>
</template>

<style scoped>
  
#login-info-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

#login-info {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 5px 5px 10px 0px rgba(0, 0, 0, 0.3);
  background-color: #ffffff;
}

h1 {
  margin-bottom: 15px;
}

.credential-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px;
  border-radius: 8px;
}

.credentials {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
}

input[type="text"],
input[type="password"]{
  height: 25px;
  border-radius: 5px;
  border: 2px solid #dad8d8;
  width: 230px;
}

#login-submit {
  margin-top: 10px;
  align-self: flex-end;
  background-color: #565758; 
  color: white;
  border: none;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, opacity 0.3s;
}

#login-submit:hover {
  background-color: #4b4a4a;
}

#login-submit:disabled {
  background-color: #cccccc;
  color: #666666;
  cursor: not-allowed;
  opacity: 0.6;
}

label {
  margin-bottom: 8px;
  font-family: Arial, Helvetica, sans-serif;
}
</style>
