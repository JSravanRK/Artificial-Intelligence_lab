def load_data(f):
    a=[]
    with open(f,'r') as file:
        for line in file:
            a.append(line.strip().split())
    return a

def calculate_freq(a):
    b={}
    for row in a[1:]:
        ec,it,ma,intern=row
        key=(ec,it,ma)
        if key not in b:
            b[key]={'q':0,'nq':0}
        if intern=='1':
            b[key]['q']+=1
        else:
            b[key]['nq']+=1
    return b

def calculate_cpts(b):
    total=sum(v['q']+v['nq'] for v in b.values())
    c={}
    for key,v in b.items():
        q=v['q']
        nq=v['nq']
        c[key]={
            'P(Q|G)':q/total,
            'P(NQ|G)':nq/total
        }
    return c

def predict_grade(c,key1,key2,key3):
    k=(key1,key2,key3)
    if k in c:
        return c[k]
    else:
        return {'P(Q|G)':0,'P(NQ|G)':0}

def evaluate_model(a,c):
    correct=0
    total=len(a)-1
    for row in a[1:]:
        ec,it,ma,intern=row
        p=predict_grade(c,ec,it,ma)
        if (intern=='1' and p['P(Q|G)']>p['P(NQ|G)']) or \
           (intern=='0' and p['P(NQ|G)']>p['P(Q|G)']):
            correct+=1
    return correct/total if total>0 else 0

file_name='2020_bn_nb_data.txt'
a=load_data(file_name)
b=calculate_freq(a)
c=calculate_cpts(b)
ec_grade='DD'
it_grade='CC'
ma_grade='CD'
predicted_probs=predict_grade(c,ec_grade,it_grade,ma_grade)
print(f'Probabilities for PH100 given grades: {predicted_probs}')
accuracy=evaluate_model(a,c)
print(f'Accuracy of the Naive Bayes classifier: {accuracy:.2f}')
