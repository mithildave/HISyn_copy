import HISyn_copy.tools.Log as log
import HISyn_copy.back_end.back_end_function_kit as fc
import re


def parsing_rules(nlp, gg):
    print ("we are in backend *********")
    pattern_string = r'(string\d+)'
    pattern_cond = r'(condition\d+)'
    # variable_sub1 = r'(arg\d+)'
    pattern_concept = r'(concept\d+)'
    for dep in nlp.dependency:
        
        
        if re.match(pattern_string, nlp.token[dep.target].lemma):
            if 'nmod' not in dep.dep:
                dep.dep = 'keep'
            nlp.token[dep.target].ner = 'string'
            nlp.displayByEdge()
            replace_index = int(re.findall(r'(\d+)', nlp.token[dep.target].lemma)[0])
            nlp.token[dep.target].lemma = nlp.replaced_tokens[replace_index]

            nlp.token[dep.target].word = nlp.replaced_tokens[replace_index]
            print(nlp.token[dep.target].word)

        if re.match(pattern_cond, nlp.token[dep.target].lemma):
            dep.dep = 'keep'
            nlp.token[dep.target].ner = 'condition'
            nlp.displayByEdge()
            replace_index = int(re.findall(r'(\d+)', nlp.token[dep.target].lemma)[0])
            nlp.token[dep.target].lemma = nlp.replaced_tokens_condition[replace_index]

            nlp.token[dep.target].word = nlp.replaced_tokens_condition[replace_index]
            print(nlp.token[dep.target].word)

        # if re.match(variable_sub1, nlp.token[dep.target].lemma):
        #     dep.dep = 'keep'
        #     nlp.token[dep.target].ner = 'arg'
        #     nlp.displayByEdge()
        #     replace_index = int(re.findall(r'(\d+)', nlp.token[dep.target].lemma)[0])
        #     nlp.token[dep.target].lemma = nlp.replaced_tokens[replace_index]
        # 
        #     nlp.token[dep.target].word = nlp.replaced_tokens[replace_index]
        #     print(nlp.token[dep.target].word)
        #     
        if re.match(pattern_concept, nlp.token[dep.target].lemma):
             dep.dep = 'keep'
             nlp.token[dep.target].ner = 'concept'
             nlp.displayByEdge()
             replace_index = int(re.findall(r'(\d+)', nlp.token[dep.target].lemma)[0])
             nlp.token[dep.target].lemma = nlp.replaced_tokens_concept[replace_index]
             nlp.token[dep.target].word = nlp.replaced_tokens_concept[replace_index]
             print(nlp.token[dep.target].word)


def special_mapping_rules(nlp):
    pass


def special_cases_treatment(nlp, gg, text_index):
    pass