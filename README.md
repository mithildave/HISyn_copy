# INPOWS

INPOWS is a workflow synthesis framework that generates the workflow expressions which can be directly executed inside a Python script.
INPOWS referes to **I**nteractive **N**LU-**P**owered **O**ntology-based **W**orkflow **S**ynthesis. INPOWS allows the use of Natural Language for queries, maximizes the robustness in handling concepts and language ambiguities through an interactive ontology-based design, and achieves superior extensibility by adopting a synthesis algorithm powered by Natural Language Understanding. When being integrated into a FAIR data management system for HPC, INPOWS shows the efficacy in enabling flexible, robust, and extensible workflow synthesis. The overall framework of INPOWS is shown in the figure: [framework.pdf](https://github.com/mithildave/HISyn_copy/files/8494151/framework.pdf)


## Deployment

1. To deploy INPOWS on your local machine, you need to have python 3.8 installed on your host machine.

      You can download python 3.8 from [here](https://www.python.org/downloads/).
      
2. You also need JDK version 8, download it from [here](https://www.oracle.com/java/technologies/downloads/#java8).

3. Apart from python and java, you need to install few python libraries as well. All packages are mentioned inside requirements.txt file. Just run below command. 

```
python -m pip install -r requirements.txt
```

4. After cloning this repository, you also need to download the required third party packages. Refer to the instruction in [third_party_packages](https://github.com/mithildave/HISyn_copy/blob/main/third_party_pkgs/README.md) 


## Execution

The main-new.py is the entry point for running INPOWS. After finishing setting up StanfordNLP, you should be able to directly run the code in python.

      python main_new.py


#### How INPOWS work?:

A set of natural language queries needs to be selected by user from the CLI prompt. Then, they are passed through the DSL/ontology query split module of INPOWS. The user-selected DSL query is then given to HISyn. We use HPC ontology to store domain knowledge and meta data. Before HISyn processes the query, meta data is provided to the document generator to create a DSL grammar and API doc. Hereafter, HISyn performs dependency graph-based code synthesis and generates a workflow expression. While generating the workflow expression, if an ontology node is present in the dependency tree, the Ontology module is called to replace that node with the information retrieved via a sparql query. HISyn then generates the workflow code expression which is executable by the user. 

#### Details of the experiment:

The experiments have been conducted in two separate parts. Workflow synthesis module and DS split module have been evaluated separately to obtain the results mentioned in the paper. For the workflow synthesis task, queries are divided into three groups. 1) Data manipulation queries 2) Ontology Interactive simple queries and 3) Combined queries. Accuracies for all of them have been reported in the result section of the paper. For the DS split module, queries are divided in two groups. 1) Ontology interactive queries 2) All queries. Accuracies were reported for both ‘with’ and ‘without’ user interaction.  

## Result Data

The result data is provided in the [excel sheet](https://github.com/mithildave/HISyn_copy/blob/main/Experiments/Artifact%20Description.xlsx). There are two separate sheets named "Synthesis Accuracy" and "DS_Split Accuracy". These sheets each have 3 tables. 

Inside the sheet "Synthesis Accuracy" there are five columns in each table, "No., Query, Result, Accuracy from formatted query,NL Accuracy". Here is the description of each column:

```
1. No. - Query Number
2. Query - user query, input for INPOWS
3. Result - Synthesized code expression returned from INPOWS
4. Accuracy from formatted query - accuracy for DSL query (0:Fail,1:Pass)
5. NL Accuracy - accuracy for natural language query (0:Fail,1:Pass)
```
Inside the sheet "DS_Split Accuracy" there are five columns in each table, "No., Query, Result, Accuracy w/o interaction,Accuracy w/ interaction". Here is the description of each column:

```
1. No. - Query Number
2. Query - user query, input for INPOWS
3. Result - Synthesized code expression returned from INPOWS
4. Accuracy w/o interaction - accuracy when user interaction was not imposed (0:Fail,1:Pass)
5. Accuracy w/ interaction - accuracy when user interacts with the module to select best suited result (0:Fail,1:Pass)
```

The consolidated results can be visualized using this chart. [accuracy_chart.pdf](https://github.com/mithildave/HISyn_copy/files/8494206/accuracy.1.pdf)
