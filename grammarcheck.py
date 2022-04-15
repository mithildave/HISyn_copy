import sys
import re

class APIDoc:

    name = ''
    input = ''
    ret = ''
    desc = ''

    def __init__(self, name, input, ret, desc):
        self.name = name
        self.input = input
        self.ret = ret
        self.desc = desc
    
    def has_desc(self):
        if self.desc == '' or self.desc.isspace():
            return False
        else:
            return True

    def has_name(self):
        if self.name == '' or self.name.isspace():
            return False
        else:
            return True

    def has_input(self):
        if self.input == '' or self.input.isspace():
            return False
    
    def has_ret(self):
        if self.ret == '' or self.ret.isspace():
            return False
        else:
            return True

def check_documentation(domain):
    grammar_doc = open('Documentation/' + domain + '/grammar.txt', 'r').readlines()
    api_doc_strings = open('Documentation/' + domain + '/API_documents.txt', 'r').readlines()
    
    api_docs = []
    try:
        for i in range(0, len(api_doc_strings)):
            name = ''
            input = ''
            ret = ''
            desc = ''

            api_doc_string = api_doc_strings[i]

            if api_doc_string.isspace():
                continue
            if not api_doc_string.strip()[0:7]  == 'input:'\
                and not api_doc_string.strip()[0:8]  == 'return:'\
                and not api_doc_string.strip()[0:13] == 'description'\
                and not api_doc_string.strip().isspace():
                name = api_doc_string.strip()
                i += 1
                api_doc_string = api_doc_strings[i]
            if api_doc_string.strip()[0:6]  == 'input:':
                input = api_doc_string.strip()[6:].strip()
                i += 1
                api_doc_string = api_doc_strings[i]
            if api_doc_string.strip()[0:7]  == 'return:':
                ret = api_doc_string.strip()[7:].strip()
                i += 1
                api_doc_string = api_doc_strings[i]
            if api_doc_string.strip()[0:12] == 'description:':
                desc = api_doc_string.strip()[12:].strip()
            api_docs.append(APIDoc(name, input, ret, desc))
    except Exception as e:
        print('an exception occurred at line ' + str(i + 1) + ' of api document')

    missing_warnings = set()
    input_warnings = set()
    ret_warnings = set()
    desc_warnings = set()


    for grammar_string in grammar_doc:
        found = False
        for token_one in grammar_string.split():
            for token in token_one.split('|'):
                if '(' in token:
                    api = token[:token.index('(')]
                    for node in api_docs:
                        if node.name == api:
                            found = True
                            if not node.has_input():
                                input_warnings.add(api)
                            if not node.has_ret():
                                ret_warnings.add(api)
                            if not node.has_desc():
                                desc_warnings.add(api)
                    if not found:
                        missing_warnings.add(api)

    print()
    for api in missing_warnings:
        ret_warnings.discard(api), input_warnings.discard(api), desc_warnings.discard(api)
    if (missing_warnings):
        print("The following APIs are missing from the doc altogether:")
        for api in missing_warnings:
            print(api, end=', ')
        print('\n')

    if (input_warnings):
        print("The following APIs are missing input descriptions")
        for api in input_warnings:
            print(api, end=', ')
        print('\n')

    if (ret_warnings):
        print("The following APIs are missing return descriptions:")
        for api in ret_warnings:
            print(api, end=', ')
        print('\n')

    if (desc_warnings):
        print("The following APIs are missing API descriptions:")
        for api in desc_warnings:
            print(api, end=', ')
        print('\n')

def check_grammar(domain):
        grammar_file = open('Documentation/' + domain + '/grammar.txt', 'r').readlines()

        # Group grammar as terms
        grammar_list = []
        tmp_grammar = []
        for g in grammar_file:
            if g[0] == '#':
                continue
            else:
                if g[0] == '\n' or g == grammar_file[-1]:
                    grammar_list.append(tmp_grammar)
                    tmp_grammar = []
                else:
                    tmp_grammar.append(g)

                # Set grammar into string
        remove_list = []
        grammar_string = []
        for g in grammar_list:
            if len(g) == 0:
                remove_list.append(g)
            else:
                tmp = ''.join(g).replace('\n', '').replace('\t', '').replace(' ', '')
                grammar_string.append(tmp)
        for r in remove_list:
            grammar_list.remove(r)

        nt_nodes = []
        derivations_and_params = []

        for grammar in grammar_string:
            grammar_split = grammar.split(':=')

            # add nt
            nt_nodes.append(grammar_split[0])

            if len(re.findall(r'\(', grammar_split[1])) > 1:
                print("There are multiple apis in the derivation of " + grammar_split[0])

            # split each derivation
            derivations = grammar_split[1].split('|')

            for d in derivations:
                # this derivation doesn't have API
                if '(' not in d:
                    elements = d.split(',') 
                    derivations_and_params.extend(elements)

                # this derivation has API
                else:
                    # create API, extract API parameters, put API into nt's derivations
                    api = d.split('(')
                    api_names = api[0]
                    api_parameters = api[1].replace(')', '').split(',')
                    derivations_and_params.extend(api_parameters)
        for nt in nt_nodes:
            if not nt in derivations_and_params:
                print('No path to ' + nt)

if __name__ == '__main__':
    domain = sys.argv[1]
    check_documentation(domain)
    # check_grammar(domain)
    

                        
            
