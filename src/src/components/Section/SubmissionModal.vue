<script setup>
  import { inject } from "vue"
  
  const submitFailed = inject("submitFailed");

      defineProps({
        show: {
            type: Boolean,
            required: true
        },
        info: {
            type: String,
            required: true
        },
        submitting: {
            type: Boolean,
            required: true
        },
        submitFailed: {
          type: Boolean,
          required: true
        }
    });
    
    const emit = defineEmits(["discard", "peek", "close"])
    
</script>

<template>
  <div v-if="show" class="popup">
    <div class="popup-content">
      <div class="popup-header">
        <h2 v-if="submitting">Submitting...</h2>
        <h2 v-else-if="!submitFailed">Submitted Success</h2>
        <h2 v-else>Submission Failed</h2>
      </div>
      <div class="scrollable-content">
        <div v-if="!submitting && !submitFailed">
          <pre>The following configuration has been submitted:</pre>
          <pre>{{ info }}</pre>
        </div>
      </div>
      <div class="button-container">
        <button @click.prevent="$emit('discard')" v-show="submitting || !submitFailed">Discard</button>
        <button @click.prevent="$emit('peek')" v-show="!submitFailed && !submitting">Peek building progress</button>
        <button @click.prevent="$emit('close')">Close</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.popup {
  position: fixed;
  top: 70px; /* Adjust this value to match your header height */
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: flex-start; /* Changed from center to flex-start */
  padding: 20px;
  box-sizing: border-box;
  overflow-y: auto; /* Allow scrolling if popup is taller than available space */
}

.popup-content {
  background-color: white;
  width: 90%;
  max-width: 600px;
  max-height: calc(100vh - 100px); /* Subtract header height and some padding */
  display: flex;
  flex-direction: column;
  margin-top: 20px; /* Add some top margin */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border-radius: 15px;
}

.popup-header {
  padding: 15px 20px;
  background-color: #fff;
  border-radius: 15px;

}

.popup-header h2 {
  margin: 0;
  text-align: center;
}

.scrollable-content {
  flex-grow: 1;
  overflow-y: auto;
  text-wrap: wrap;
  padding: 10px;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 15px 20px;
  background-color: #fff;
  border-radius: 15px;

}

button {
  padding: 8px 16px;
  background-color: #6c6d6e;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #565758;
}

pre {
  white-space: pre-wrap;       /* CSS 3 */
  white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
  white-space: -pre-wrap;      /* Opera 4-6 */
  white-space: -o-pre-wrap;    /* Opera 7 */
  word-wrap: break-word;       /* Internet Explorer 5.5+ */
  overflow-wrap: break-word;
  font-family: monospace;
  font-size: 14px;
  line-height: 1.5;
  margin: 0;
  padding: 0;
}
</style>