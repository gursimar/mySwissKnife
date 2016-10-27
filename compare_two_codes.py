import pandas as pd
import difflib

def compareCode(code1, code2):
    #print code1
    #print code2

    ## Get code lines after removing stray chars
    cl1 = code1.split('\n')
    cl2 = code2.split('\n')

    # strip \r \t etc
    cl1 = [i.strip() for i in cl1]
    cl2 = [i.strip() for i in cl2]

    # remove empty strings
    cl1 = [i for i in cl1 if i]
    cl2 = [i for i in cl2 if i]

    ## Take set difference of code lines
    diff1_2 = [i for i in cl1 if i not in cl2]
    diff2_1 = [i for i in cl2 if i not in cl1]

    ## comapare line by line
    diffobj = difflib.unified_diff(cl1, cl2)
    plus = []
    minus = []
    for line in diffobj:

        if line == '--- \n' or line == '+++ \n':
            pass
        elif line.startswith('+'):
            plus.append('`'+line)
        elif line.startswith('-'):
            minus.append('`'+line)
        else:
            pass

    result = {
        'initial': code1,
        'final': code2,
        'diff1_2': '\n'.join(diff1_2),
        'diff2_1':'\n'.join(diff2_1),
        'plus': '\n'.join(plus),
        'minus': '\n'.join(minus)
    }
    return result

if __name__ == '__main__':
    data = pd.DataFrame.from_csv('./data/codes.csv', index_col = None)
    results = []
    for index, row in data.iterrows():
        results.append(compareCode(row['initial'], row['final']))

    result_df = pd.DataFrame(results)
    result_df.to_csv('./results/code_diff.csv')



