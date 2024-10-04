<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, inject, onActivated, onDeactivated, onUpdated  } from 'vue'
import SubmissionModal from "../components/Section/SubmissionModal.vue"
import router from '../router/index.js' 
import MarkdownIt from 'markdown-it';

const messagesEndRef = ref(null);
const prompt = ref("")
const messages = ref([
                    { type: 'ai', text: 'Hi !' },
                    { type: 'ai', text: 'I am your WAF manager. ' },
                    { type: 'ai', text: "What do you need?" }
                ])
                
const showPopup = ref(false);
const submittedInfo = ref(null);
const submitting = ref(false);

const submitFailed = inject("submitFailed");
const showButton = inject("showButton");
const submitSuccess = inject("submitSuccess");
const uid = inject("user_id");


const wafConfig = ref("{}")
                
const scrollToBottom = () => {
  messagesEndRef.value?.scrollIntoView({ behavior: 'smooth' });
};

const md = new MarkdownIt();

const renderMarkdown = (content) => {
  return md.render(content);
};

const isJSON = (str) => {
  try {
    JSON.parse(str);
    return true;
  } catch (e) {
    return false;
  }
};

const formatJSON = (jsonString) => {
  try {
    return JSON.stringify(JSON.parse(jsonString), null, 2);
  } catch (e) {
    return jsonString;
  }
};

const entityMap = {
  '&quot;': '"', 
  '&lt;': '<',
  '&gt;': '>',
  '&amp;': '&',
  '&apos;': "'",
  '&cent;': '¢',
  '&pound;': '£',
  '&yen;': '¥',
  '&euro;': '€',
  '&copy;': '©',
  '&reg;': '®'
};

function replaceHTMLEntities(str) {
  return str.replace(/&[#\w]+;/g, match => entityMap[match] || match);
}

const renderMessage = (message) => {
  if (message.type === 'ai') {
    let decodedText = replaceHTMLEntities(message.text);
    if (isJSON(decodedText)) {
      return `<pre><code>${formatJSON(decodedText)}</code></pre>`;
    } else {
      return renderMarkdown(decodedText);
    }
  } else {
    return message.text;
  }
};


const sendPrompt = async () => {
  // send api
  
  const thePrompt = prompt.value.trim()
  if (thePrompt === '') return
  console.log("send")
  messages.value.push({ type: 'user', text: thePrompt })
  
  if (thePrompt === "deploy" && wafConfig.value !== ""){
    messages.value.push({ type: 'ai', text: "Initialize the submit process." })
    await submitConfiguration()
    
    return
  }
  
  prompt.value = ''
  
  try {
        const response = await fetch(import.meta.env.VITE_SEND_PROMPT_URL, {
            method: 'POST',
            body: JSON.stringify({"input": thePrompt})
        });
        
        console.log(response.status)
        
        if (!response.ok) {
            throw new Error(`HTTP error: status: ${response.status}`);
        }
        
        let result = await response.json();
        const jsonData = JSON.parse(result["body"])
        console.log(jsonData)
    
        if (thePrompt === "generate" && jsonData["response"] !== "Information insufficient.") {
          wafConfig.value = jsonData["response"];
        }
    
        // Remove preserveFormatting here
        messages.value.push({ type: 'ai', text: jsonData["response"] })
        
        return
    } catch (error) {
        console.error('Error fetching S3 file contents:', error);
        throw error;
    }
}

const submitConfiguration = async () => {
  submitSuccess.value = false;
  submitFailed.value = false;
  submitting.value = true;
  
  const dataToSend = wafConfig.value
  console.log("set WAF config");
  showPopup.value = true;
  
  let parsed = JSON.parse(dataToSend, null, 2);
  uid.value = parsed.Resource.Resource_Arn;
  console.log(typeof dataToSend)
  try {
        const response = await fetch(import.meta.env.VITE_SUBMIT_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: dataToSend
        });
        
        if (!response.ok) {
            submitting.value = false;
            submitFailed.value = true;
            throw new Error(`HTTP error: status: ${response.status}`);
        }
        
        submittedInfo.value = JSON.parse(dataToSend, null, 2);
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

onMounted(() => {
  scrollToBottom();
});

onUpdated(() => {
  scrollToBottom();
});
</script>

<template>
<div class="section chat-container">
        <div class="chat-messages">
          <div v-for="(message, index) in messages" :key="index" 
                     :class="['message', message.type === 'ai' ? 'ai-message' : 'user-message']">
           <div v-if="message.type === 'ai'" v-html="renderMessage(message)"></div>
           <div v-else>{{ message.text }}</div>
          </div>
          <div ref="messagesEndRef"></div>
        </div>
</div>

<div class="section"> 
        <div class="input-area">
          <input type="text" placeholder="Enter 'generate' to generate submit form. Enter 'deploy' to deploy." v-model="prompt">
          <button class="sendButton"  @click.prevent="sendPrompt">Send</button>
        </div>
</div>

<SubmissionModal
        :show="showPopup"
        :info="submittedInfo" 
        :submitting="submitting"
        :submitFailed="submitFailed"
        @close="popupClose"
        @discard="discardBuilding"
        @peek="goToProgressPage"
      />
</template>

<style scoped>

.chat-container {
  width: 800px;
  max-width: 800px;
  margin-top: 110px;
  overflow: hidden;
  
  border-radius: 15px;
  box-shadow: -5px -2px 10px rgba(0, 0, 0, 0.1);
  background-color: #ffffff;
    
  height: 400px;
  display: flex;
  flex-direction: column;
}

.chat-messages {
  overflow-y: auto;
  padding: 20px;
  gap: 10px;
  
  flex-grow: 1;
  display: flex; 
  flex-direction: column;
}

.message {
  max-width: 70%;
  padding: 10px;
  border-radius: 8px;
  word-wrap: break-word;
  overflow-wrap: break-word;
  hyphens: auto;
  
  align-self: flex-start;
}

.ai-message {
  background-color: #f5f0ff;
  color: black;
  justify-self: start;
}
.ai-message :deep(p) {
  margin: 0 0 10px;
}

.ai-message :deep(ul), .ai-message :deep(ol) {
  margin: 0 0 10px;
  padding-left: 20px;
}

.ai-message :deep(pre) {
  white-space: pre-wrap;
  word-wrap: break-word;
  background-color: #f4f4f4;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
}

.ai-message :deep(code) {
  font-family: monospace;
  font-size: 14px;
  line-height: 1.4;
}

.user-message {
  background-color: #000000;
  align-self: flex-end;
  color: white;
}

.input-area {
  display: flex;
  padding: 10px;
}

.input-area input {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  
  font-size: 14px;
}

.input-area button {
  padding: 10px 20px;
  background-color: #6c6d6e;
  color: white;
  border: none;
  border-radius: 4px;
  margin-left: 10px;
  cursor: pointer;
}
</style>