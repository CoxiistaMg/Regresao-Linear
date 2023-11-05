from random import randint, random


class Weights:
    def __init__(self, qt_columns, qt_weights_per_columns) -> None:
        self.lst_weights = []
        self.bias = []
        self.qt_per_columns =  qt_weights_per_columns
        for index in range(qt_columns):
            self.lst_weights.append([])
            for _ in range(qt_weights_per_columns):
                self.lst_weights[index].append(random() * randint(0, 1))
            self.bias.append(randint(0, 10) * random())
        
    
    def update_weight(self, values=[3, 3, 1, 0], st_index=0, value=1, len_rate=0.01):
        weights = self.lst_weights[st_index]
    
        result = self.result(index=st_index, values=values)
        for index in range(len(weights)):
            weights[index] += len_rate * (values[index] * (value - result))

        self.bias[st_index] += len_rate * (value - result) 
    
    def result(self, index, values=[3, 3, 1, 0]):
        result = 0
     
        for i in range(self.qt_per_columns):
            result += self.lst_weights[index][i] * values[i]
       

        result += self.bias[index]
        return result
           
    def __str__(self) -> str:
        text = '-----------------------------------------------------------------'
        for pos, weights in enumerate(self.lst_weights):
            text += f'\nPesos {pos+1}\n'
            text += '\n'.join((str(x) for x in weights)) 
            text += '\n-----------------------------------------------------------------'
        return text
    
