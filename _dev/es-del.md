To delete all documents of a given type in a given Elasticsearch index:

    curl -XDELETE "http://$HOST/$INDEX/$TYPE/_query?q=*:*"

To delete all ElasticSearch entries in which `field` equals `value`:

    curl -XDELETE "http://$HOST/_all/_query?q=field:value"

In newer versions of Elasticsearch, [the Delete by Query
plugin](https://www.elastic.co/guide/en/elasticsearch/plugins/2.3/plugins-delete-by-query.html)
must be installed first.
