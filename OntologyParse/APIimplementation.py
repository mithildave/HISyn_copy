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
import re
from HISyn.tools.root_directory import root_dir

#from lxml import ET
f = open("OntologyParse/API.py", "w")
f.write("import os\n")
f.write("flag0=flag1=flag2=flag3=flag4=flag5=flag6=flag7=flag8=0\n")
count =0 
filepath = "/Users/mdave2/Documents/HISyn/Files/"
def find_path(s_name):
    import xml.etree.ElementTree as ET
    from re import search
    tree = ET.parse('OntologyParse/Ontology_latest_new.xml')
    root = tree.getroot()
    Path = "hasScriptPath"
    namespaces = {'owl': 'http://www.w3.org/2002/07/owl#', 'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#' , 'rdfs' : 'http://www.w3.org/2000/01/rdf-schema#' }  # add more as needed
    for NI in root.findall('owl:NamedIndividual', namespaces):
        attr = str(NI.attrib)
        if search(s_name,attr):

            ans = NI.find('{http://www.w3.org/2000/01/rdf-schema#}isDefinedBy')
            print(ans.text)
            return ans.text

def find_data_path(s_name):
    import xml.etree.ElementTree as ET
    from re import search
    tree = ET.parse('OntologyParse/Ontology_latest_new.xml')
    root = tree.getroot()
    namespaces = {'owl': 'http://www.w3.org/2002/07/owl#', 'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#' , 'rdfs' : 'http://www.w3.org/2000/01/rdf-schema#' }  # add more as needed
    for NI in root.findall('owl:NamedIndividual', namespaces):
        attr = str(NI.attrib)
        if search(s_name,attr):

            ans = NI.find('{https://github.com/HPC-FAIR/HPC-Ontology#}Path')
            print(ans.text)
            return ans.text

def write_API(apiPath, apiName , apiArg):
    global count
    argnew = ""
    if(apiArg!=""):
        apiArg= apiArg.replace(".", "_")
        apiArg = apiArg.replace("-", "_")
        apiArg2 = apiArg.replace(",", " ").rstrip()


        for each in apiArg2.split("  "):
            argnew+=file_Path(each)+" "


    text = 'def ' + apiName + '(' + apiArg + '):\n' \
            '\tglobal flag'+str(count)+'\n'\
            '\tif(flag'+str(count)+'==1):return\n'\
            '\telse: flag'+str(count)+'=1\n'\
            '\tprint( "Running: '+apiName+'\")\n'\
            '\tfunc_path = \"' + apiPath + '\"\n' \
            '\tinput_file = \"' + argnew + '\"\n'\
            '\tos.chdir(\'/Users/mdave2/\')\n'\
            '\tos.system (func_path+\' \'+input_file) \n\n\n'

    f.write(text)
    count=count+1
    #To be Added
#nsight_log
def file_Path(arg):
    if(arg!="fvcorr" and arg!="None"):
        inpstr =  arg.lstrip('_')
        indx= inpstr.rfind('_')
        inpstr = inpstr[:indx]+"."+inpstr[indx+1:]
        print(inpstr)
    else:
        inpstr=arg
    inppath = find_data_path((inpstr)) + (inpstr)
    return (inppath)

def xml_parse(proc, file1):
    import xml.etree.ElementTree as ET
    #from lxml import etree as ET
    from re import search

    tree = ET.parse('OntologyParse/Ontology_latest_new.xml')
    root = tree.getroot()

    namespaces = {'owl': 'http://www.w3.org/2002/07/owl#', 'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'}  # add more as needed
    Proc = proc
    Out = "hasOutput"
    In = "hasInput"
    Prereq = "hasPrereq"
    Path = "hasScriptPath"
    prereq =[]
    input = []
    output = []
    path = []
    for Class in root.findall('owl:Class', namespaces):
        attr = str(Class.attrib)

        if search(Proc, attr):
            definition = Class.find('{http://www.w3.org/2000/01/rdf-schema#}isDefinedBy')

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
                    if search(Path, attr):

                        items = Res.iter('{http://www.w3.org/2002/07/owl#}hasValue')
                        for item in items:
                            attr = str(item.attrib)
                            split_array = attr.split('#')
                            s_name = (split_array[-1])[:-2]
                            print("Action Command -----> " + s_name)
                            print (s_name)
                            path = find_path(s_name)


    #Check if multiple Return

    flag=len(output)
    while(flag):
        flag=flag-1

        file1.write("name:\t"+Proc+"\n")
        file1.write("type:\n")



        file1.write("return:\t")
        file1.write(output[flag])

        file1.write("\n")

        file1.write("argument:\t")
        argm = input + prereq

        for each in input:
            if(each!="None"):
                file1.write(each)

            if(input.index(each)!=len(input)-1):
                file1.write(",")

        file1.write("\n")

        file1.write("prereq:\t")

        for each in prereq:
            file1.write(each)
            if(prereq.index(each)!=len(prereq)-1):
                file1.write(",")

        file1.write("\n")

        arg_text = ""
        for each in input:
            if(each!="None"):
                arg_text += each
            if(input.index(each)!=len(input)-1):
                arg_text += ", "

        file1.write("method:\n")
        print("Description: "+ definition.text)
        file1.write("description:\t"+ definition.text+"\n")
        file1.write("\n\n")
    write_API(path, Proc, arg_text)

def rdf_parser():
    # create a Graph
    g = rdflib.Graph()

    # parse in an RDF file
    result = g.parse('OntologyParse/hpc-ontology_new.ttl', format='turtle')

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

    result = g.parse('OntologyParse/hpc-ontology_new.ttl', format='turtle' )

    hpc = URIRef("https://github.com/HPC-FAIR/HPC-Ontology#")
    hascommand = URIRef("https://github.com/HPC-FAIR/HPC-Ontology#hasCommand")
    proc = URIRef("https://github.com/HPC-FAIR/HPC-Ontology#Processes")

    for s,p,o in g.triples((None, RDFS.subClassOf, proc)):

        #defining process URI

        p1 = URIRef(s)
        proc_name = (s.split('#')[-1])
        #Writing the API

        #file1.write("name:\t"+proc_name+"\n")
        #file1.write("type:\n")

        print("\n---------------Process "+proc_name+"-------------------")
        #check if its a Process

        xml_parse(proc_name, file1)


        #Get Definition of P
        Definition = g.value(p1, RDFS.isDefinedBy)
        #file1.write("method:\n")
        print("Description: "+ Definition)
        #file1.write("description:\t"+ Definition+"\n")

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
        #file1.write("\n\n")

    print("\n--------------- End  ---------------------")

    print("\n\n\n------------Data- Set URI ------------------")


def editExpression(st):

        #words = list(map(str, st.split(')')))
        array = re.split(',|\(|\)| ', st)
        for each in array:
            if re.search('log|csv|fvcor|None',each):
                newst= "'"+each+"'"
                st= st.replace(each,newst)
        return st[2:-2]

def call_API(argv):
    f.write("if __name__ == '__main__':\n")
    st = editExpression(str(argv))
    f.write("\t"+st+"\n")
    print("Finished API process")

def main():
    #rdf_parser()
    text= root_dir + '/Documentation/' + 'HPC-FAIR' + '/API_documents_autogen.txt'
    file1 = open(text, "w")
    #find_data_path("dataset.csv")
    rdf_general_match(file1)




