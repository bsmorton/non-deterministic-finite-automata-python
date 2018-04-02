import goody

def read_ndfa(file : open) -> {str:{str:{str}}}:
    d={}
    for line in file:
        r=line.strip('\n').split(';')
        d.update({r[0]:{r[num]:set() for num in range(len(r[1:])) if num%2==1}})
        for num in range(len(r[1:])):
            if num%2==1:
                d[r[0]][r[num]].add(r[num+1])
    return d


def ndfa_as_str(ndfa : {str:{str:{str}}}) -> str:
   return ''.join(sorted(['  '+item+' transitions: '+str(sorted([(item2,sorted([item3 for item3 in ndfa[item][item2]])) for item2 in ndfa[item].keys()]))+'\n' for item in ndfa.keys()]))

       
def process(ndfa : {str:{str:{str}}}, state : str, inputs : [str]) -> [None]:
    l=[state]
    current_state=[state]
    for item1 in inputs:
        temp_set=set()
        for item2 in current_state:
            try:
                temp_set=temp_set.union(ndfa[item2][item1])
            except:
                pass
            
        l.append((item1,temp_set.copy()))
        if len(temp_set)==0:
            break
        current_state=[]
        while len(temp_set)!=0:
            current_state.append(temp_set.pop())    
    return l


def interpret(result : [None]) -> str:
    return 'Start state = '+result[0]+'\n'+''.join(['  Input = '+item[0]+'; new possible states = '+str(sorted(list(item[1])))+'\n' for item in result[1:] ])+'Stop state(s) = '+str(sorted(list(result[-1][1])))+'\n'





if __name__ == '__main__':
    # Write script here
    file=input('Enter the name of any file with a non-deterministic finite automaton: ')
    d1=read_ndfa(open(file))
    print()
    print("Non-Deterministic Finite Automaton's Description")
    print(ndfa_as_str(d1))
    print()
    d2=input('Enter the name of any file with the start-state and inputs: ')
    for line in open(d2):
        print()
        print('Starting new simulation')
        temp=line.strip('\n').split(';')
        print(interpret(process(d1, temp[0], temp[1:])))          
              
    # For running batch self-tests
    print()
#    import driver
#    driver.default_file_name = "bsc4.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
#    driver.driver()
