import sys
import os

sys.path.insert(0, '..')
from HISyn_copy.tools.root_directory import root_dir
import HISyn_copy.tools.Log as log


def run_HISyn(domain, text='', index=0):
    # get query from test cases

    import HISyn_copy.front_end.front_end_function_kit as front_kit
    if not text:
        text = front_kit.read_text(root_dir + '/Documentation/' + domain + '/text_new.txt', index)

    # Build grammar graph
    import HISyn_copy.domain_knowledge.DomainKnowledgeConstructor as dkc
    gg = dkc.set_grammar_graph(domain, root_dir + '/Documentation/' + domain + '/grammar_adv.txt',
                               root_dir + '/Documentation/' + domain + '/API_document_adv.txt', reload=True)

    gg.build_test()

    nlp = front_kit.nlp_parsing(text, domain)

    nlp.displayByEdge()
    front_kit.domain_specfic_parsing_rules(domain, nlp, gg)

    import HISyn_copy.common_knowledge.NLPCommonKnowledge as nlpck
    front_kit.prune_edges(nlp, nlpck.prunable_dep_tags, nlpck.prunable_pos_tags, nlpck.common_knowledge_tags)

    nlp.displayByEdge()

    import HISyn_copy.back_end.back_end_function_kit as back_kit

    back_kit.semantic_mapping(domain, gg, nlp, nlpck.common_knowledge_tags)

    nlp.displayByEdge()

    back_kit.longest_matching(nlp)

    [dependent_dict, no_gov_source_dict, empty_mapping_source_edge_dict, root_index] = back_kit.reordering(nlp, gg,
                                                                                                           nlpck.preposition)

    print(empty_mapping_source_edge_dict)
    nlp.displayByEdge()

    back_kit.reversed_all_path_searching(domain, nlp, gg, dependent_dict)

    nlp.displayByEdge()

    final_cgt_list = back_kit.path_selection_and_combination(nlp, gg, dependent_dict, root_index)

    [min_expr, expr_list] = back_kit.code_generation(gg, final_cgt_list)

    for i in min_expr:
        print('-', i)
    # for i in expr_list:
    #    print('-', i)

    return [min_expr, expr_list]


