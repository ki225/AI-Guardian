<script setup>
import LabelSelect from "../Compound/LabelSelect.vue"
import LabeText from "../Compound/LabelText.vue"
import CheckboxLabelSelect from "../Compound/CheckboxLabelSelect.vue"
import ToggleButton from "../Compound/ToggleButton.vue"
import { ref, reactive, computed, onMounted, watch } from 'vue'

/*
const modeOptions = [
    { value: "disable", text: "Disable" },
    { value: "default", text: "Default", selected: "selected" },
    { value: "test", text: "Test" },
    { value: "advanced", text: "Advanced" }
];
*/

const modeOptions = [
    { value: "disable", text: "Disable" },
    { value: "default", text: "Default", selected: "selected" },
    { value: "test", text: "Test" },
];

/*
const actionOptions = [
    { value: "Allow", text: "Allow" },
    { value: "Block", text: "Block", selected: "selected" },
    { value: "Count", text: "Count" },
    { value: "Captcha", text: "CAPTCHA" },
    { value: "Challenge", text: "Challenge" }
];
*/

const actionOptions = [
    { value: "Block", text: "Rule default action" },
    { value: "Count", text: "Just count the matched request for testing. (Non-blocking)" }
];

const defaultAction = [
    { value: "Allow", text: "Allow", selected: "selected" },
    { value: "Block", text: "Block"}
]

const createRulePackage = (name, rules) => ({
    name,
    id: name.split(" ").join(''),
    mode: 'default',
    selectDisabled: true, 
    checkboxDisabled: false, 
    rules: rules.map(rule => ({
        id: rule.id,
        label: rule.label,
        checked: false,
        action: 'Block'
    }))
});

const rulePackages = ref([]);
const isLoading = ref(true);
const props = defineProps({
    isVisible:{
        type: Boolean,
        required: true
    }
})

const valueChange = (val, packageIndex) => {
    const updatedPackages = [...rulePackages.value];
    const packageToUpdate = updatedPackages[packageIndex];
    
    if (val === "disable") {
        packageToUpdate.selectDisabled = true;
        packageToUpdate.checkboxDisabled = true;
    } 
    else if(val === "test"){
        packageToUpdate.selectDisabled = true;
        if (packageToUpdate.checkboxDisabled === true) {
            packageToUpdate.checkboxDisabled = false;
        }
        packageToUpdate.rules.forEach(rule => {
            rule.action = "Count"; 
        });
    }
    else if(val === "default"){
        packageToUpdate.selectDisabled = true;
        if (packageToUpdate.checkboxDisabled === true) {
            packageToUpdate.checkboxDisabled = false;
        }
        packageToUpdate.rules.forEach(rule => {
            rule.action = "Block"; 
        });
    }
    else {
        if (packageToUpdate.checkboxDisabled === true) {
            packageToUpdate.checkboxDisabled = false;
        }
        packageToUpdate.selectDisabled = false;
    }

    packageToUpdate.mode = val;
    rulePackages.value = updatedPackages;

    submitRule.Rule_Package[packageToUpdate.name].Mode = val;
    submitRule.Rule_Package[packageToUpdate.name].Set.forEach((rule, index) => {
        rule.Action = packageToUpdate.rules[index].action;
        rule.Chosen = packageToUpdate.rules[index].checked;
    });
}

// return json file for creating rule package
const get_rule_packages = async () => {
    const getObjectUrl = import.meta.env.VITE_GET_OBJECT_URL
    try {
        const response = await fetch(getObjectUrl,{
          method: 'GET', 
          headers: {
            'Content-Type': 'application/json'
          },
          mode: 'cors'
        });
        if (!response.ok) {
            throw new Error(`HTTP error with status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Error fetching S3 file contents:', error);
        throw error;
    }
}

onMounted(async () => {
    try {
        let _priority = 0;
        isLoading.value = true;
        const data = await get_rule_packages();
        rulePackages.value = data.map(pkg => {

            const packageName = pkg["key"].split('/')[1].split('.')[0];
            const parsedRules = JSON.parse(pkg["content"]);
            
            submitRule.Rule_Package[packageName] = {
                Mode: 'default',
                Set: parsedRules.map(rule => {
                return {
                    Rule_Id: rule.Rule_Id,
                    Chosen: true,
                    Action: "Block",
                    Priority: _priority++
                }
                })
            };
            
            return createRulePackage(
                packageName, 
                parsedRules.map(rule => ({
                    id: rule.Rule_Id,
                    label: rule.Name
                }))
            );
        });
        isLoading.value = false;
    } catch (error) {
        console.error('Failed to load rule packages:', error);
        isLoading.value = false;
    }
    
    model.value = submitRule
});

const model = defineModel()

const submitRule = reactive({
    "Rule_Package": {}
})

watch(submitRule, (newVal) => {
    model.value = newVal
}, { deep: true })

</script>

<template>
        <h2>Rules</h2>
        <h3>Rule Packages</h3>
        <div v-if="isLoading">Rule packages loading...</div>
        <div v-for="(aPackage, index) in rulePackages" :key="aPackage.name" v-else>
            <div class="input-group">
                <LabelSelect 
                    :selectId="`${aPackage.id}`"
                    :selectOptions="modeOptions"
                    :labelText="`${aPackage.name}:`"
                    :modelValue="aPackage.mode"
                    @update:modelValue="(val) => valueChange(val, index)"
                />
            </div>

            <ToggleButton :title="'Click to inspect rules'">
                <div class="rule-content" :id="`${aPackage.name.toLowerCase()}r`">
                    <div v-for="(rule, i) in aPackage.rules" :key="rule.id">
                        <CheckboxLabelSelect
                            :checkboxId="rule.id"
                            :checkboxClass="`${aPackage.name.toLowerCase()}-check`"
                            :labelText="rule.label"
                            :selectId="`${rule.id}-select`"
                            :selectOptions="actionOptions"
                            :selectClass="`${aPackage.name.toLowerCase()}-action action`"
                            :selectDisabled="aPackage.selectDisabled"
                            :checkboxDisabled="aPackage.checkboxDisabled"
                            
                            v-model:selectedValue="submitRule.Rule_Package[Object.keys(submitRule.Rule_Package)[index]].Set[i].Action"
                            v-model:isChecked="submitRule.Rule_Package[Object.keys(submitRule.Rule_Package)[index]].Set[i].Chosen"
                        />
                    </div>
                </div>
            </ToggleButton>
        </div>
        
        <div :hidden="!isVisible">
        <h3>Rule Priority</h3>
        <div v-if="isLoading">Rule packages loading...</div>
        <div v-for="(aPackage, index) in rulePackages" :key="aPackage.name" v-else>
            <div v-for="(rule, i) in aPackage.rules" :key="rule.id">
                <LabeText 
                 :inputId="`${rule.label}-priority`"
                 :labelText="rule.label"

                 v-model="submitRule.Rule_Package[Object.keys(submitRule.Rule_Package)[index]].Set[i].Priority"
                />
            </div>
        </div>
                
        <!-- 
        <h3>If requests that don't match any rules</h3>
            <LabelSelect 
                    :selectId="reqDontMatchRule"
                    :selectOptions="defaultAction"
                    :labelText="Action"
            />
            todo -->
        </div>

</template>

<style scoped></style>
