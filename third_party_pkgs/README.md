## third_party_pkgs
This directory is used store third party packages that used in INPOWS.

### Package instructions

- Step 1: Download StanfordCoreNLP

   Download the version 3.9.2(2018-10-05) from stanfordnlp official website (https://stanfordnlp.github.io/CoreNLP/history.html).
   

- Step 2: Unzip the package and put the entire folder under *third_party_pkgs* folder.
   
   The directory should look like:
   
        -HISyn
        --third_party_pkgs
        ---stanford-corenlp-full-2018-10-05
        ---start_nlp_server.sh

- Step 3: Run StanfordNLP server
   Run start_nlp_server.sh at command line
   
        sh start_nlp_server.sh

   This command will start a StanfordNLP sever at port 9000. The front end of INPOWS will pass the text to the server through nlp clinet and get the NLP results.
