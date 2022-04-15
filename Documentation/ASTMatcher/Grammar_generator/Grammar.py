class API:
    def __init__(self, name, param, output, desc, cat):
        self.name = name
        self.param = param
        self.ret = output
        self.desc = desc
        self.cat = cat

    def add_param(self, param):
        self.param.append(param)

    def add_ret(self, ret):
        self.ret = ret

    def display(self):
        print(self.ret, self.name, self.param, self.desc)


class NT:
    def __init__(self, name):
        self.name = name
        self.derivation = []
        self.source = []

    def add_derivation(self, derivation):
        self.derivation.append(derivation)

    def add_source(self, source):
        self.source.append(source)

    def display(self):
        print(self.name, '\t:=\t', self.derivation)

class Grammar:
    def __init__(self):
        self.ret_type_dict = {}   # {type name: nt object}  type stores as an nt object
        self.param_type_dict = {} # {type name: nt object}
        self.ret_type_class_dict = {}   # {type class: [type name]}
        self.nt_dict = {}   # {nt name: nt object}
        self.api_dict = {}  # {api name: api object}
        self.nt_list = []   # nt name
        self.api_list = []  # api name
        self.ck_list = []
        self.api_type_dict = {} # {api_type: api name}
        self.root = None
        self.grammar_text = ''

    def add_api(self, name, input, output, desc, cat):
        while name in self.api_dict:
            name += '_c'
        if '_c' in name and not desc:
            if self.api_dict[name.replace('_c', '')].desc:
                desc = self.api_dict[name.replace('_c', '')].desc
        elif '_c' in name and desc:
            if not self.api_dict[name.replace('_c', '')].desc:
                self.api_dict[name.replace('_c', '')].desc = desc
        tmp_api = API(name, input, output, desc, cat)
        self.api_dict[name] = tmp_api
        if cat in self.api_type_dict:
            self.api_type_dict[cat].append(name)
        else:
            self.api_type_dict[cat] = [name]
        self.api_list.append(name)

    def add_type(self):
        for api in self.api_dict.keys():
            ret_type_name = self.api_dict[api].ret
            if ret_type_name not in self.ret_type_dict:
                tmp_nt = NT(ret_type_name)
                tmp_nt.add_derivation(api)
                self.ret_type_dict[ret_type_name] = tmp_nt
            else:
                self.ret_type_dict[ret_type_name].add_derivation(api)
        for api in self.api_dict.keys():
            param_type_name = self.api_dict[api].param
            for param in param_type_name:
                if param not in self.ret_type_dict:
                    tmp_nt = NT(param)
                    tmp_nt.add_source(api)
                    self.param_type_dict[param] = tmp_nt
                else:
                    self.ret_type_dict[ret_type_name].add_source(api)

    def generate_type_based_grammar(self):
        for i in self.ret_type_dict.keys():
            tmp_text = ''
            for d in self.ret_type_dict[i].derivation:
                arg_text = '()'
                if self.api_dict[d].param[0]:
                    arg_text = '(' + d[0].capitalize() + d[1:]  + '_arg)'
                if not tmp_text:
                    tmp_text += (i + '\t:=\t' + d + arg_text + '\n')
                else:
                    tmp_text += ('\t\t|\t' + d + arg_text + '\n')
            self.grammar_text += (tmp_text + '\n')

        for i in self.api_dict.keys():
            if self.api_dict[i].param[0]:
                tmp_text = i[0].capitalize() + i[1:] + '_arg\t:=\t' + 'empty\n\t\t|\t'
                for param in self.api_dict[i].param:
                    # if param not in self.param_type_dict:
                    tmp_text += ( param + ',')
                tmp_text = tmp_text[0:len(tmp_text)-1] + '\n'
                self.grammar_text += (tmp_text + '\n')

        print(self.grammar_text)

    def add_nt(self, name, derivation, source):
        if not name in self.nt_dict:
            tmp_nt = NT(name)
            tmp_nt.add_derivation(derivation)
            tmp_nt.add_source(source)
            self.nt_dict[name] = tmp_nt
            self.nt_list.append(name)
        else:
            self.nt_dict[name].add_derivation(derivation)
            self.nt_dict[name].add_source(source)


    def write_to_file(self, file, text):
        file = open(file, 'a+', encoding='utf-8')
        file.write(text)

    def generate_grammar_file(self):
        for i in self.nt_list:
            text = i[0].capitalize() + i[1:] + '\t:=\t'
            for derivation in self.nt_dict[i].derivation:
                for param in derivation:
                    if not (param in self.param_type_dict or param in ['empty', 'Node', 'Matcher']):
                        text += param + '(' + param[0].capitalize() + param[1:] + '_arg)'
                        text += ','
                    else:
                        text += param
                        text += ','
                text = text[0:len(text)-1] + '\n' + '\t\t|\t'
            text = text[0:len(text)-4] + '\n'
            print(text)
            self.write_to_file('../grammar.txt', text)

    def generate_api_document(self):
        for i in self.api_dict.keys():
            text = i + '\ninput: '
            for param in self.api_dict[i].param:
                text += param + ','
            text = text[0:len(text)-1] + '\n'
            text += 'return: ' + self.api_dict[i].ret + '\n'
            text += 'description: ' + self.api_dict[i].desc + '\n\n'
            self.write_to_file('../API_documents.txt', text)






    def api_display(self):
        for i in self.api_list:
            self.api_dict[i].display()

    def ret_type_display(self):
        for i in self.ret_type_dict:
            self.ret_type_dict[i].display()

    def param_type_display(self):
        for i in self.param_type_dict:
            self.param_type_dict[i].display()

    def nt_display(self):
        for i in self.nt_list:
            self.nt_dict[i].display()