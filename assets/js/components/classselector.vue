<template>
  <div class="classselector animated fadeIn">
      <div v-for="{field_name, label, uri, description} in $root.correspondances.classes" class="form-checkbox animated fadeIn">
          <label class="customcheckbox">
            <input class="form-check-input" type="checkbox" :value="field_name" :id="'checkClass' + field_name" v-model="checked_class_correspondances">
            <span class="checkmark"></span>
            <div class="form-check-label" :for="'checkClass' + field_name">
                Field <b>{{label}}</b> contains <a :href="uri" target="_blank">{{ description }}</a>
            </div>
          </label>

      </div>
      <button class="btn btn-secondary" v-on:click="pass_class_correspondances">I don't know</button>
      <button class="btn btn-primary" v-on:click="confirm_class_correspondances">Validate</button>
  </div>
</template>

<script>

  export default {
      name: 'Classselector',
      data: function () {
          return {
              checked_class_correspondances: []
          }
      },
      methods: {
          confirm_class_correspondances() {
              this.$root.$emit('confirmedClassCorrespondancesEvent', this.checked_class_correspondances);
              this.$root.$emit('isWaiting', true);
              this.$root.confirm_class_correspondance(this.checked_class_correspondances);
          },
          pass_class_correspondances() {
              this.$root.$emit('passClassCorrespondancesEvent');
              this.$root.$emit('isWaiting', true);
              this.$root.pass_class_correspondance();
          }
      }
  }
</script>

<style lang="scss">

</style>