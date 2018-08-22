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
        <h3> OpenDataSoft </h3>
        <p>
          OpenDataSoft is an online platform designed to quickly facilitate the publication,
          sharing and re-use of data by business users and stimulate the creation of new applications.
        <br>
          <a href="https://www.opendatasoft.com/">www.opendatasoft.com</a>.
        <br>
        </p>
        <p>
          Data network is a dataset library accesible for everyone. It gathers public datasets from all users in one place.
        <br>
          <a href="https://data.opendatasoft.com/">data.opendatasoft.com</a>.
        </p>
        <h3> Semantic </h3>
        <p>
          <a href="https://en.wikipedia.org/wiki/Semantic_Web">Semantic web</a> technologies are used on OpenDataSoft platform
          to improve data interoperability. It facilitates data discoverability and data consumption.
          Semantic powered features such as semantic filters or automatic federation of datasets will make OpenDataSoft plateform smarter.
        </p>
        <p>
          A documentation about how semantic web is used on OpenDataSoft platform is
          available at <a href="hhttps://help.opendatasoft.com/apis/tpf/">help.opendatasoft.com/apis/tpf</a>.
        </p>
        <h3> Chatbot </h3>
        <p>
          Integrating data in the semantic web is not an easy task.
          The goal of this chatbot is to assist you in this process.
        <br>
          Chatbot will generate an <a href="http://rml.io/">RML</a>. mapping file that can be uploaded to OpenDataSoft plateform to define how your dataset should be described in semantic formats.
        <br>
          This tool is powered with linked data from
          <a href="http://lov.okfn.org/">Linked Open Vocabularies</a>, <a href="https://wiki.dbpedia.org/">DBpedia</a> and <a href="https://www.wikidata.org/">Wikidata</a>.
        </p>
        <h3> Contact </h3>
        <a href="TO DO">Hubspot</a>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>
`);
