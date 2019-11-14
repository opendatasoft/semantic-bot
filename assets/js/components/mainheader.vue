<template>
  <div class="mainheader">
    <div class="switch">
        <ul>
            <li class="viewschema" v-on:click="switchSchema">
                <span>Mapping</span>
            </li>
            <li class="viewmapping" v-on:click="switchMapping">
                <span>Schema</span>
            </li>
        </ul>
    </div>
    <div>
        <getmappingbtn></getmappingbtn>
    </div>
  </div>
</template>

<script>
    import Getmappingbtn from "./getmappingbtn.vue";

    export default {
        name: 'Mainheader',
        components: {
            Getmappingbtn
        },
        data: function () {
            return {
                switchmainapp: false,
            }
        },
        methods: {
            switchSchema: function (event) {
                this.$root.$emit('switchmainappEvent', true);
            },
            switchMapping: function (event) {
                this.$root.$emit('switchmainappEvent', false);
            }
        },
        mounted: function () {
            this.$root.$on('switchmainappEvent', (switchmainappstate) => {
                this.switchmainapp = switchmainappstate;
            });
        }
    }
</script>

<style lang="scss">

</style>
