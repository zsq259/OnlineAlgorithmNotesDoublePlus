import os
import matplotlib.pyplot as plt
import seaborn as sns

def ensure_dir(directory):
    """确保目录存在，如果不存在则创建。"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def plot_competitive_ratio_trend(n_values, m_values, competitive_ratios, save_dir="plots"):
    """
    绘制竞争比随参数变化的趋势图，并保存到本地。
    
    参数:
    - n_values: 离线顶点数的列表。
    - m_values: 在线顶点数的列表。
    - competitive_ratios: 竞争比的二维列表，competitive_ratios[i][j] 对应 n_values[i] 和 m_values[j]。
    - save_dir: 保存图表的目录。
    """
    ensure_dir(save_dir)
    plt.figure(figsize=(10, 6))
    for i, n in enumerate(n_values):
        plt.plot(m_values, competitive_ratios[i], label=f"n={n}")
    plt.xlabel("Online Vertices (m)")
    plt.ylabel("Competitive Ratio")
    plt.title("Competitive Ratio vs Online Vertices (m) for Different n")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(save_dir, "competitive_ratio_trend.png"))
    plt.close()

def plot_competitive_ratio_distribution(competitive_ratios, save_dir="plots"):
    """
    绘制竞争比的分布图（直方图），并保存到本地。
    
    参数:
    - competitive_ratios: 竞争比的列表。
    - save_dir: 保存图表的目录。
    """
    ensure_dir(save_dir)
    plt.figure(figsize=(10, 6))
    plt.hist(competitive_ratios, bins=20, edgecolor='black')
    plt.xlabel("Competitive Ratio")
    plt.ylabel("Frequency")
    plt.title("Distribution of Competitive Ratio")
    plt.grid(True)
    plt.savefig(os.path.join(save_dir, "competitive_ratio_distribution.png"))
    plt.close()

def plot_alg_vs_opt(alg_values, opt_values, save_dir="plots"):
    """
    绘制算法收益与离线最大匹配的对比图（散点图），并保存到本地。
    
    参数:
    - alg_values: 在线算法收益的列表。
    - opt_values: 离线最大匹配的列表。
    - save_dir: 保存图表的目录。
    """
    ensure_dir(save_dir)
    plt.figure(figsize=(10, 6))
    plt.scatter(opt_values, alg_values, alpha=0.5)
    plt.plot([min(opt_values), max(opt_values)], [min(opt_values), max(opt_values)], color='red', linestyle='--', label="ALG = OPT")
    plt.xlabel("Offline OPT")
    plt.ylabel("Online ALG")
    plt.title("Online ALG vs Offline OPT")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(save_dir, "alg_vs_opt.png"))
    plt.close()

def plot_parameter_sensitivity(n_values, m_values, competitive_ratios, save_dir="plots"):
    """
    绘制参数敏感性分析图（热力图），并保存到本地。
    
    参数:
    - n_values: 离线顶点数的列表。
    - m_values: 在线顶点数的列表。
    - competitive_ratios: 竞争比的二维列表，competitive_ratios[i][j] 对应 n_values[i] 和 m_values[j]。
    - save_dir: 保存图表的目录。
    """
    ensure_dir(save_dir)
    plt.figure(figsize=(10, 6))
    sns.heatmap(competitive_ratios, annot=True, xticklabels=m_values, yticklabels=n_values, cmap="YlGnBu")
    plt.xlabel("Online Vertices (m)")
    plt.ylabel("Offline Vertices (n)")
    plt.title("Parameter Sensitivity Analysis")
    plt.savefig(os.path.join(save_dir, "parameter_sensitivity.png"))
    plt.close()