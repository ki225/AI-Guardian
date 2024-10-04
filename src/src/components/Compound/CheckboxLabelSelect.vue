<script setup>
import BaseInput from "../Atom/BaseInput.vue"
import LabelSelect from "../Compound/LabelSelect.vue"
import { ref } from 'vue'

const inputValue = ref("")
const props = defineProps({
    checkboxId: {
        type: String,
        required: true
    },
    checkboxPlaceholder: {
        type: String,
        required: false
    },
    checkboxClass: {
        type: String,
        required: false
    },
    checkboxValue: {
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
    selectId: {
        type: String,
        required: true
    },
    selectOptions: {
        type: Array,
        required: true
    },
    selectClass: {
        type: String,
        required: false
    },
    selectDisabled: {
        type: Boolean,
        required: false
    },
    modelValue: {
        type: [String, Number],
        required: false
    },
    checkboxDisabled: {
        type: Boolean,
        required: false
    }
})

const selectedValue = defineModel('selectedValue')
const isChecked = defineModel('isChecked')

</script>

<template>
    <BaseInput
        :id="checkboxId"
        :type="'checkbox'"
        :placeholder="checkboxPlaceholder"
        :class="checkboxClass"
        :value="checkboxValue"
        :disabled="checkboxDisabled"

        v-model="isChecked"
    />
    <span></span>
    <LabelSelect
        :labelText="labelText"
        :labelClass="labelClass"
        :selectId="selectId"
        :selectOptions="selectOptions"
        :selectClass="selectClass"
        :selectDisabled="selectDisabled"
        
        v-model="selectedValue"
    />
</template>

<style scoped>
    span {
        margin-left: 30px;
    }
</style>