from tools import dates, weights
dates.FILE_DATES = 'tools/files/'

def lr(file_name):
    date = dates.DatesBi(file_name, train_percentage=0.5)
    w = weights.Weights(date.qt_weights, date.qt_weights_per_types)

    try:
        
        with open('refined_weight.csv', 'r') as CsvFile:
            w = dates.login_weight(w)
            w.lst_weights = [[float(y) for y in x] for x in w.lst_weights]
            w.bias = [float(x) for x in w.bias]
            date.min_selector = date.acc_rate(w, True)
            min_selector = date.min_selector
        
            date.acc_rate(w, True)

            for _ in range(0, 1000):
                date = dates.DatesBi(file_name, train_percentage=0.01)
                date.min_selector = min_selector
                date.train(w.update_weight, 0.000000)
                result = date.acc_rate(w, False)
                if date.min_selector < result:
                    min_selector = result
     
 



    except:
        date.train(w.update_weight, 0.3)
    date.acc_rate(w, True)
    
def lor(file_name):
    pass

lr('diabetes.csv')

