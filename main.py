# Alireza Moradi 

import itertools

def compBinary(s1,s2):
    count = 0
    pos = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            count+=1
            pos = i
    if count == 1:
        return True, pos
    else:
        return False, None


def compBinarySame(term,number):
    for i in range(len(term)):
        if term[i] != '-':
            if term[i] != number[i]:
                return False

    return True


def combinePairs(group, unchecked):
    l = len(group) -1

    check_list = []

    next_group = [[] for x in range(l)]

    for i in range(l):
        for elem1 in group[i]:
            for elem2 in group[i+1]:
                b, pos = compBinary(elem1, elem2)
                if b == True:
                    check_list.append(elem1)
                    check_list.append(elem2)
                    new_elem = list(elem1)
                    new_elem[pos] = '-'
                    new_elem = "".join(new_elem)
                    next_group[i].append(new_elem)
    for i in group:
        for j in i:
            if j not in check_list:
                unchecked.append(j)

    return next_group, unchecked


def remove_redundant(group):
    new_group = []
    for j in group:
        new=[]
        for i in j:
            if i not in new:
                new.append(i)
        new_group.append(new)
    return new_group


def remove_redundant_list(list):
    new_list = []
    for i in list:
        if i not in new_list:
            new_list.append(i)
    return new_list


def check_empty(group):

    if len(group) == 0:
        return True

    else:
        count = 0
        for i in group:
            if i:
                count+=1
        if count == 0:
            return True
    return False


def find_prime(Chart):
    prime = []
    for col in range(len(Chart[0])):
        count = 0
        pos = 0
        for row in range(len(Chart)):
            if Chart[row][col] == 1:
                count += 1
                pos = row

        if count == 1:
            prime.append(pos)

    return prime

def check_all_zero(Chart):
    for i in Chart:
        for j in i:
            if j != 0:
                return False
    return True

def find_max(l):
    max = -1
    index = 0
    for i in range(len(l)):
        if l[i] > max:
            max = l[i]
            index = i
    return index

def multiplication(list1, list2):
    list_result = []
    if len(list1) == 0 and len(list2)== 0:
        return list_result
    elif len(list1)==0:
        return list2
    elif len(list2)==0:
        return list1

    else:
        for i in list1:
            for j in list2:
                if i == j:
                    list_result.append(i)
                else:
                    list_result.append(list(set(i+j)))

        list_result.sort()
        return list(list_result for list_result,_ in itertools.groupby(list_result))

def petrick_method(Chart):
    P = []
    for col in range(len(Chart[0])):
        p =[]
        for row in range(len(Chart)):
            if Chart[row][col] == 1:
                p.append([row])
        P.append(p)
    for l in range(len(P)-1):
        P[l+1] = multiplication(P[l],P[l+1])

    P = sorted(P[len(P)-1],key=len)
    final = []
    min=len(P[0])
    for i in P:
        if len(i) == min:
            final.append(i)
        else:
            break
    return final

def find_minimum_cost(Chart, unchecked):
    P_final = []
    essential_prime = find_prime(Chart)
    essential_prime = remove_redundant_list(essential_prime)

    if len(essential_prime)>0:
        s = ''
        for i in range(len(unchecked)):
            for j in essential_prime:
                if j == i:
                    s= s+binary_to_letter(unchecked[i])+' , '

    for i in range(len(essential_prime)):
        for col in range(len(Chart[0])):
            if Chart[essential_prime[i]][col] == 1:
                for row in range(len(Chart)):
                    Chart[row][col] = 0

    if check_all_zero(Chart) == True:
        P_final = [essential_prime]
    else:
        P = petrick_method(Chart)

      

        P_cost = []
        for prime in P:
            count = 0
            for i in range(len(unchecked)):
                for j in prime:
                    if j == i:
                        count = count+ cal_efficient(unchecked[i])
            P_cost.append(count)


        for i in range(len(P_cost)):
            if P_cost[i] == min(P_cost):
                P_final.append(P[i])

        for i in P_final:
            for j in essential_prime:
                if j not in i:
                    i.append(j)

    return P_final

def cal_efficient(s):
    count = 0
    for i in range(len(s)):
        if s[i] != '-':
            count+=1

    return count

def binary_to_letter(s):
    out = ''
    c = 'a'
    more = False
    n = 0
    for i in range(len(s)):
        if more == False:
            if s[i] == '1':
                out = out + c
            elif s[i] == '0':
                out = out + c+'\''

        if more == True:
            if s[i] == '1':
                out = out + c + str(n)
            elif s[i] == '0':
                out = out + c + str(n) + '\''
            n+=1
        if c=='z' and more == False:
            c = 'A'
        elif c=='Z':
            c = 'a'
            more = True

        elif more == False:
            c = chr(ord(c)+1)
    return out



def main():
    n_var = int(raw_input("Enter the number of variables: "))
    minterms = raw_input("Enter the minterms (example: 2 3 6 7) : ")
    a = minterms.split()
    a = map(int, a)

    group = [[] for x in range(n_var+1)]

    for i in range(len(a)):
        a[i] = bin(a[i])[2:]
        if len(a[i]) < n_var:
            for j in range(n_var - len(a[i])):
                a[i] = '0'+ a[i]
        elif len(a[i]) > n_var:
            print '\nError : Choose the correct number of variables\n'
            return
        index = a[i].count('1')
        group[index].append(a[i])


    all_group=[]
    unchecked = []
    while check_empty(group) == False:
        all_group.append(group)
        next_group, unchecked = combinePairs(group,unchecked)
        group = remove_redundant(next_group)



    Chart = [[0 for x in range(len(a))] for x in range(len(unchecked))]

    for i in range(len(a)):
        for j in range (len(unchecked)):
            if compBinarySame(unchecked[j], a[i]):
               Chart[j][i] = 1

    primes = find_minimum_cost(Chart, unchecked)
    primes = remove_redundant(primes)


    print "Simplified Equation\n"

    for prime in primes:
        s=''
        for i in range(len(unchecked)):
            for j in prime:
                if j == i:
                    s= s+binary_to_letter(unchecked[i])+' + '
        print s[:(len(s)-3)]



if __name__ == "__main__":
    main()
    A = raw_input("\nPress Enter to Quit")