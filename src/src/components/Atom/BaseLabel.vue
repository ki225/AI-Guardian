<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'

const props = defineProps({
    for: {
        type: String,
        required: true
    },
    text: {
        type: String,
        required: true
    },
    class: {
        type: String,
        required: false
    }
})
</script>

<template>
    <label :for="for" :class="class" :value="text">{{ text }}</label>
</template>

<style scoped></style>