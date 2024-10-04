<script setup>
import BaseLabel from "../Atom/BaseLabel.vue"
import BaseSelect from "../Atom/BaseSelect.vue"

const props = defineProps({
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
  labelText: {
    type: String,
    required: true
  },
  labelClass: {
    type: String,
    required: false
  }
})
const selectedValue = defineModel()
</script>

<template>
  <BaseLabel
    :for="selectId"
    :text="labelText"
    :class="labelClass"
  />
  <BaseSelect
    :id="selectId"
    :options="selectOptions"
    :class="selectClass"
    :disabled="selectDisabled"
    
    v-model="selectedValue"
  />
</template>