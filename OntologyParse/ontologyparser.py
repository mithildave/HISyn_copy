#!/user/bin/env python3 -tt
"""
Module documentation.
"""

# Imports
import sys
import urllib
import rdflib
from rdflib import URIRef
from rdflib.namespace import RDF
from rdflib.util import get_tree
#from lxml import ET


def xml_parse(proc, file1):
    import xml.etree.ElementTree as ET
    #from lxml import etree as ET
    from re import search

    tree = ET.parse('hpc-ontology.xml')
    root = tree.getroot()

    namespaces = {'owl': 'http://www.w3.org/2002/07/owl#', 'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}  # add more as needed
    Proc = proc
    Out = "hasOutput"
    In = "hasInput"
    Prereq = "hasPrereq"
    prereq =[]
    input = []
    output = []
    for Class in root.findall('owl:Class', namespaces):
        attr = str(Class.attrib)
        if search(Proc, attr):
            #print ("Yes")
            #print (Class.findall('.//owl:Restriction', namespaces))
            for Res in Class.findall('.//owl:Restriction', namespaces):
                for tag1 in Res.iter('{http://www.w3.org/2002/07/owl#}onProperty'):
                    attr = str(tag1.attrib)
                    if search(Out, attr):

                        items = Res.iter('{http://www.w3.org/2002/07/owl#}someValuesFrom')
                        for item in items:
                            attr = str(item.attrib)
                            split_array = attr.split('#')
                            file = (split_array[-1])[:-2]
                            if "Data" != file:
                                output.append(file)
                                print("Output ------>  "+file)

                    if search(In, attr):

                        items = Res.iter('{http://www.w3.org/2002/07/owl#}someValuesFrom')
                        for item in items:
                            attr = str(item.attrib)
                            split_array = attr.split('#')
                            file = (split_array[-1])[:-2]
                            if "Data" != file:
                                input.append(file)
                                print("Input ------>  " + file)

                    if search(Prereq, attr):

                        items = Res.iter('{http://www.w3.org/2002/07/owl#}someValuesFrom')
                        for item in items:
                            attr = str(item.attrib)
                            split_array = attr.split('#')
                            file = (split_array[-1])[:-2]
                            prereq.append(file)
                            print("Prereq ------>  " + file)
    file1.write("return:\t")
    for each in output:
        file1.write(each)
        if(output.index(each)!=len(output)-1):
            file1.write(", ")

    file1.write("\n")

    file1.write("argument:\t")
    argm = input + prereq
    for each in argm:
        file1.write(each)
        if(argm.index(each)!=len(argm)-1):
            file1.write(", ")
    file1.write("\n")

def rdf_parser():
    # create a Graph
    g = rdflib.Graph()

    # parse in an RDF file
    result = g.parse('hpc-ontology.ttl', format='turtle')

    # loop through each triple in the graph (subj, pred, obj)
    for subj, pred, obj in g:
        # check if there is at least one triple in the Graph

        if (subj, pred, obj) not in g:
            raise Exception("It better be!")

    # print the number of "triples" in the Graph
    #print("graph has {} statements.".format(len(g)))

    # print out the entire Graph in the RDF Turtle format
    #print(g.serialize(format="turtle").decode("utf-8"))
def fix(s):
    i = s.rindex('/')
    return s[:i]+urllib.quote(s[i:])

def rdf_general_match(file1):
    from rdflib import URIRef
    from rdflib.namespace import RDF, RDFS, OWL
    g = rdflib.Graph()

    result = g.parse('hpc-ontology.ttl', format='turtle' )

    hpc = URIRef("https://github.com/HPC-FAIR/HPC-Ontology#")
    hascommand = URIRef("https://github.com/HPC-FAIR/HPC-Ontology#hasCommand")
    proc = URIRef("https://github.com/HPC-FAIR/HPC-Ontology#Processes")

    for s,p,o in g.triples((None, RDFS.subClassOf, proc)):

        #defining process URI

        p1 = URIRef(s)
        proc_name = (s.split('#')[-1])
        file1.write("name:\t"+proc_name+"\n")
        file1.write("type:\n")

        print("\n---------------Process "+proc_name+"-------------------")
        #check if its a Process

        xml_parse(proc_name, file1)


        #Get Definition of P
        Definition = g.value(p1, RDFS.isDefinedBy)
        file1.write("method:\n")
        print("Description: "+ Definition)
        file1.write("description:\t"+ Definition+"\n")

        #for label in g.objects(p1 rdfs.subClassOf hpc.Processes):
        #    print("----"+label)
        for s, p, o in g.triples((p1, hascommand, None)):
            print ("Process has command : " + o)
            comm = g.value(o, RDFS.isDefinedBy)
            print ("Command is defined by : (" + comm+")")
        #for s, p, o in g.triples((None, OWL.someValuesFrom, None)):
        #    print ("%s has Value  " + o)

        for temp in g.triples((p1, RDFS.subClassOf, proc)):
            #print (temp)
            for s, p, o in g.triples((temp, None, None)):
                print ("")
        file1.write("\n\n")

    print("\n--------------- End  ---------------------")

    print("\n\n\n------------Data- Set URI ------------------")
    SPARQL()



def SPARQL(cnpt):
    g = rdflib.Graph()
    g.parse('hpc-ontology-concept.ttl', format='turtle')


    query = """SELECT DISTINCT ?entity
        WHERE {
            
            ?entity rdfs:subClassOf ?concept.
            ?concept rdfs:subClassOf hpc:Concept
            
            FILTER( STRSTARTS (STR(?concept),str(hpc:"""+cnpt+""")) )
     
            
        }"""

    qres = g.query(query)
    Results = []
    for row in qres:
        Results.append(str(row).rsplit('#')[-1].rstrip(',)\''))
    print(*Results,sep='\n')

def SPARQL_py():
    from SPARQLWrapper import SPARQLWrapper, JSON

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(
        """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label
        WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        print(result["label"]["value"])

def main():
    #rdf_parser()
    #file1 = open("output.txt", "w")
    #rdf_general_match(file1)
    SPARQL("Performance")
    args = sys.argv[1:]

    if not args:
        print('usage: [--flags options] [inputs] ')
        sys.exit(1)


# Main body
if __name__ == '__main__':
    main()

