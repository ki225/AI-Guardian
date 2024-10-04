<script setup>
import BaseLabel from "../Atom/BaseLabel.vue"
import BaseInput from "../Atom/BaseInput.vue"
import { ref, reactive, computed, onMounted, watch } from 'vue'

const inputValue = ref("")
const props = defineProps({
    inputId: {
        type: String,
        required: true
    },
    inputPlaceholder: {
        type: String,
        required: false
    },
    inputClass: {
        type: String,
        required: false
    },
    inputValue: {
        type: String,
        required: false
    },
    labelText: {
        type: String,
        required: true
    },
    labelClass: {
        type: String,
        required: false
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

const input = defineModel()
</script>

<template>
    <BaseLabel
        :for="inputId"
        :text="labelText"
        :class="labelClass"
    />
    <BaseInput
        :id="inputId"
        :type="'text'"
        :placeholder="inputPlaceholder"
        :Class="inputClass"
        :value="inputValue"
        :pattern="pattern"
        :required="required"
        
        v-model="input"
    />
</template>

<style scoped></style>