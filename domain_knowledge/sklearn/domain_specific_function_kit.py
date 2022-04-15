import HISyn.tools.Log as log
import HISyn.back_end.back_end_function_kit as fc


# domain specific knowledge for flight domain
def parsing_rules(nlp, gg):
    pass


def special_mapping_rules(nlp):
    for dep in nlp.dependency:
        if dep.dep == 'nmod:to':
            dep.dep = 'nmod'


def special_cases_treatment(nlp, gg, text_index):
    pass
