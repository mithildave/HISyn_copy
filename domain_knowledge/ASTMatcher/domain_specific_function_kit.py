import HISyn.tools.Log as log

other_query_list = ['fare', 'time', 'airline', 'type', 'cost']
question_word = ['what', 'which']


# domain specific knowledge for flight domain
def parsing_rules(nlp, gg):
    log.log('Set special knowledge for ast domain...')
    for dep in nlp.dependency:
        if nlp.token[dep.target].word in ['cxx']:
            for api in gg.api_dict.keys():
                print(api)
                if 'cxx' in api:
                    nlp.token[dep.target].ner = 'translated'
                    nlp.token[dep.target].mapping.append(api)
        elif nlp.token[dep.target].ner == 'STRING':
            dep.dep = 'TRANS'

    log.log('Special knowledge for ast domain finished')


def special_mapping_rules(nlp):
    for dep in nlp.dependency:
        if nlp.token[dep.source].lemma == 'forstatement':
            nlp.token[dep.source].mapping = ['forStmt']
        elif nlp.token[dep.target].lemma == 'forstatement':
            nlp.token[dep.target].mapping = ['forStmt']
        if nlp.token[dep.target].lemma == 'continuestatement':
            nlp.token[dep.target].mapping = ['continueStmt']
        elif nlp.token[dep.source].lemma == 'continuestatement':
            nlp.token[dep.source].mapping = ['continueStmt']
        if nlp.token[dep.target].lemma == 'ifstatement':
            nlp.token[dep.target].mapping = ['ifStmt']
        elif nlp.token[dep.source].lemma == 'ifstatement':
            nlp.token[dep.source].mapping = ['ifStmt']
        if nlp.token[dep.target].lemma == 'nullstatement':
            nlp.token[dep.target].mapping = ['nullStmt']
        elif nlp.token[dep.source].lemma == 'nullstatement':
            nlp.token[dep.source].mapping = ['nullStmt']
        # if nlp.token[dep.target].lemma == 'elsestatement':
        #     nlp.token[dep.target].mapping = ['elseStmt']
        # elif nlp.token[dep.source].lemma == 'thenstatement':
        #     nlp.token[dep.source].mapping = ['thenStmt']

        elif nlp.token[dep.source].word in ['is']:
            nlp.token[dep.source].mapping = []

        if dep.dep == 'nmod:to':
            dep.dep = 'nmod'
        elif dep.dep == 'nmod:with':
            dep.dep = 'nmod'

        if 'name' in nlp.token[dep.target].lemma and nlp.token[dep.source].ner == 'translated':
            nlp.token[dep.target].mapping = []
            # dep.dep = 'name'
            for d in nlp.dependency:
                if d.source == dep.target:
                    d.source = dep.source
                if d.target == dep.target:
                    d.target = dep.source
        elif 'name' in nlp.token[dep.source].lemma and nlp.token[dep.target].ner == 'translated':
            nlp.token[dep.source].mapping = []
            # dep.dep = 'name'
            tmp = nlp.token[dep.source]
            nlp.token[dep.source] = nlp.token[dep.target]
            nlp.token[dep.target] = tmp
            for d in nlp.dependency:
                if d.source == dep.target:
                    d.source = dep.source
                if d.target == dep.target:
                    d.target = dep.source

        if 'equals_c_c' in nlp.token[dep.target].mapping and nlp.token[dep.source].ner == 'translated':
            nlp.token[dep.target].mapping = []
            # dep.dep = 'name'
            for d in nlp.dependency:
                if d.source == dep.target:
                    d.source = dep.source
                if d.target == dep.target:
                    d.target = dep.source
        elif 'equals_c_c' in nlp.token[dep.source].mapping and nlp.token[dep.target].ner == 'translated':
            nlp.token[dep.source].mapping = []
            # dep.dep = 'name'
            tmp = nlp.token[dep.source]
            nlp.token[dep.source] = nlp.token[dep.target]
            nlp.token[dep.target] = tmp
            for d in nlp.dependency:
                if d.source == dep.target:
                    d.source = dep.source
                if d.target == dep.target:
                    d.target = dep.source



def special_cases_treatment(nlp, gg, text_index):
    pass


def set_shortest_path(nlp, length):
    for dep in nlp.dependency:
        path = []
        if len(dep.paths) > length:
            log.log('dependency paths length: ', len(dep.paths))
            dep.paths.sort(key = len)
            path.append(dep.paths[0])
            min_path_len = len(dep.paths[0])
            index = 1
            while len(path[-1]) == min_path_len and index < len(dep.paths):
                # log.err(path)
                path.append(dep.paths[index])
                index += 1
                if len(path[-1]) > min_path_len and len(path) < length - 5:
                    min_path_len = len(path[-1])
            dep.paths = path
            log.log('paths length after set: ', len(dep.paths))
            log.test('new paths: ', dep.paths)

