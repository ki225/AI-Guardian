<script setup>  
import { computed } from "vue"

const props = defineProps({
  id: {
    type: String,
    required: true
  },
  options: {
    type: Array,
    required: true
  },
  class: {
    type: String,
    required: false
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const selectedValue = defineModel()
</script>

<template>
  <select 
    :id="id" 
    :class="class" 
    :disabled="disabled"

    v-model="selectedValue"
  >
    <option 
      v-for="option in options" 
      :key="option.value" 
      :value="option.value"
      :selected="option.selected"
      :disabled="option.disabled === 'true'"

    >
      {{ option.text }}
    </option>
  </select>
</template>