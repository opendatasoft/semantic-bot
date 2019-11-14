<template>
    <div class="modal" id="aboutModal" tabindex="-1" role="dialog" aria-labelledby="aboutModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            <div class="modal-body">

            <div class="about-section">
            <h3>OpenDataSoft</h3>
            <p>
                OpenDataSoft is an online platform designed to quickly facilitate the publication,
                sharing and re-use of data by business users and stimulate the creation of new applications.
            </p>
            <a href="https://www.opendatasoft.com/" target="_blank">Learn more about OpenDataSoft</a>.

            <p>
                The data network is a data catalog available for everyone. It gathers public and open datasets published by every OpenDataSoft's users in one place.
            </p>
            <a href="https://data.opendatasoft.com/" target="_blank">Explore the data network</a>.
            </div>

            <div class="about-section">
            <h3> Semantic at OpenDataSoft</h3>
            <p>
                <a href="https://en.wikipedia.org/wiki/Semantic_Web" target="_blank">Semantic web</a> technologies are used on OpenDataSoft platform
                to improve data interoperability. It improves data discoverability and data consumption.
                Semantic powered features such as semantic filters or automatic federation of datasets will make OpenDataSoft plateform smarter for it's users.
            </p>
            <p>
                A documentation about <a href="hhttps://help.opendatasoft.com/apis/tpf/" target="_blank">how semantic web is used on OpenDataSoft</a> is available.
            </p>
            </div>

            <div class="about-section">
            <h3> Chatbot</h3>
            <p>
                Integrating data in the semantic web is not an easy task. The goal of this chatbot is to assist you in this process.
            </p>
            <p>
                Chatbot will generate an <a href="http://rml.io/" target="_blank">RML</a>. mapping file that can be uploaded to OpenDataSoft plateform to define how your dataset should be described in semantic formats.
            </p>
            <p>
                This tool is powered with linked data from
                <a href="http://lov.okfn.org/" target="_blank">Linked Open Vocabularies</a>, <a href="https://wiki.dbpedia.org/" target="_blank">DBpedia</a> and <a href="https://www.wikidata.org/" target="_blank">Wikidata</a>.
            </p>
            </div>

            <div class="about-section">
            <h3> Research</h3>
            <p>
                Semantic web at OpenDataSoft is lead by Benjamin Moreau. You can <a href="https://scholar.google.fr/citations?user=TGDeQO0AAAAJ&hl=fr" target="_blank">learn more about his work</a> and feel free to adress him a message!
            </p>
            </div>

            <div class="about-section">
            <h3><i class="fab fa-github"></i> Open source</h3>
            The code source for this bot is open under MIT license on <a href="https://github.com/opendatasoft/ontology-mapping-chatbot" target="_blank">Github</a>.
            </div>


        </div>


    </div>
    </div>
    </div>


</template>

<script>
export default {
    name: 'ModalAbout',
    data: function () {
        return {

        }
    }
}
</script>

<style lang="scss">

</style>
