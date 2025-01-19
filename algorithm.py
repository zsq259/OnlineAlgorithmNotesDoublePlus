import numpy as np
from scipy.optimize import linear_sum_assignment

def compute_p_j(edge_distributions, n, m, num_samples=1000):
    """
    通过重复采样边权分布，计算每个离线顶点 j 的 p_j。
    
    参数:
    - edge_distributions: 一个 n x m 的列表，每个元素是一个分布函数
    - n: 离线顶点数
    - m: 在线顶点数
    - num_samples: 采样次数
    
    返回:
    - p_j: 一个长度为 n 的列表，表示每个离线顶点的价格
    """
    p_j = np.zeros(n)
    for _ in range(num_samples):
        # 采样边权
        edge_weights = np.zeros((n, m))
        for j in range(n):
            for i in range(m):
                edge_weights[j][i] = edge_distributions[j][i]()
        
        # 计算最大匹配
        row_ind, col_ind = linear_sum_assignment(-edge_weights)
        max_matching_value = edge_weights[row_ind, col_ind].sum()
        
        # 累加每个离线顶点的贡献
        for j in row_ind:
            p_j[j] += edge_weights[j][col_ind[row_ind.tolist().index(j)]]
    
    # 计算均值并设置 p_j
    p_j = 0.5 * (p_j / num_samples)
    return p_j

def run_algorithm(edge_distributions, p_j, n, m):
    """
    模拟在线算法的运行，并记录所有在线顶点到达后的实际边权。
    
    参数:
    - edge_distributions: 一个 n x m 的列表，每个元素是一个分布函数
    - p_j: 一个长度为 n 的列表，表示每个离线顶点的价格
    - n: 离线顶点数
    - m: 在线顶点数
    
    返回:
    - ALG: 在线算法的总收益
    - actual_edge_weights: 一个 n x m 的矩阵，表示所有在线顶点到达后的实际边权
    """
    matched = set()  # 记录已匹配的离线顶点
    ALG = np.float128(0)  # 在线算法的总收益
    actual_edge_weights = np.zeros((n, m))  # 记录实际边权
    matches = [-1] * m
    
    for i in range(m):
        # 采样当前在线顶点的边权
        for j in range(n):
            actual_edge_weights[j][i] = edge_distributions[j][i]()
        
        # 选择使效用最大的离线顶点
        utilities = []
        for j in range(n):
            if j not in matched:
                utilities.append(max(actual_edge_weights[j][i] - p_j[j], 0))
            else:
                utilities.append(0)
        if utilities:
            best_j = np.argmax(utilities)
            if utilities[best_j] > 0:
                matched.add(best_j)
                matches[i] = best_j
                ALG += np.float128(actual_edge_weights[best_j][i])
    
    row_ind, col_ind = linear_sum_assignment(-actual_edge_weights)
    OPT = np.float128(0)
    for i in range(len(row_ind)):
        OPT += np.float128(actual_edge_weights[row_ind[i]][col_ind[i]])
    if ALG > OPT:
        print("ALG:", ALG, "OPT:", OPT)
        for i in range(len(matches)):
            if matches[i] != -1:
                print(matches[i], i, actual_edge_weights[matches[i]][i])
        print(matches)
        for i in range(len(row_ind)):
            print(row_ind[i], col_ind[i], actual_edge_weights[row_ind[i]][col_ind[i]])
        
        raise ValueError("ALG > OPT")
    
    return ALG, OPT