<script setup>
import AwsResourceType from "../components/Section/AwsResourceType.vue"
import WafProfile from "../components/Section/WafProfile.vue"
import MonitorSetting from "../components/Section/MonitorSetting.vue"
import RuleSetting from "../components/Section/RuleSetting.vue"
import SubmissionModal from "../components/Section/SubmissionModal.vue"

import { ref, computed, watch, reactive, inject } from 'vue'
import router from '../router/index.js' 

const showPopup = ref(false);
const submitting = ref(false);
const submittedInfo = ref(null);
const isVisible = ref(false)
const showHideButton = ref("Show Advanced Options")

const submitFailed = inject("submitFailed");
const submitSuccess = inject("submitSuccess");
const uid = inject("user_id");
const showButton = inject("showButton");

const showAdvanced = () => {
    isVisible.value = !isVisible.value
    if (showHideButton.value === "Show Advanced Options"){
        showHideButton.value = "Hide Advanced Options"
    }
    else{
         showHideButton.value = "Show Advanced Options"
    }
}

const resource = ref(null)
const profile = ref(null)
const monitor = ref(null)
const rule = ref(null)

const submitConfiguration = async () => {
  submitSuccess.value = false;
  submitFailed.value = false;
  submitting.value = true;
  
  const dataToSend = {
    Resource: resource.value,
    Waf: profile.value,
    Monitor_Settings: monitor.value,
    Rules: {
      ...rule.value, 
     Rule_Created: []
    },
    IP: []
  }

  showPopup.value = true;
  uid.value = JSON.parse(JSON.stringify(dataToSend, null, 2))["Resource"]["Resource_Arn"];
  console.log('Submitting form data:', JSON.stringify(dataToSend, null, 2))

  try {
        const response = await fetch(import.meta.env.VITE_SUBMIT_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dataToSend)
        });
        
        console.log(response.status)
        
        if (!response.ok) {
            submitting.value = false;
            submitFailed.value = true;
            throw new Error(`HTTP error: status: ${response.status}`);
        }
        
        submittedInfo.value = JSON.stringify(dataToSend, null, 2);
        submitSuccess.value = true;
        submitting.value = false;
        return await response.json();
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
        throw error; 
    }
}

const popupClose = () => {
  submitting.value = false;
  showPopup.value = false;
  submittedInfo.value = "";
  showButton.value = true;
}

const discardBuilding = () => {
  // Todo: add an api call to discard the build progress
  submitting.value = false;
  showPopup.value = false;
  submittedInfo.value = "";
}

const goToProgressPage = () => {
  submitting.value = false;
  showPopup.value = false;
  submittedInfo.value = "";
  if(!submitFailed.value){
    router.push("/build-progress");
  }
}
</script>

<template>
  <div class="app-container">
    <div class="header-container">
      <h1>WAF Configuration</h1>
    </div>
    <div>
      <form id="wafForm" method="GET">
        <div class="section">
          <AwsResourceType v-model="resource"/>
        </div>

        <div class="section">
          <WafProfile v-model="profile"/>
        </div>

        <div class="section">
          <MonitorSetting v-model="monitor"/>
        </div>

        <div class="section">
          <RuleSetting :isVisible="isVisible" v-model="rule"/>
        </div>

        <div class="buttons">
          <button id="showVeryAdvancedOption" @click.prevent="showAdvanced">{{ showHideButton }}</button>
          <button type="submit" class="submitButton" @click.prevent="submitConfiguration()">Submit WAF Configuration</button>
        </div>

        <div id="formResult"></div>
      </form>
      
      <!--
      <button @click="toggleChat" class="ai-chat-button">
        <span>AI</span>
      </button>
      -->
    
      <SubmissionModal
        :show="showPopup"
        :info="submittedInfo" 
        :submitting="submitting"
        :submitFailed="submitFailed"
        @close="popupClose"
        @discard="discardBuilding"
        @peek="goToProgressPage"
      />
    </div>
  </div>
</template>

<style scoped>
.app-container {
  width: 100%;
  max-width: 800px;
  padding-top: 110px;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h1 {
  margin: 0;
}
</style>
