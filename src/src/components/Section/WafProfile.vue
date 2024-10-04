<script setup>
import LabelSelect from "../Compound/LabelSelect.vue"
import LabelText from "../Compound/LabelText.vue"
import { ref, reactive, computed, onMounted, watch } from 'vue'

const inspectionOptions = [
    {value: "16KB", text: "Default (16 KB)", selected: "selected"},
    {value: "32KB", text: "Beyond average (32 KB)"},
    {value: "48KB", text: "Large (48 KB)"},
    {value: "64KB", text: "Extra Large (64 KB)"}
];

const model = defineModel()

const submitProfile = reactive({
    Name: "Emergency-WAF",
    Description: "WAF created for emergency purpose",
    Inspection: "16KB"
})

watch(submitProfile, (newValue) => {
    console.log(newValue)

    model.value = newValue
}, { deep: true })

onMounted(() => {
    model.value = submitProfile
})
</script>

<template>
    <h2>WAF Profile</h2>
    <div class="input-group">
        <LabelText
            :inputId="'wafName'"
            :labelText="'WAF Name:'"

            v-model="submitProfile.Name"
        />
    </div>
    <div class="input-group">
        <LabelText
            :inputId="'wafDescription'"
            :labelText="'Description:'"

            v-model="submitProfile.Description"
        />
    </div>
    <div class="input-group">
        <LabelSelect
            :selectId="'inspection'"
            :selectOptions="inspectionOptions"
            :labelText="'Web request body inspection:'"

            v-model="submitProfile.Inspection"
        />
    </div>
</template>

<style scoped></style>
