from collections import namedtuple
import math
Item = namedtuple("Item", ['index', 'value', 'weight','val_ratio'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    optimality_flg = 0
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()

    item_count = int(firstLine[0])
    capacity = int(firstLine[1])


    #global items
    items_original=[]


    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items_original.append(Item(i-1, int(parts[0]), int(parts[1]),round(int(parts[0])/int(parts[1]),10)))

    #print(items)

    global Best

    #---------------------------Get feasible bound ------------------------
    items2 = sorted(items_original,key= lambda x : (getattr(x,'val_ratio'),getattr(x,'value')), reverse=True)
    weight2 = []
    for i in range(0,len(items2)):
        weight2.append(items2[i][2])

    value = 0
    weight = 0
    taken = [0]*len(items_original)
    #temp = []

    for i in range(0,len(items2)):
        item = items2[i]
        if weight + item.weight <= capacity:
            taken[i] = 1
            value += item.value
            weight += item.weight
            #temp.append(item.weight)
            #print("selected temp :",item.weight)
        else :
            taken[i] = 0
            #temp.append(item.weight)


    Best=[value,taken]

    #----------------------------------------------------------------------

    # for i in range(len(items2)-1,-1,-1):
    #     if(items2[i][2]>capacity):
    #         items2.pop(i)
    #Best = [20,[0,0,1,1]]
    #print(taken)
    #print(Best)
    #print(capacity)
    #print(weight)
    #print(temp)
    #print(items2)
    #print(capacity)
    #[item for item in a if item[0] == 1]



    def BB(Var,Cap,Val,lb,items,Best):
        #check for capacity available
        #print(Var)
        if(item_count<=40):
            if(len(Var)==len(items)):
                #print("here")
                return

            elif(items[len(Var)][2]>Cap):
                #print("here2")
                Var_3 = Var.copy()
                Var_3.append(0)
                BB(Var_3,Cap,Val,lb,items,Best)

            elif(lb<=Best[0]):
                #print("here3")
                return
            elif(len(Var)==len(items)):
                #print("here4")
                return
            else:
                #print("here5")

                for i in [1,0]:

                    Var_2 = Var.copy()
                    Cap_2 = Cap
                    Val_2 = Val
                    lb_2 = lb
                    if (i==0):
                        #let's append right which is zero cases fisrt

                        Var_2.append(0)

                        lb_2 = sum(Var_2[i]*[item[1] for item in items][i] for i in range(0,len(Var_2)))

                        if(item_count>40):
                            weight = Cap - items[len(Var_2)-1][2]

                            for item in items[len(Var_2):len(items)]:
                                if(weight!=0):
                                    if  item.weight <= weight:
                                        lb_2 = item.value + lb_2
                                        weight = weight - item.weight
                                    else:
                                        lb_2 = (weight/ item.weight)*item.value + lb_2
                                        weight = 0
                        else:
                            lb_2 = lb_2 +  sum([item[1] for item in items][i] for i in range(len(Var_2),len(items)))
                        Cap_2 = Cap
                        Val_2 = Val

                    else :
                        #let's work on the left branch whis is one
                        Var_2.append(1)
                        lb_2 = sum(Var_2[i]*[item[1] for item in items][i] for i in range(0,len(Var_2)))
                        if(item_count>40):

                            weight = Cap - items[len(Var_2)-1][2]
                            for item in items[len(Var_2):len(items)]:
                                if(weight!=0):
                                    if  item.weight <= weight:
                                        lb_2 = item.value + lb_2
                                        weight = weight - item.weight
                                    else:
                                        lb_2 = (weight/ item.weight)*item.value + lb_2
                                        weight = 0
                        else:
                            lb_2 = lb_2 +  sum([item[1] for item in items][i] for i in range(len(Var_2),len(items)))
                        #print(Cap_2)
                        Cap_2 = Cap - items[len(Var_2)-1][2]
                        Val_2 = Val + items[len(Var_2)-1][1]

                    if(len(Var_2)==len(items)):
                        feasible = sum(Var_2[i]*[item[1] for item in items][i] for i in range(len(Var_2)))
                        if(feasible>Best[0]):
                            Best[0] = feasible
                            Best[1] = Var_2

                    BB(Var_2,Cap_2,Val_2,lb_2,items,Best)

        return Best
        #print(Best)
        #print(capacity)
        #sum(Var_2[i]*[item[1] for item in items][i] for i in range(0,len(Var_2)))
        #print(sum(Best[0]*[item[2] for item in items2[j] for j in range(0,len(Best))]))


    result = BB([],capacity,0,sum([item[1] for item in items_original][i] for i in range(0,len(items_original))),items2,Best)
    #print(result)
    #print(capacity)
    #used_capacity = sum(result[1][j]*[item[2] for item in items2][j] for j in range(0,len(result[1])))
    #print(used_capacity)
    #print(capacity-used_capacity)
    #print("real---")
    final_var_list = [0]*len(items_original)
    for i in range(0,len(items2)):
        #print(items2[i].index)
        final_var_list[items2[i].index] = result[1][i]
    #print(final_var_list)
    #print(sum(final_var_list[j]*[item[1] for item in items_original][j] for j in range(0,len(final_var_list))))

    # prepare the solution in the specified output format

    output_data = str(result[0]) + ' ' + str(optimality_flg) + '\n'
    output_data += ' '.join(map(str, final_var_list))

    return output_data

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
