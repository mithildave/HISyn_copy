#!/user/bin/env python3 -tt
"""
This Module contains Generic Data Processing APIs for HPC Datasets.
"""
import re
import os
import HISyn_copy.tools.Log as log

import pandas as pd
import shlex
import rdflib
from rdflib import URIRef
from rdflib.namespace import RDF
from rdflib.util import get_tree
import re

api_map = {
    "modelName":"hpc:AIModel",
    "datasetName":"hpc:Dataset",
    "projectName":"hpc:Project",
    "personName": "hpc:Person",
    "softwareName": "hpc:Software",
    "columnName":"concept"
}
def printSeparation():
    for i in range(0,50):
        print ('#', end ="")
    print("\n")

def get_tag(exp):
    tag = ""
    for key in api_map:
        if(exp.find(key) != -1):
            tag = api_map[key]
            break
    return tag

def Expression_Handling(exp, array):
    api_tag = get_tag(exp)
    name_tag = "hpc:name"
    if(api_tag=="hpc:Person"):
        name_tag = "hpc:givenName"
    tags = {}
    for i in range(0, len(array) - 1, 2):
        tags[array[i]] = array[i + 1]

    cond = ""
    for tag in tags:
        cond += "\t\t\t?x_item " + tag + " " + tags[tag] + "." + "\n"

    query = """

    PREFIX hpc:<https://github.com/HPC-FAIR/HPC-Ontology#>
    SELECT ?x_name
     WHERE { 
            ?x_item rdf:type """+api_tag+""". \n""" + cond + """\t\t\t?x_item """+name_tag+""" ?x_name 

        }"""
    print("Running Sparql query:")
    print(query)
    return query
def Expression_Handling_2(exp, array):
    var_count = 0
    api_tag = get_tag(exp)

    name_tag = "hpc:name"
    if ( api_tag == "hpc:Person" ):
        name_tag = "hpc:givenName"

    if (api_tag == "concept"):
        file_name = "cgo17-nvidia.csv"

        for pair in array:
            concept_tag = pair[1]
            query = """
            PREFIX hpc:<https://github.com/HPC-FAIR/HPC-Ontology#>
            PREFIX schema: <http://schema.org/>

            SELECT ?x_name
            WHERE{

                   ?dataset rdf:type hpc:Dataset.
                   ?dataset hpc:name \""""+file_name+"""\".
                   ?dataset hpc:hasColumn ?var.
                   ?var hpc:columnName ?x_name.
                   ?var hpc:columnTag ?colTag.
                   {SELECT ?colTag WHERE { ?props schema:domainIncludes """+concept_tag+""". 
                                            ?colTag rdfs:subPropertyOf* ?props}}          
            }"""
            print(query)
            return query
    cond = ""
    count = 0
    print (array)
    for pair in array:

        if(len(pair)==2):
            cond += "\t\t\t?x_item " + pair[0] + " ?obj" + str(count) + "." + "\n"
            cond += "\t\t\tFILTER(lcase(str(?obj" + str(count) + "))= \"" + pair[1].lower() + "\")" + "\n"
        else:
            cond += "\t\t\t?x_item " + pair[0] + " ?var" + str(count) + "." + "\n"
            cond += "\t\t\t?var"+ str(count) +" " + pair[-2] + " ?obj" + str(count) + "." + "\n"
            cond += "\t\t\tFILTER(lcase(str(?obj" + str(count) + "))= \"" + pair[-1].lower() + "\")" + "\n"


        count += 1
    query = """

    PREFIX hpc:<https://github.com/HPC-FAIR/HPC-Ontology#>
    SELECT ?x_name
     WHERE { 
            ?x_item rdf:type """+api_tag+""". \n""" + cond + """\t\t\t?x_item """+name_tag+""" ?x_name 

        }"""
    print(query)
    return query

def executeQuery_1(query):

    g = rdflib.Graph()
    g.parse('./allInOne.ttl', format='turtle')

    #printSeparation()
    #print ("                Results                ")
    #printSeparation()

    qres = g.query(query)
    result = "["
    for row in qres:
        d = str(row.asdict()['x_name'].toPython())
        #print (d)
        d= d.strip('"')
        result += "\'"+d+"\'" + ","

    result = result[:-1] + "]"

    return result

def hpc_parse(text):
    concept_regex = r'(string\([^\)]+\))'
    match = re.search(concept_regex, text)
    while match:
        newtext = match.group().lstrip("string")
        newtext = newtext[1:-1]
        text = text.replace(match.group(), "\"" + newtext + "\"", 1)
        match = re.search(concept_regex, text)

    cond_regex = r'(conditions\(([^\)]+)\))'
    match = re.findall(cond_regex, text)

    for each in match:

        newtext = each[1]
        re_text = newtext.replace("<", "").replace(">", "")
        text = text.replace(newtext, "\"<" + re_text + ">\"", 1)
    #print(text)
    return text

