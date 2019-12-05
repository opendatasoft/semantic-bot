<template>
    <header class="animated fadeIn delay-04s shadow" :class="{ 'shadow': shadow}">
        <div class="logo">
            <a href="#">
                <img src="static/img/logo.svg">
            </a>
        </div>
        <div class="nav">
            <ul>
                <li>
                    <a href="#" data-toggle="modal" data-target="#aboutModal">
                        About
                    </a>
                </li>
                <li>
                    <a href="mailto:support@opendatasoft.com?Subject=SemanticBot">
                        Support
                    </a>
                </li>
                <li>
                    <a href="https://legal.opendatasoft.com/en_FR/terms-of-use.html" target="_blank">
                        Legal
                    </a>
                </li>
            </ul>
           

        </div>

    </header>
</template>

<script>
export default {
    name: 'Hedaer',
    data: function () {
        return { 
            heightsidepanel:0,
            heightintropanel:0,
            shadow: 0
        }
    },
    methods: {
        onResize(event) {
            this.heightsidepanel = document.getElementById("sidepanel").offsetHeight - 300;
            this.heightintropanel = document.getElementById("inersidepanel").offsetHeight;
            if (this.heightsidepanel < this.heightintropanel){
                this.shadow = 1
            } else {
                this.shadow = 0
            }
        }
    },
    mounted() {
        this.heightsidepanel = document.getElementById("sidepanel").offsetHeight;
        this.heightintropanel = document.getElementById("inersidepanel").offsetHeight;
        window.addEventListener('resize', this.onResize)
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.onResize)
    }
}
</script>

<style lang="scss">

</style>