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
          More infos on OpenDataSoft <a href="https://www.opendatasoft.com/">here</a>.
        <br>
          Discover OpenDataSoft's data network <a href="https://data.opendatasoft.com/">here</a>.
        </p>
        <h3> Semantic </h3>
        <p>
          <a href="https://en.wikipedia.org/wiki/Semantic_Web">Semantic web</a> is a web where data is described
          using common representation <a href="https://en.wikipedia.org/wiki/Resource_Description_Framework">(RDF)</a> and vocabularies.
          It allows data to be reused accross application, enterprise, city, country, ...
        </p>
        <h3> Chatbot </h3>
        <p>
          Integrating data in the semantic web is not an easy task.
          The goal of this chatbot is to assist you in this process.
        <br>
          This tool is powered with linked data from <a href="http://lov.okfn.org/">Linked Open Vocabularies</a>
          and <a href="https://wiki.dbpedia.org/">DBpedia</a>.
        <br>
          A documentation about how semantic web is used on OpenDataSoft platform is
          available <a href="https://docs.opendatasoft.com/api/explore/tpf.html">here</a>.
        </p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
      </div>
    </div>
  </div>
</div>
`);
