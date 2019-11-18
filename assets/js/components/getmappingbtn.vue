<template>
    <button class="btn btn-primary" v-bind:disabled="!is_button_activated" v-clipboard:copy="mapping" v-on:click="mappingHasBeenCopied">
        Get mapping
    </button>
</template>

<script>
  export default {
      name: 'GetMappingBtn',
      data: function () {
          return {
              is_button_activated: false,
              mapping: ''
          }
      },
      methods: {
          mappingHasBeenCopied() {
              this.$root.$emit('mappingHasBeenCopied');
          }
      },
      mounted: function () {
          this.$root.$on('mappingUpdatedEvent', (new_mapping) => {
              this.mapping = new_mapping;
              if (this.mapping.length > 0) {
                  this.is_button_activated = true;
              }
          });
      }
  }
</script>

<style lang="scss">

</style>