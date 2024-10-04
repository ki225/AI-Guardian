<script setup>
import { ref } from 'vue'

const isVisible = ref(false)

const props = defineProps({
    title:{
        type: String,
        required: true
    }
})

const toggleContent = () => {
    isVisible.value = !isVisible.value
}
</script>

<template>
    <div class="toggle-container">
    <div @click="toggleContent" class="toggle-header">
        <span class="toggle-icon">{{ isVisible ? '▼' : '▶' }}</span>
        {{ title }}
    </div>
    <div v-show="isVisible" class="toggle-content">
        <slot>Oops</slot>
    </div>
  </div>
</template>

<style scoped>
.toggle-header {
    background-color: #fff;
    color: #444;
    cursor: pointer;
    border: none;
    text-align: left;
    outline: none;
    font-size: 15px;
    margin-bottom: 10px;
}
.toggle-content {
  padding: 10px;
}
</style>