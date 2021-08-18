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

def get_Kendall(lists, output='coef'):
    
    if len(lists)<2:
        raise ValueError("На вход должно быть подано минимум 2 списка!")
    
    n = [len(l) for l in lists]
    if not all(elem == n[0] for elem in n):
        raise ValueError("Списки должны быть одинаковой длины!")
        
    #Ранговая шкала
    if all(check_if_range_scale(elem) for elem in lists):
        
        cons = [get_cons(l) for l in lists]
        if all(len(elem) == 0 for elem in cons):
            m = len(lists)
            n1 = n[0]
            
            S = sum(
                    (sum(lists[j][i] for j in range(m))
                    -sum(lists[j][i] for j in range(m) for i in range(n1))/n1)**2 
                for i in range(n1))
            
            W = 12*S / (m**2 * (n1**3 - n1))
       
        else:
            
            m = len(lists)
            n1 = n[0]
            
            or_lists = [turn_into_range(l) for l in lists]
            
            cons_v = [list(get_cons(l).values()) for l in lists]
            
            T = [sum(len(cons_v[j][k])**3 - len(cons_v[j][k]) 
                        for k in range(len(cons_v[j]))) 
                         for j in range(m)]
            
            W = 12*sum((sum(lists[j][i] for j in range(m))
                        -sum(lists[j][i] for j in range(m) for i in range(n1))/n1)**2
                         for i in range(n1)) / (m**2 * (n1**3 - n1) - m* sum(T[j] for j in range(m)))

    #Количественная
    else:
        or_lists = [turn_into_range(l) for l in lists]
        
        cons_v = [list(get_cons(l).values()) for l in lists]
        
        if all(len(elem) == 0 for elem in cons_v):
            
            m = len(lists)
            n1 = n[0]
            
            S = sum(
                    (sum(lists[j][i] for j in range(m))
                    -sum(lists[j][i] for j in range(m) for i in range(n1))/n1)**2 
                for i in range(n1))
            
            W = 12*S / (m**2 * (n1**3 - n1))
            
        else:
            
            m = len(lists)
            n1 = n[0]
            
            cons_v = [list(get_cons(l).values()) for l in lists]
            
            T = [sum(len(cons_v[j][k])**3 - len(cons_v[j][k]) 
                        for k in range(len(cons_v[j]))) 
                         for j in range(m)]
            
            W = 12*sum((sum(lists[j][i] for j in range(m))
                        -sum(lists[j][i] for j in range(m) for i in range(n1))/n1)**2
                        for i in range(n1)) / (m**2 * (n1**3 - n1) - m* sum(T[j] for j in range(m)))
  

    #Спецификация вывода
    if output == 'coef':
        return W
    elif output == 't':
        return W*sqrt(n1 - 2)/sqrt(1-W**2 + 0.0000000001)
    elif output == 'conclusion':
        T = W*sqrt(n1 - 2)/sqrt(1-W**2 + 0.0000000001)
        value = t.ppf(0.95, 1)
        if T < value:
            print("Статистическая значимость наблюдаемой связи отсутствует с вероятностью 95%. табличное: ", value,
                  " расчётное: ", T)
        else:
            print("Наблюдается статистическая значимость связи с вероятностью 95%. табличное: ", value,
                  " расчётное: ", T)
    else:
        raise ValueError("Доступные опции вывода: coef, t, conclusion")