if __name__ == '__main__':
    domain = 'HPC-FAIR'

    text = 'get columns {memory related concept} from the file <cgo17-nvidia.csv>'
    text = 'get column names from file "cgo17-nvidia.csv"'
    text = 'convert file "abc.json" to csv'
    text = 'Convert data file "X.csv" to JSON format'
    text = 'get normalized result for "l1cache" from file "cgo17-nvidia.csv"'
    text = 'get count of column "X" from file "Y", group by "Model"'
    text = 'get count of column "X" from file "Y", group by "Model,BenchNumber"'
    text = 'merge dataset "X.csv" with dataset "Y.csv"'
    text = 'get encoding result for "l1cache" from file "cgo17-nvidia.csv" with type "oneHotEncoding"'
    text = 'get encoding result for "l1cache" from file "cgo17-nvidia.csv"'
    text = 'merge file "X.csv" with file "Y.csv"'
    text = 'get multiplication of column "X" from file "A" and  column "Y" from file "B"'
    text = 'get all columns from the dataset <cgo17-nvidia.csv> without column <MemoryFrequency>'
    text = 'get encoding result for <l1cache> from file <cgo17-nvidia.csv> with type <oneHotEncoding>'
    text = 'get dataset <X> from dataset <Y> without column <Memory Frequency>'
    text = 'get multiplication of column <X> from file <A> and  column <Y> from file <B>'
    text = 'get <X> from dataset <Y> without column <Memory Frequency>'
    text = 'get multiplication of column <X> from dataset <A> and column <Y> from <B>'
    text = 'get merging result of <X,Y,Z> from dataset <w>'

    text = "get dataset with <hpc:Project 'Xplacer'>"
    text = "get dataset with <hpc:Id 'DA00001'>"
    text = "get all dataset <hpc:fundedBy 'NSF' hpc:subject 'PerformancePrediction'>"
    text = "get machine <hpc:name 'NVIDIA_100' hpc:SoftwareArchitecture 'GPU'>'"
    #text = "get AI model names of a <hpc:targetMachine 'lassen'>"
    #text = "get AI model with <hpc:modelType 'Classification'>"
    #text = "get AI model with <hpc:version '1.2.1' hpc:learningtype 'Classification'>"
    #text = "get merging result of <X,> from dataset with<hpc:Project 'Xplacer'> "
    #text = "get AI model with <hpc:type 'classification'>"


    #text = "get AI model with <hpc:modelType 'Prediction' hpc:targetMachine hpc:lassen >"
    #text = "get AI model with <hpc:learningType 'Supervised' hpc:subject 'Gradient Decent'>"
    #text = "get AI model with <hpc:modelType 'Classification'>"
    #text = "get AI model with <hpc:modelFormat 'PYTHON'>"
    #text = "get AI model with <hpc:modelFormat 'PYTHON NOTEBOOK'>"
    #text = "get AI model with <hpc:learningType 'Supervised' hpc:subject 'Gradient Decent'>"
    #text = "get AI model with <hpc:modelType 'Prediction'>"

    #text = "get AI model with <hpc:learningType 'Supervised' hpc:subject 'Gradient Decent'>"
    #text = "get AI model with <hpc:modelType 'Prediction'>"
    #text = "get AI model with <hpc:modelFormat 'PYTHON NOTEBOOK'>"


    text = "get dataset with <hpc:subject 'high-performance computing'>"
    text = "get dataset with <hpc:project hpc:name 'PR000001'>"
    text = "get dataset with <hpc:subject 'Heterogeneous  System'>"
    text = "get dataset with <hpc:license 'GPL-3.0'>"
    text = "get dataset with <hpc:version '0.2.0' hpc:subject 'LLVM'>"
    text = "get all dataset <hpc:fundedBy 'NSF' hpc:subject 'PerformancePrediction'>"
    text = "get dataset with <hpc:name 'dataflow_logs_20.06.01.tar.bz2'>"
    text = "get project <hpc:fundedBy 'Lawrence Livermore National Laboratory'>"
    text = "get project <hpc:programArea 'OpenMP'>"
    text = "get project <hpc:fundedBy 'ICT' hpc:programArea 'parallel computing'>"
    text = "get project <hpc:fundedBy 'ICT'>"
    text = "get person <hpc:affiliation 'Lawrence Livermore National Laboratory, CA'> "
    text = "get person with <hpc:memberOf 'Center for Applied Scientific Computing'>"
    text = "get person <hpc:affiliation 'Lawrence Livermore National Laboratory, CA'> "
    text = "get person <hpc:affiliation 'Lawrence Livermore National Laboratory, CA'> "
    text = "get person having <hpc:jobTitle 'Senior Computer Scientist' hpc:gender 'Male'>"

    #Advance


    text = "Get software <<hpc:usedBy> <experiment hpc:name 'OPUM'>>"
    text = "Get all columns from the dataset with <hpc:name X> "
    text = "Get software with <hpc:version '16.2'>"
    text = 'convert file "abc.json" to csv'
    text = "Get software <hpc:usedBy experiment hpc:name 'Optimal Unified Memory - Postprocess Steps'>"
    text = "get dataset with <<hpc:version '0.2.0'> <hpc:subject 'LLVM'>>"
    text = "Get software with <hpc:version '16.2'>"
    text = "Get software with <<hpc:version '16.2'>  <hpc:usedBy project hpc:name 'X'>>"
    text = "Get software <hpc:usedBy experiment hpc:name 'Optimal Unified Memory - Postprocess Steps'>"
    text = "Get columns from the dataset <hpc:name 'X'>"
    text = "get dataset with <<hpc:version '0.2.0'> <hpc:subject 'LLVM'>>"
    text = "Get all columns from the dataset <hpc:name 'X'>"
    text = "get normalization result for \"X,Y\" from dataset with <hpc:name 'Z'>"
    text = "merge dataset \"X\" and dataset with <hpc:license 'Apache'> "
    text = "convert file <hpc:contributor having hpc:name 'caleb'> to json"
    text = "Get software with <<hpc:version '16.2'>  <hpc:usedBy project hpc:name 'X'>>"
    text = "Get all files with <hpc:contributor which has hpc:givenName 'Lee'>"

    text = "Get Hardware <hpc:usedBy experiment hpc:name 'OPUM'>"
    text = "Get all member for <hpc:Project which has hpc:name 'GPU Kernel'>"
    text = "Get dataset <hpc:generatedBy Experiment hpc:name 'Optimal Unified Memory - Online Inference'>"
    text = "Get column \"memory related concept\" from dataset with <hpc:name 'X'>"
    text = "get column {GPU Cache performance} from dataset \"abc.csv\""
    text = "get column {GPU Cache performance} from file \"abc\""
    text = "Get Hardware <hpc:usedBy experiment hpc:name 'OPUM'>"
    text = "Get software with <<hpc:version '16.2'>  <hpc:usedBy project hpc:name 'X'>>"
    text = "get person having <<hpc:jobTitle 'Senior Computer Scientist'> <hpc:gender 'Male'>>"
    text = "get AI model with <hpc:modelType 'Classification'>"

    text = "get AI model with <<hpc:version '1.2.1'> <hpc:learningType 'Supervised'>>"
    text = "Get software with <<hpc:version '16.2'>  <hpc:usedBy project hpc:name 'X'>>"
    text = "Get software having <hpc:usedBy something> and  <hcp: else>"
    text = "Get AI model with <hpc:tag> and <hpc:another>  <hpc:another>"
    text = "Get ai model <hpc:usedBy something>"
    text = "get AI model <hpc:version '1.2.1'> "
    text = "return me AI model with <hpc:modelType 'Classification'>"
    text = "Get software <hpc:usedBy something> and <this> is 'X'"
    text = "give AI model having <hpc:modelType 'Classification'>"
    text = "give AI model <hpc:modelType 'Classification'>"
    text = 'return me AI model with "y"'
    text = "Get software which is <hpc:usedBy something> and <some> "
    text = "list of software having <name 'X'>"


    text = 'get column <schema:domainIncludes hpc:cpu> from file "X"'
    text = "give AI model <hpc:modelType 'Classification'>"
    text = 'get <schema:domainIncludes hpc:cpu> data from file "X"'
    text = "Get AI model with <hpc:tag> and <hpc:another> and  <hpc:another2>"
    text = "Get columns from dataset <hpc:name 'X'>"
    text = 'Get <schema:domainIncludes hpc:Memory> from file "cgo-nvidia"'
    text = "Get all member for <hpc:Project which has hpc:name 'GPU Kernel'>"
    q0 = "get dataset <hpc:fundedBy 'NSF'> and having <hpc:subject 'PerformancePrediction'>"
    text = "get AI model with <hpc:modelType 'Prediction'>"

    q1 = "list of  AI models with <hpc:modelFormat 'python notebook'>"
    q2 = 'get all data columns from file "X" except "P"'
    q3 = 'get data dealing with <schema:domainIncludes hpc:cpu> from file "Y"'
    q4 = 'extract data linked to <schema:domainIncludes hpc:cpu> from file "X" '
    q5 = "normalize the columns \"X,Y\" from file <hpc:name 'Z'>"
    q6 = "get a list of people with <hpc:contributor to a project named 'GPU kernal'"
    q7 = "get files having <hpc:contributor with hpc:givenName 'Lee'>"
    q8 = "get files which are <hpc:contributor by hpc:givenName 'Lee'>"
    q9 = "get dataset having <hpc:contributor by a person hpc:givenName 'chunhua'>"
    q10 = "get software having <hpc:version '16.2'>  and <hpc:usedBy by project hpc:name 'X'>"
    q11 = "give me hardware <hpc:usedBy experiment hpc:name 'OPUM'>"
    q12 = "get hardware that was <hpc:usedBy experiment hpc:name 'OPUM'>"
    q13 = "merge dataset \"X\" with another dataset with <hpc:license 'Apache'>"
    q14 = "convert file having <hpc:contributor hpc:givenName 'caleb'> to json format"

    query_synthesis = ['Get all the column names of dataset "cgo17-nvidia.csv"',
                               'Convert file "X" to CSV format',
                               'get normalized result for "l1cache" from file "cgo17-nvidia.csv"',
                               'get count of column "X" from file "Y", group by "Model"',
                               "get AI model with <hpc:modelType 'Prediction'>",
                               "get person <hpc:affiliation 'Lawrence Livermore National Laboratory, CA'> ",
                               "get dataset with <hpc:subject 'Heterogeneous  System'>",
                               "get project having <hpc:programArea 'parallel computing'>",
                               "get files having <hpc:contributor with hpc:givenName 'chunhua'>",
                               ]

    query_dssplit = [ "get AI model that has model type 'prediction'",
                      "get dataset having subject 'Heterogeneous System'",
                      "Get memory related data from file 'cgo-nvidia.csv'",
                      "get files having contributor with name 'Lee'"]


    text = q13


    import HISyn_copy.DSSplit.DSL_ontology_split as dsp
    import HISyn_copy.domain_knowledge.Ontology.sparql as sparql

    import HISyn_copy.sparql.sparql as sq
    import HISyn_copy.Workflow.workflow_API as wf

    while 1:
        module = input("\n\nEnter the module you want to access \n (Enter : 1) Workflow Synthesis \n (Enter : 2) DS Split \n (Enter : 0) Exit\n")
        if module == "0":
            break
        if module == "1":
             print("List of queries: \n ")
             count = 0
             for q in query_synthesis:
                 print (str(count)+" --> "+q)
                 count+=1

             query = input("\nSelect your query number from the list above:\n")
             text = query_synthesis[int(query)]
             expression = run_HISyn(domain, text, index=1)
             if int(query) in range(4,10):
                 BestExpression = input(" Enter the best expression to parse using SPARQL module:\n ")
                 sq.processSparql(str(BestExpression))

        if module == "2":
             print("List of queries: \n ")
             count2 = 0
             for q in query_dssplit:
                 print (str(count2)+" --> "+q)
                 count2 +=1
             query = input("\n Select your natural language query number from list above:\n")
             text = query_dssplit[int(query)]
             text = dsp.DSL_ontology_split(text)