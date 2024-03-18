from policytree import *
import copy

        
def createPolicy(policy_string):
        assert type(policy_string) == str, "invalid type for policy_string"
        parser = PolicyParser()        
        policy_obj = parser.parse(policy_string)
        _dictCount, _dictLabel = {}, {}
        parser.findDuplicates(policy_obj, _dictCount)
        for i in _dictCount.keys(): 
            if _dictCount[ i ] > 1: _dictLabel[ i ] = 0
        parser.labelDuplicates(policy_obj, _dictLabel)
        print("policy_obj: ", policy_obj)
        return policy_obj
    

def LSSS(tree):
    counter = 1
    LSSSM = {}
    #ro = []
    tree.getVector().append(1)
    #print("vector:", tree.getVector())
    def recur(tree):
        nonlocal LSSSM
        nonlocal counter
        #print("counter:", counter)
        node = tree.getNodeType()
        if(node == OpType.AND):
            tree.getLeft().vector_pad_to(counter)
            #print("vector:", tree.getLeft().getVector())
            leftve = tree.getLeft().getVector()
            leftve.append(-1)
            
            rightve = tree.getRight().getVector()
            for i in tree.getVector():
                rightve.append(i)
            tree.getRight().vector_pad_to(counter)
            rightve = tree.getRight().getVector()
            rightve.append(1)
            counter += 1
            #print("Lvector:", tree.getLeft().getVector())
            #print("Rvector:", tree.getRight().getVector())
            recur(tree.getLeft())
            recur(tree.getRight())
        elif(node == OpType.OR):
            rightve = tree.getRight().getVector()
            leftve = tree.getLeft().getVector()
            for i in tree.getVector():
                rightve.append(i)
                leftve.append(i)
            #print("Lvector:", tree.getLeft().getVector())
            #print("Rvector:", tree.getRight().getVector())
            recur(tree.getLeft())
            recur(tree.getRight())
        elif(node == OpType.ATTR):
            attr = tree.getAttributeAndIndex()
            LSSSM[attr] = copy.deepcopy(tree.getVector())
            return
        else: return None
    recur(tree)
    for key in LSSSM:
        for i in range(counter - len(LSSSM[key])):
            LSSSM[key].append(0)
    return LSSSM


if __name__ == '__main__':
    #test 
    secret = 3
    policy_str = "(E and (((A and B) or (C and D)) or ((A or B) and (C or D))))"
    policy = createPolicy(policy_str)

    """coeff = getCoefficients(policy)
    
    print(coeff)
    print(calculateSharesDict(secret, policy))"""
    print(LSSS(policy))