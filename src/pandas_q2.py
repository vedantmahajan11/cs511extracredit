'''
    Author: University of Illinois at Urbana Champaign
    DateTime: 2023-11-05 10:42:47
    FilePath: src/pandas_q2.py
    Description:
'''

import pandas as pd

from src.difference import Difference
from src.report import get_file, report


@report
def pandas_q2(data_file: str, pattern_file: str) -> str:
    data = pd.read_csv(data_file, sep=' ', header=None, 
                      names=['src', 'dst', 'src_label', 'dst_label', 'edge_label'])
    pattern = pd.read_csv(pattern_file, sep=' ', header=None, 
                         names=['src', 'dst', 'src_label', 'dst_label', 'edge_label'])
    
    pattern_vertices = sorted(list(set(pattern['src'].tolist() + pattern['dst'].tolist())))
    
    edge_relations = []
    
    for _, row in pattern.iterrows():
        matches = data[
            (data['src_label'] == row['src_label']) & 
            (data['dst_label'] == row['dst_label']) & 
            (data['edge_label'] == row['edge_label'])
        ]
        if not matches.empty:
            relation = matches[['src', 'dst']].copy()
            relation.columns = [f'u{row["src"]}', f'u{row["dst"]}']
            edge_relations.append(relation)
    
    if edge_relations:
        result = edge_relations[0]
        for relation in edge_relations[1:]:
            result = pd.merge(result, relation, how='inner')
            
        columns = [f'u{i}' for i in range(len(pattern_vertices))]
        result = result.reindex(columns=columns)
    else:
        result = pd.DataFrame(columns=[f'u{i}' for i in range(len(pattern_vertices))])
    
    result = result.sort_values(by=list(result.columns))
    result = result.drop_duplicates()
    
    output_file = 'out/pandas_q2.csv'
    result.to_csv(output_file, index=False, header=False)
    
    return output_file

def test(data, pattern, expect) -> int:
    # import the logger to output message
    import logging
    logger = logging.getLogger()
    data = get_file('data', data)
    pattern = get_file('pattern', pattern)
    expect = get_file('expect', expect)


    # run the test
    print("**************begin pandas_q2 test**************")
    diff = Difference(pandas_q2(data, pattern), expect)
    try:
        assert(diff.match)
        print('*******************pass*******************')
        return 20
    except Exception as e:
        logger.error("Exception Occurred:" + str(e))
        print('*******************fail*******************')
        print(diff.actual)
        print(diff.expect)
        return 0


if __name__ == "__main__":
    data = 'data/1.txt'
    pattern = 'pattern/2.txt'
    expect = 'expect/d1-p2.txt'
    test(data, pattern, expect)
