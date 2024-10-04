<script setup>
import LabelSelect from "../Compound/LabelSelect.vue"
import LabelText from "../Compound/LabelText.vue"
import { ref, reactive, computed, onMounted, watch } from 'vue'

const model = defineModel()

const samplingOptions = [
    {value: "true", text: "Record how/why the request being processed (Enable)", selected: "selected"},
    {value: "false", text: "Take actions without recording the details (Disable)"}
];

const submitMonitor = reactive({
    CW_Metric_Name: "Emergency-WAF",
    Option: "true"
})


watch(submitMonitor, (newValue) => {
    console.log(newValue)

  model.value = newValue
}, { deep: true })

onMounted(() => {
    model.value = submitMonitor
})
</script>

<template>
        <h2>Monitor Settings</h2>
        <div class="input-group">
            <LabelText
                :inputId="'cwMetricName'"
                :labelText="'CloudWatch Metric Name:'"

                v-model="submitMonitor.CW_Metric_Name"
            />
        </div>

        <div class="input-group">
            <LabelSelect
                :selectId="'monitorOption'"
                :selectOptions="samplingOptions"
                :labelText="'Request sampling options:'"

                v-model="submitMonitor.Option"
            />
        </div>
</template>

<style scoped></style>
