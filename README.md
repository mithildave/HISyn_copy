# HISyn

HISyn refers to "**h**uman learning **i**nspired **syn**thesizer". 

HISyn is built on NL understanding-driven approach, synthesizing domain specific language code expressions by
comparing the information in NL queries and NL API descriptions.

Details can be found in the paper *HISyn: Human Learning-Inspired Natural Language
Programming*(https://research.csc.ncsu.edu/picture/publications/papers/FSE20-HISyn.pdf) published on FSE2020.

## Play with HISyn
To deploy HISyn on local machine, after clone this repository, you also need to download the required third party packages. 
Please refer to instructions in [third_party_pkgs](./third_party_pkgs) to download and install all the necessary packages. 

After have StanfordNLP package deployed, you need to install the stanfordnlp python library:

      pip install stanfordnlp

The main-new.py and main-new.ipynb (*for jupyter notebook*) are main source code for running HISyn. After finishing setting up StanfordNLP, you
should be able to directly run these two codes.