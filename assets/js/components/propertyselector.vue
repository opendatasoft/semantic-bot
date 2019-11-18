<template>
    <div class="propertyselector animated fadeIn">
        <div v-for="{field_name, label, uri, description, domain} in $root.correspondances.properties" class="form-checkbox animated fadeIn">
            <label class="customcheckbox">
                <input class="form-check-input" type="checkbox" :value="field_name" :id="'checkProperty' + field_name" v-model="checked_property_correspondances">
                <span class="checkmark"></span>
                <div class="form-check-label" :for="'checkProperty' + field_name">
                    Field <b>{{label}}</b> is <a :href="uri" target="_blank">{{description}}</a> of <a :href="domain.uri" target="_blank">{{domain.description}}</a>
                </div>
            </label>
        </div>
        <button class="btn btn-secondary" v-on:click="pass_property_correspondances">I don't know</button>
        <button class="btn btn-primary" v-on:click="confirm_property_correspondances">Validate</button>
    </div>
</template>

<script>

    export default {
        name: 'Propertyselector',
        data: function () {
            return {
                checked_property_correspondances: []
            }
        },
        methods: {
            confirm_property_correspondances() {
                this.$root.$emit('confirmedPropertyCorrespondancesEvent', this.checked_property_correspondances);
                this.$root.confirm_property_correspondance(this.checked_property_correspondances);
            },
            pass_property_correspondances() {
                this.$root.$emit('passPropertyCorrespondancesEvent');
                this.$root.pass_property_correspondance();
            }
        }
    }
</script>

<style lang="scss">

</style>