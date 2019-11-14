<template>
  <div class="mainmapping animated fadeIn" v-bind:class="{ 'graphstarted': mapping}" v-show="switchmainapp">
        <mainheaderapp></mainheaderapp>
        <div class="innerapp">
            <pre v-highlightjs="mapping"><code class="yaml"></code></pre>
        </div>
  </div>
</template>

<script>

import Mainheaderapp from "./mainheader.vue";

export default {
    name: 'Mainmapping',
    components: {
        Mainheaderapp
    },
    data: function () {
        return {
            appstarted: false,
            switchmainapp: false,
            mapping: ''
        }
    },
    mounted: function () {
        this.$root.$on('appstartedEvent', (appstartedstate) => { 
            this.appstarted = appstartedstate;
        });
        this.$root.$on('switchmainappEvent', (switchmainappstate) => { 
            this.switchmainapp = switchmainappstate;
        });
        this.$root.$on('newConfirmedCorrespondance', (confirmed_correspondances) => {
            this.$http.post('/api/' + this.$root.dataset.datasetid + '/correspondances/mapping', confirmed_correspondances).then(response => {
                this.mapping = response.body;
                this.$root.$emit('mappingUpdatedEvent', this.mapping);
            });
        });
    }
}
</script>

<style lang="scss">

</style>