def substitue(exp,result):
    api =""
    for key in api_map:
        if(exp.find(key) != -1):
            api = key
            break


    pattern = r'('+api+'\(\))'
    match = re.search(pattern, exp)
    api_exp = match.group()
    #print (api_exp)
    result = api+"("+result+")"
    modify_expression = exp.replace(api_exp,result,1)
    printSeparation()
    print("                Modified Expression                ")
    printSeparation()
    print(modify_expression)
    return modify_expression

def conditions(cond):
    cond = cond.replace("'","\"")
    #print (cond)

    list = []
    regex = r'(<[^>]+>)'
    match = re.findall(regex, cond)
    if(match):
        for each in match:
            each = each.lstrip('<').rstrip('>')
            temp = shlex.split(each)
            list.append(temp)

    #print(list)
    return list

def processSparql(expression):

    expression = hpc_parse(expression)
    #print (expression)

    # Finding the conditions API and replace it with the sparql result

    exp_regex = r'(conditions\(([^\)]+)\))'
    match = re.findall(exp_regex, expression)
    condition = ""
    for each in match:
        condition += each[1].rstrip().lstrip()


    #condition = match.group(0).rstrip().lstrip()

    condition = "conditions("+condition+")"
    #print("here")
    #print (condition)


    modify_expression = expression
    modify_expression= modify_expression.replace(condition,"",1)
    print(modify_expression)

    # After we find conditions API: conditions("<hpc:jobTitle 'Senior Computer Scientist'> <hpc:gender 'Male'>")
    # We separate the input string
    cond_regex = r'(\([^\)]+\))'
    match = re.search(cond_regex, condition)
    cond = match.group(0).rstrip().lstrip()
    cond = re.sub("[()\"]","", cond)

    #print (cond)
    # Cond is the input of conditions API at this step

    # Running conditions API : it return the [tag,value] pairs
    tags= conditions(cond)
    # Expression handling : It creates a sparql query
    query = Expression_Handling_2(expression,tags)
    # Execute sparql
    result = executeQuery_1(query)
    # Replace it in the expression
    substitue(modify_expression,result)

    #executeQuery("")

def executeQuery(query):
    g = rdflib.Graph()
    g.parse('./allInOne.ttl', format='turtle')

    query1 = """
    PREFIX hpc:<https://github.com/HPC-FAIR/HPC-Ontology#>
    PREFIX schema: <http://schema.org/>

    SELECT ?colName
    WHERE{
        
           ?dataset rdf:type hpc:Dataset.
           ?dataset hpc:name "cgo17-nvidia.csv".
           ?dataset hpc:hasColumn ?var.
           ?var hpc:columnName ?colName.
           ?var hpc:columnTag ?colTag.
           {SELECT ?colTag WHERE { ?props schema:domainIncludes hpc:performance. 
                                    ?colTag rdfs:subPropertyOf* ?props}}          
    }"""
    query2 = """
    
    PREFIX hpc:<https://github.com/HPC-FAIR/HPC-Ontology#>
    PREFIX schema: <http://schema.org/>

    SELECT ?colTag
    WHERE{        
           ?dataset rdf:type hpc:Dataset.
           ?dataset hpc:name "cgo17-nvidia.csv".
           ?dataset hpc:hasColumn ?var.
           ?var hpc:columnName ?colName.
           ?var hpc:columnTag ?colTag.        
        
        }"""
    query0 = """
    PREFIX hpc:<https://github.com/HPC-FAIR/HPC-Ontology#>
    PREFIX schema: <http://schema.org/>
    SELECT ?colTag
    WHERE {
            ?props schema:domainIncludes hpc:performance.
            ?colTag rdfs:subPropertyOf* ?props
        }"""
    query4 = """

    PREFIX hpc:<https://github.com/HPC-FAIR/HPC-Ontology#>
    SELECT ?x_name
     WHERE { 
            ?x_item rdf:type hpc:File. 
			?x_item hpc:contributor ?var0.
			?var0 hpc:givenName ?obj0.
			FILTER(lcase(str(?obj0))= "chunhua")
			?x_item hpc:name ?x_name 
        }"""

    print(query4)
    qres = g.query(query4)
    print(qres)
    d = ""
    print("These are the concept properties:")
    for row in qres:
        d = str(row.asdict()['x_name'].toPython())
        print(d)
        d= d.strip('"')

    #return ""
    if d!="":
        return d.split(',')
    else:
        return ""
