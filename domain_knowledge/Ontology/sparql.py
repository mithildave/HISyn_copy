import sys
import urllib
import rdflib
from rdflib import URIRef
from rdflib.namespace import RDF
from rdflib.util import get_tree
import re
from HISyn_copy.tools.root_directory import root_dir
import HISyn_copy.tools.Log as log
concpt = ["memLocal","memAtomic","wgSize","coalesced"]

def loadOntology():

    g = rdflib.Graph()
    g.parse('/Users/mithildave/Documents/allInOne.ttl', format='turtle')

    query = """
    
    PREFIX hpc:<https://github.com/HPC-FAIR/HPC-Ontology#>
    SELECT ?model_name
     WHERE { 
            ?model_id rdf:type hpc:AIModel .
            ?model_id hpc:targetMachine <http://example.org/cluster/lassen> .
            ?model_id hpc:name ?model_name 
            
            
        }"""

    qres = g.query(query)
    Results = list(qres)
    print (Results)



def exampleOntology(file_name):
    g = rdflib.Graph()
    g.parse('/Users/mithildave/Documents/allInOne.ttl', format='turtle')

    query = """

    PREFIX hpc:<https://github.com/HPC-FAIR/HPC-Ontology#>
    SELECT ?column
     WHERE { 

            ?dataset rdf:type hpc:Dataset.
            ?dataset hpc:name \"""" + file_name + """\".
            ?dataset hpc:hasConceptTags ?column
        }"""

    qres = g.query(query)
    for row in qres:
        d = str(row.asdict()['column'].toPython())
        print (d)
        d= d.strip('"')

    return d.split(',')


def NER():
    import spacy

    nlp = spacy.load('en_core_web_sm')

    sentence = "Memory performance"

    doc = nlp(sentence)

    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)

def getConcept():
    #ToDo SPARQL Query
    return ['memory','cpu','operatingSystem','performance']

def SPARQL_concept(cnpt):
    g = rdflib.Graph()
    g.parse('hpc-ontology-concept.ttl', format='turtle')

    query = """SELECT DISTINCT ?entity
        WHERE {
           
            ?entity rdfs:subClassOf ?concept.  
            
            ?concept rdfs:subClassOf hpc:Concept 

            FILTER( STRSTARTS (STR(?concept),str(hpc:""" + cnpt + """)) )

        }"""

    qres = g.query(query)
    Results = []
    for row in qres:
        Results.append(str(row).rsplit('#')[-1].rstrip(',)\''))
    print(*Results, sep='\n')


def SPARQL_concept_prop(cnpt):
    g = rdflib.Graph()
    g.parse('/Users/mithildave/Documents/hpc-ontology-concept.ttl', format='turtle')

    query = """SELECT DISTINCT ?entity
        WHERE {
            ?entity rdfs:subPropertyOf hpc:"""+ cnpt + """.
        }"""

    qres = g.query(query)
    Results = []
    for row in qres:
        Results.append(str(row).rsplit('#')[-1].rstrip(',)\''))
    print(*Results, sep='\n')
    return Results

def printSeparation():
    for i in range(0,50):
        print ('#', end ="")
    print("\n")

def queryConcept(text):
    log.log("Replacing hpc concept in the query: ")

    file_name = "cgo17-nvidia.csv"
    concepts = getConcept()

    concept_regex = r'(\{[^\}]+\})'
    match = re.search(concept_regex, text)
    if(match == None):
        return text
    match = match.group(0).rstrip().lstrip()
    for c in concepts:
        if c in match:
            cnpt = c
            break
    
    print ("\n\n            filename: "+file_name+"")
    print("            concept: " + cnpt + "\n\n")
    printSeparation()
    print ("                hpc:hasConceptTag                 ")

    columns = exampleOntology(file_name)
    printSeparation()

    print("          Matched Columns of the Dataset                 ")

    concept = SPARQL_concept_prop(cnpt)

    result = ""
    i =0 
    for each in columns:
        if each in concpt:
            print ("                "+each+"              ")
            if (i == 0):
                result += each
                i += 1
            else:
                result += "," +each

    concept_regex = r'(\{[^\}]+\})'
    match = re.search(concept_regex, text)
    text = text.replace(match.group(), '"'+result + '"', 1)

    printSeparation()
    return text

    


