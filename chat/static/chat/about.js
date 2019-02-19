document.write(`
<div class="modal fade" id="aboutModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">About</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">

        <div class="about-section">
          <h3><i class="far fa-heart"></i> OpenDataSoft</h3>
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
          <h3><i class="fas fa-share-alt"></i> Semantic at OpenDataSoft</h3>
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
          <h3><i class="far fa-comment-alt"></i> Chatbot</h3>
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
          <h3><i class="fas fa-graduation-cap"></i> Research</h3>
          <p>
            Semantic web at OpenDataSoft is lead by Benjamin Moreau. You can <a href="https://scholar.google.fr/citations?user=TGDeQO0AAAAJ&hl=fr" target="_blank">learn more about his work</a> and feel free to adress him a message!
          </p>
        </div>

        <div class="about-section">
          <h3><i class="fab fa-github"></i> Open source</h3>
          The code source for this bot is open under MIT license on <a href="https://github.com/opendatasoft/ontology-mapping-chatbot" target="_blank">Github</a>.
        </div>

        <div class="about-section">
          <h3><i class="far fa-envelope"></i> Reach out</h3>
        <!--[if lte IE 8]>
          <script charset="utf-8" type="text/javascript" src="//js.hsforms.net/forms/v2-legacy.js"></script>
        <![endif]-->
        <script charset="utf-8" type="text/javascript" src="//js.hsforms.net/forms/v2.js"></script>
        <script>
          hbspt.forms.create({
            portalId: "2041226",
            formId: "ba1cbb2d-9bc9-4979-b46e-54cf97772fcc"
          });
        </script>
      </div>
    </div>

    <div class="modal-footer">
      <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
    </div>
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.3.1/css/all.css" integrity="sha384-mzrmE5qonljUremFsqc01SB46JvROS7bZs3IO2EmfFsd15uHvIt+Y8vEf7N7fWAU" crossorigin="anonymous">
  </div>
</div>
</div>
`);
