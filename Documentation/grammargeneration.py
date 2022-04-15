import sys
import os
sys.path.insert(0, '../..')
from HISyn_copy.Documentation.GrammarGenerator import GrammarGenerator
from HISyn_copy.tools.root_directory import root_dir

gram_gen = GrammarGenerator()

domain = 'HPC-FAIR'
gram_gen.generate_grammar(domain = 'HPC-FAIR', doc_file=root_dir + '/Documentation/' + domain +'/API_documents_autogen.txt')

for k in gram_gen.api_dict:
    gram_gen.api_dict[k].display()