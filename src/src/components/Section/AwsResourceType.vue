<script setup>
import BaseSelect from "../Atom/BaseSelect.vue"
import LabelSelect from "../Compound/LabelSelect.vue"
import LabelText from "../Compound/LabelText.vue"

import { ref, reactive, computed, onMounted, watch } from 'vue'

const resourceOptions = [
    {value: "alb", text: "Application Load Balancer", selected: "selected"},
    {value: "apigateway", text: "Amazon API Gateway REST API"},
    {value: "apprunner", text: "Amazon App Runner service"},
    {value: "appsync", text: "AWS AppSync GraphQL API"},
    {value: "cognito", text: "Amazon Cognito user pool"},
    {value: "verifiedaccess", text: "AWS Verified Access"},
];

const awsRegions = [
    {value: "global", text: "Global", disabled: "true"},
    {value: "us-east-2", text: "US East (Ohio) - us-east-2"},
    {value: "us-east-1", text: "US East (N. Virginia) - us-east-1", selected: "selected"},
    {value: "us-west-1", text: "US West (N. California) - us-west-1"},
    {value: "us-west-2", text: "US West (Oregon) - us-west-2"},
    {value: "af-south-1", text: "Africa (Cape Town) - af-south-1"},
    {value: "ap-east-1", text: "Asia Pacific (Hong Kong) - ap-east-1"},
    {value: "ap-south-2", text: "Asia Pacific (Hyderabad) - ap-south-2"},
    {value: "ap-southeast-3", text: "Asia Pacific (Jakarta) - ap-southeast-3"},
    {value: "ap-southeast-4", text: "Asia Pacific (Melbourne) - ap-southeast-4"},
    {value: "ap-south-1", text: "Asia Pacific (Mumbai) - ap-south-1"},
    {value: "ap-northeast-3", text: "Asia Pacific (Osaka) - ap-northeast-3"},
    {value: "ap-northeast-2", text: "Asia Pacific (Seoul) - ap-northeast-2"},
    {value: "ap-southeast-1", text: "Asia Pacific (Singapore) - ap-southeast-1"},
    {value: "ap-southeast-2", text: "Asia Pacific (Sydney) - ap-southeast-2"},
    {value: "ap-northeast-1", text: "Asia Pacific (Tokyo) - ap-northeast-1"},
    {value: "ca-central-1", text: "Canada (Central) - ca-central-1"},
    {value: "eu-central-1", text: "Europe (Frankfurt) - eu-central-1"},
    {value: "eu-west-1", text: "Europe (Ireland) - eu-west-1"},
    {value: "eu-west-2", text: "Europe (London) - eu-west-2"},
    {value: "eu-south-1", text: "Europe (Milan) - eu-south-1"},
    {value: "eu-west-3", text: "Europe (Paris) - eu-west-3"},
    {value: "eu-south-2", text: "Europe (Spain) - eu-south-2"},
    {value: "eu-north-1", text: "Europe (Stockholm) - eu-north-1"},
    {value: "eu-central-2", text: "Europe (Zurich) - eu-central-2"},
    {value: "il-central-1", text: "Israel (Tel Aviv) - il-central-1"},
    {value: "me-south-1", text: "Middle East (Bahrain) - me-south-1"},
    {value: "me-central-1", text: "Middle East (UAE) - me-central-1"},
    {value: "sa-east-1", text: "South America (São Paulo) - sa-east-1"},
    {value: "us-gov-east-1", text: "AWS GovCloud (US-East) - us-gov-east-1"},
    {value: "us-gov-west-1", text: "AWS GovCloud (US-West) - us-gov-west-1"}
];

const isVisible = ref(false)
const selectedResourceType = ref("alb")
const selectedRegion = ref("global") 
const inputVal = ref("")
const activeButton = ref('global-resource')

const visible = () => {
    isVisible.value = true
    submitResource.Region = "us-east-1"
    submitResource.Type = "alb"
    activeButton.value = 'region-resource' 
}

const invisible = () => {
    isVisible.value = false
    submitResource.Region = "global"
    submitResource.Type = "cloudfront"
    activeButton.value = 'global-resource'
}

const model = defineModel()

const submitResource = reactive({
    Type: "cloudfront",
    Region: "global",
    Resource_Arn: "",
    Resource_Id: "",
    Resource_Name: ""
})

watch(submitResource, (newVal) => {
    model.value = newVal
}, { deep: true })

onMounted(() => {
    model.value = submitResource
})
</script>

<template>
    <h2>Resource</h2>
            <div class="input-group">
                <label>Type:</label>
                <button 
                    name="regional resource" 
                    class="resource-type" 
                    :class="{ 'active': activeButton === 'region-resource' }"
                    id="region-resource" 
                    @click.prevent="visible"
                >
                    Regional resources
                </button>
                <button 
                    name="global resource" 
                    class="resource-type" 
                    :class="{ 'active': activeButton === 'global-resource' }"
                    id="global-resource" 
                    @click.prevent="invisible"
                >
                    CloudFront distributions WAF(global)
                </button>
                <div class="input-group" v-show="isVisible">
                    <BaseSelect
                        :id="'regional-resource-type'"
                        :options="resourceOptions"
                        :class="'input-group'"

                        v-model="submitResource.Type"
                    />
                </div>
            </div>

            <div class="input-group" id="chose-region">
                <LabelSelect
                    :selectId="'region'"
                    :selectOptions="awsRegions"
                    :labelText="'Region:'"
                    :selectDisabled="!isVisible"

                    v-model="submitResource.Region"
                />
            </div>

            <div class="input-group">
                <LabelText
                    :inputId="'resourceArn'"
                    :labelText="'Resource ARN:'"
                    
                    v-model="submitResource.Resource_Arn"
                />
            </div>
</template>

<style scoped>
.resource-type {
    padding: 10px 15px;
    margin-right: 10px;
    border: 1px solid #ccc;
    background-color: #6c6d6e;
    cursor: pointer;
    transition: all 0.3s ease;
}

.resource-type:hover, .resource-type:focus {
    background-color: #6c6d6e;
}

.resource-type.active {
    background-color: #292727;
    color: white;
}
</style>
