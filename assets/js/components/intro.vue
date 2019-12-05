<template>
<div  id="inersidepanel" class="intro animated" :class="{ 'fadeIn delay-05s': !fadeoutpanel, 'fadeOut': fadeoutpanel}" v-if="!appstarted">
  <h1>{{ title }}</h1>
  <ul>
    <li>
      <span>1.</span>Ask <a href="mailto:support@opendatasoft.com?Subject=semantic metadata">support</a> to enable metadata templates on your domain
    </li>
    <li>
      <span>2.</span>Go to your backoffice in the configuration section
    </li>
    <li>
      <span>3.</span>Go to “Other metadata” and click on “Semantic Metadata” 
    </li>
    <li>
      <span>4.</span>Check “Activate this metadata template on the portal”
    </li>
    <li>
      <span>5.</span>Click the save button
    </li>
    <li>
    <small>
      <i>
        Submitted data are subject to <a href="https://legal.opendatasoft.com/en_FR/privacy-policy.html">Opendatasoft’s Privacy Policy</a>
      </i>
    </small>
    </li>
  </ul>
  <button class="btn btn-primary" v-on:click="startApp">I understand</button>
  
</div>

</template>

<script>
export default {
  name: 'Intro',
  data: function () {
    return {
      title: 'If it’s the first time, please activate semantic metadata on your domain',
      appstarted: false,
      fadeoutpanel: false
}
  },
  methods: {
    startApp: function (event) {
      this.fadeoutpanel = true
      setTimeout(()=>{
        this.$root.$emit('appstartedEvent', true);
      },1000);
      
    }
  },
  mounted: function () { 
      this.$root.$on('appstartedEvent', (appstartedstate) => { 
        this.appstarted = appstartedstate;
      })
  }
}
</script>

<style lang="scss">

</style>
