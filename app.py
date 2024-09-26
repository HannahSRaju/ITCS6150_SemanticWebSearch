from flask import Flask, request, jsonify, render_template
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)

# SPARQL endpoint
sparql = SPARQLWrapper("https://dbpedia.org/sparql")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_query = request.json.get('query')
    
    # Example SPARQL query using the user input
    query = f"""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?title ?author WHERE {{
        ?book a dbo:Book ;
              rdfs:label ?title ;
              dbo:author ?author .
        FILTER (CONTAINS(LCASE(?title), LCASE("{user_query}")))
    }} LIMIT 10
    """
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    books = [
        {'title': result['title']['value'], 'author': result['author']['value']}
        for result in results["results"]["bindings"]
    ]
    
    return jsonify(books)

@app.route('/relations', methods=['GET'])
def get_relations():
    # Mocked data for relations visualization (nodes and links)
    data = {
        "nodes": [
            {"id": "Document1", "group": 1},
            {"id": "Document2", "group": 1},
            {"id": "Document3", "group": 2}
        ],
        "links": [
            {"source": "Document1", "target": "Document2", "value": 1},
            {"source": "Document2", "target": "Document3", "value": 1}
        ]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
