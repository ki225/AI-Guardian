<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, inject, onActivated, onDeactivated  } from 'vue'
import router from '../router/index.js' 

const display = ref("Waiting for status...");
const uid = inject("user_id")

let intervalId;

const extractAccountNumber = (arn) => {
  const match = arn.match(/arn:aws:[\w-]+:[\w-]*:(\d{12}):/);
  return match ? match[1] : null;
}

const accountNumber = computed(() => extractAccountNumber(uid.value));

const progress = async () => {

    const pollResponse = await fetch(import.meta.env.VITE_GET_PROGRESS_URL, {
      method: 'POST',
      headers: {
                'Content-Type': 'application/json',
            },
      body: JSON.stringify({"user_id": accountNumber.value})
    });

    if (pollResponse.status === 200) {
      let result = await pollResponse.json();
      display.value = result.system_status
    } 
}

const handleBack = () => {
    router.push("/waf-manager");
}

const startInterval = () => {
    if (!intervalId) {
        intervalId = setInterval(progress, 5000)
    }
}

const stopInterval = () => {
    if (intervalId) {
        clearInterval(intervalId)
        intervalId = null
    }
}

onMounted(startInterval)
onActivated(startInterval)

onUnmounted(stopInterval)
onDeactivated(stopInterval)
</script>

<template>
    <div class="section progress-section">
        <div>
            <h1>Resource building progress</h1>
            <p>{{ display }}</p>
        </div>
        <div style="margin-top: 10px; display: flex; justify-content: flex-end;">
            <button style="margin-right: 0px" @click.prevent="handleBack">Go Back</button>
        </div>
    </div>
</template>

<style scoped>
.progress-section {
    margin-top: 110px;
}

</style>