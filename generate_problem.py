import numpy as np

def generate_problem(n, m):
    """
    生成一个 Prophet Matching 问题实例。
    每条边的分布类型随机选择（均匀分布、正态分布、长尾分布等）。
    
    参数:
    - n: 离线顶点数
    - m: 在线顶点数
    
    返回:
    - edge_distributions: 一个 n x m 的列表，每个元素是一个分布函数
    """
    edge_distributions = []
    for j in range(n):
        distributions = []
        for i in range(m):
            # 随机选择分布类型
            distribution_type = np.random.choice(["uniform", "normal", "pareto", "binomial"])
            
            if distribution_type == "uniform":
                # 均匀分布
                low = np.random.uniform(0, 0.5)
                high = np.random.uniform(0.5, 1)
                distributions.append(lambda low=low, high=high: np.random.uniform(low, high))
            
            elif distribution_type == "normal":
                # 正态分布
                mu = np.random.uniform(0.5, 1)  # 均值
                sigma = np.random.uniform(0.1, 0.3)  # 标准差
                distributions.append(lambda mu=mu, sigma=sigma: np.random.normal(mu, sigma))
            
            elif distribution_type == "pareto":
                # 长尾分布（Pareto 分布）
                alpha = np.random.uniform(1, 3)  # 形状参数
                scale = np.random.uniform(0.5, 1)  # 尺度参数
                distributions.append(lambda alpha=alpha, scale=scale: np.random.pareto(alpha) * scale)
            
            elif distribution_type == "binomial":
                # 二项分布
                n = np.random.randint(1, 10)
                p = np.random.uniform(0, 1)
                distributions.append(lambda n=n, p=p: np.random.binomial(n, p) / n)
        
        edge_distributions.append(distributions)
    return edge_distributions