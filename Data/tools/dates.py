from csv import reader, writer
from random import shuffle

FILE_DATES = 'files/'
def modulo(i):
    if i < 0:
        return -i
    
    return i

def filter(function):
    def parameters(self, opts, each, hits, display=False):
        index_reponse = self.types_of_answers.index(each[-1])
        index_return = function(opts)

        if index_return == index_reponse:
            hits += 1
        
        else:
            if display:
                print('\033[0;31;31m')
          
        return index_reponse, index_return, hits
    
    return parameters

@filter
def min_filter(opts):
    return opts.index(min(opts))

@filter
def max_filter(opts):
    return opts.index(max(opts))

@filter
def bi_filter(opt):
    r = modulo(1 - opt[0])

    if r < modulo(opt[0]):
        return 1
    return 0
   
    

def func_trainer(function):
    def parameters(self, w, lst, len_rate):
        for each in lst:
            i = self.types_of_answers.index(each[-1])
            function(w, each, len_rate, i)
    return parameters

@func_trainer
def trainer_1(function ,each, len_rate, i):
    function(each[:-1], len_rate=len_rate, value=0, st_index=i)
    function(each[:-1], len_rate=len_rate, value=1, st_index=i-1)  

@func_trainer
def trainer_bi(function ,each, len_rate, i):
    function(each[:-1], len_rate=len_rate, value=int(each[-1]), st_index=0)

class Dates():
    '''
        train_percentage é uma variável para eu setar a proporção entre a lista de teste e a 
        lista de treino

        shuffle_date setado como falso é util para fazer comparações e ver se o algoritmo tá 
        aprendendo ou não, mas ao mesmo tempo a ordem dos fatores afetam os pesos finais, essa 
        aleátoridade como ate mesmo ajudar o algoritmo a melhorar  
    '''
    def __init__(self, file_name, train_percentage=0.5, shuffle_date=False, min_selector=80):
        self.filter = min_filter
        self.trainer = trainer_1
        with open(FILE_DATES + file_name) as CsvFile:
            iris_lst = list(reader(CsvFile))
        
        # separando a lista para o treino do algoritmo e outra para testar a acuracia 
        self.train_list = []
        self.test_list = []

        # aproveitando para definir a quantidades de variáveis e quantidade pesos para usar
        self.qt_columns = len(iris_lst[0])
        self.qt_weights_per_types = self.qt_columns - 1
        
        # separando todas as variavéis, menos a primeira, já que é apenas os nomes das variáveis
        # não os valores
        lst_values = iris_lst[1:]

        # criando uma lista com maior valor e o menor de cada variável, para normalizar os dados  
        self.max_var = [lst_values[0][i] for i in range(0, self.qt_weights_per_types)]
        self.min_var =  self.max_var.copy()

        # usando um for simplês e usando filtros para tirar o menor valor e o maior
        for list_ in lst_values:
            for index in range(0, self.qt_weights_per_types):
                if float(list_[index]) > float(self.max_var[index]):
                    self.max_var[index] = float(list_[index])
                
                if float(list_[index]) < float(self.min_var[index]):
                    self.min_var[index] = float(list_[index])
        
        '''
        a vantagem de normalizar é 
        '''
        for list_ in lst_values:
            for index in range(0, self.qt_weights_per_types):
                list_[index] = ((float(list_[index]) - float(self.min_var[index])) / (float(self.max_var[index]) - float(self.min_var[index])))
            

        self.types_of_answers = sorted(list(set([x[-1] for x in iris_lst[1:].copy()])))
        self.qt_weights = len(self.types_of_answers)
    
        self.dates = dict(zip(self.types_of_answers, [[] for _ in self.types_of_answers]))
        for each in lst_values:
            self.dates[each[-1]].append(each)

        self.train_list = []
        self.test_list = []
        self.qt_columns = len(iris_lst[0])
        self.qt_weights_per_types = self.qt_columns - 1
        self.min_selector =  75

        for type in self.types_of_answers:
            if shuffle_date:
                shuffle(self.dates[type])
            
            list_ = self.dates[type]
            len_ = len(list_)
            qt_train = int(int(len_) * train_percentage)
            for each in range(0, qt_train):
                self.train_list.append(list_[each])

            for each in range(qt_train, len_):
                self.test_list.append(list_[each])

    def train(self, function, len_rate):
        list_shuffle = self.train_list.copy()
        if list_shuffle:
            shuffle(list_shuffle)
        
        self.trainer(self, function, list_shuffle, len_rate)
      
    def acc_rate(self, w, display=False):
        hits = 0  
        if display:
            print('==========================================================')  
        for pos, each in enumerate(self.test_list): 
            if display:
                print(f'{pos + 1}'.center(55))
            
            opts = list([modulo(w.result(x, each[:-1])) for x in range(self.qt_weights)])
            index_reponse, index_return, hits = self.filter(self, opts, each, hits)
                     
            if display:
                print(f'reposta verdadeira: {self.types_of_answers[index_reponse]}'.center(55))
                print(f'reposta gerada: {self.types_of_answers[index_return]}'.center(55))
                print('==========================================================') 
                print('\033[0;40;40m')
        if hits * 100 / len(self.test_list) > self.min_selector:
            self.save(w)
        if display: 
            print(f'{hits * 100 / len(self.test_list)}%, hits: {hits} attempts: {len(self.test_list)}')
        return hits * 100 / len(self.test_list)

    @staticmethod
    def save(w):
         with open('refined_weight.csv', 'w') as CsvFile:
                wt = writer(CsvFile)
                wt.writerow(w.bias)
                for each in w.lst_weights:
                    wt.writerow(each)

class DatesBi(Dates):
    def __init__(self, file_name, train_percentage=0.5, shuffle_date=False, min_selector=80):
        super().__init__(file_name, train_percentage, shuffle_date, min_selector)
        self.trainer = trainer_bi
        self.filter = bi_filter
        self.qt_weights = 1
    
    
def login_weight(w):
    with open('refined_weight.csv') as Csvfile:
        list_ = list(reader(Csvfile))
        w.bias = list_.pop(0)
        w.lst_weights = list_
    return w
       

  