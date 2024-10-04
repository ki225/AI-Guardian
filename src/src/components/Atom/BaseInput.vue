<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'

const props = defineProps({
    id: {
        type: String,
        required: true
    },
    type: {
        type: String,
        required: true
    },
    placeholder: {
        type: String,
        required: false
    },
    value: {
        type: String,
        required: false
    },
    Class: {
        type: String,
        required: false
    },
    disabled: {
        type: Boolean,
        default: false
    },
    pattern: {
        type: String,
        required: false
    },
    required: {
        type: Boolean,
        required: false
    }
})

const inputValue = defineModel()
</script>

<template>
    <input 
    :type="type" 
    :id="id" 
    :class="Class" 
    :placeholder="placeholder" 
    :disabled="disabled"
    :pattern="pattern"
    
    v-model="inputValue"
    >
</template>

<style scoped></style>