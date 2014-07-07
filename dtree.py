# coding=utf-8

from collections import defaultdict
from math import log


def test():
    import urllib2
    example = []  # ['slashdot', 'USA', 'yes', '18', 'None']
    content = urllib2.urlopen(
        'http://kiwitobes.com/tree/decision_tree_example.txt').read()
    for item in content.split('\n'):
        print item
        lst = item.split('\t')
        lst[3] = int(lst[3])
        example.append(lst)
    set1, set2 = divideset(example, 3, 21)
    tree = buildtree(example)
    printtree(tree)


def uniquecounts(rows):
    results = defaultdict(int)
    for row in rows:
        results[row[-1]] += 1
    return results


def entropy(rows):
    '''计算信息熵'''
    log2 = lambda x: log(x) / log(2)
    results = uniquecounts(rows)
    ent = 0.0
    rowslen = len(rows)
    for key, value in results.items():
        p = float(value) / rowslen
        ent = ent - p * log2(p)
    return ent


def divideset(rows, column, value):
    if isinstance(value, int) or isinstance(value, float):
        set1 = filter(lambda row: row[column] >= value, rows)
    else:
        set1 = filter(lambda row: row[column] == value, rows)
    set2 = [row for row in rows if row not in set1]
    return (set1, set2)


def buildtree(rows, scoref=entropy):
    if not rows:
        return DecisionNode()
    current_score = scoref(rows)
    best_gain = 0.0
    best_criteria = None
    best_sets = None
    column_count = len(rows[0]) - 1
    for col in range(0, column_count):
        column_values = set(row[col] for row in rows)
        for value in column_values:
            set1, set2 = divideset(rows, col, value)
            # 信息增益
            p = float(len(set1)) / len(rows)
            gain = current_score - p * scoref(set1) - (1 - p) * scoref(set2)
            if gain > best_gain and set1 and set2:
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (set1, set2)
        # 创建分支
    if best_gain > 0:
        trueBranch = buildtree(best_sets[0])
        falseBranch = buildtree(best_sets[1])
        return DecisionNode(col=best_criteria[0], value=best_criteria[1],
                            tb=trueBranch, fb=falseBranch)
    else:
        return DecisionNode(results=uniquecounts(rows))


def printtree(tree):
    if tree.results:
        print str(tree.results)
    else:
        print tree.col, tree.value
        printtree(tree.tb)
        printtree(tree.fb)


class DecisionNode:

    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb


if __name__ == '__main__':
    test()
