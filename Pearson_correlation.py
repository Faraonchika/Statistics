from math import sqrt
from scipy.stats import t


def check_if_range_scale(l):
    n = len(l)
    mi = min(l)
    ma = max(l)
    return all(type(l[i]) == int for i in range(len(l))) and ma==n==l[-1] and mi==1==l[0]

def get_cons(list1):
    conectors = {}
    for i in list1:
        pos = [j for j, ltr in enumerate(list1) if ltr == i]
        if len(pos) > 1:
            conectors[i] = pos
    return conectors

def turn_into_range(list1):
    l1=list1[:]
    l1.sort()
    l2 = list(enumerate(l1))
    numbers = [l2[i][1] for i in range(len(l2))]
    positions = [l2[i][0] for i in range(len(l2))]
    
    conectors = get_cons(list1)
    
    output = []
    for i in list1:
        indx = numbers.index(i)
        output.append(positions[indx] + 1)
        if len(numbers) > 1:
            numbers = numbers[:indx] + numbers[indx+1:]
            positions = positions[:indx] + positions[indx+1:]
    
    for value in list(conectors.values()):
        length = len(value)
        acumulate = 0
        for pos in value:
            acumulate += output[pos]
        for pos in value:
            output[pos] = acumulate / length

    return output

def get_pirson(list1, list2, output='coef'):
    
    n1 = len(list1)
    n2 = len(list2)
    if n1 != n2:
        raise ValueError("Списки должны быть одинаковой длины!")
        
    #Ранговая шкала
    if(check_if_range_scale(list1) and check_if_range_scale(list2)):
        
        con1 = get_cons(list1)
        con2 = get_cons(list2)
        if len(con1) == 0 and len(con2) == 0:
            pirson = 1 - (6*sum((list1[i] - list2[i])**2 for i in range(n1)))/(n1*(n1**2 - 1))
       
        else:
            or_list1 = turn_into_range(list1)
            or_list2 = turn_into_range(list2)
            
            con1_v = list(con1.values())
            con2_v = list(con2.values())
            
            delta = 1/2 * sum(
                len(con1_v[q]) * (len(con1_v[q])**2 - 1) for q in range(len(con1))) + 1/2 * sum(
                len(con2_v[f]) * (len(con2_v[f])**2 - 1) for f in range(len(con2)))
            
            pirson = 1 - sum(
                (or_list1[i] - (n1 + 1)/2) * (or_list2[i] - (n1 + 1)/2) for i in range(n1)) / (n1 * (n1**2 - 1) - delta)
            
            

    #Количественная
    else:
        or_list1 = turn_into_range(list1)
        or_list2 = turn_into_range(list2)
        

        con1 = get_cons(list1)
        con2 = get_cons(list2)
        
        if len(con1) == 0 and len(con2) == 0:
            pirson = 1 - (6*sum((or_list1[i] - or_list2[i])**2 for i in range(n1)))/(n1*(n1**2 - 1))
        else:
            con1_v = list(con1.values())
            con2_v = list(con2.values())
            
            delta = 1/2 * sum(
                len(con1_v[q]) * (len(con1_v[q])**2 - 1) for q in range(len(con1))) + 1/2 * sum(
                len(con2_v[f]) * (len(con2_v[f])**2 - 1) for f in range(len(con2)))
            
            pirson = 1 -sum(
                (or_list1[i] - (n1 + 1)/2) * (or_list2[i] - (n1 + 1)/2) for i in range(n1)) / (n1 * (n1**2 - 1) - delta)
  

    #Спецификация вывода
    if output == 'coef':
        return pirson
    elif output == 't':
        return pirson*sqrt(n1 - 2)/sqrt(1-pirson**2 + 0.0000000001)
    elif output == 'conclusion':
        T = pirson*sqrt(n1 - 2)/sqrt(1-pirson**2 + 0.0000000001)
        value = t.ppf(0.95, n1 - 2)
        if T < value:
            print("Статистическая значимость наблюдаемой связи отсутствует с вероятностью 95%. табличное: ", value,
                  " расчётное: ", T)
        else:
            print("Наблюдается статистическая значимость связи с вероятностью 95%. табличное: ", value,
                  " расчётное: ", T)
    else:
        raise ValueError("Доступные опции вывода: coef, t, conclusion")
