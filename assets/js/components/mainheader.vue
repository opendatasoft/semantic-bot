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
      <div class="copymapping alert alert-primary animated fadeOut delay-2s" v-show="showAlert">
          Mapping has been copied to clipboard
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
                showAlert: false
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
            this.$root.$on('mappingHasBeenCopied', () => {
                this.showAlert = true;
                window.setTimeout(() => {
                    this.showAlert = false;
                }, 3000);
            });
        }
    }
</script>

<style lang="scss">

</style>
