from generate_problem import generate_problem
from algorithm import compute_p_j, run_algorithm
from visualization import (
    plot_competitive_ratio_trend,
    plot_competitive_ratio_distribution,
    plot_alg_vs_opt,
    plot_parameter_sensitivity,
)
import numpy as np

def main():
    # 参数设置
    n_values = [5, 10, 15, 20, 25, 30]  # 离线顶点数
    m_values = [5, 10, 15, 20, 25, 30]  # 在线顶点数
    num_samples = 1000  # 计算 p_j 的采样次数
    num_trials = 10000  # 运行算法的次数
    save_dir = "plots"  # 保存图表的目录

    # 存储每组 n, m 的竞争比均值
    competitive_ratio_means = np.zeros((len(n_values), len(m_values)))

    # 存储所有实验的竞争比
    all_competitive_ratios = []

    # 存储所有实验的 ALG 和 OPT
    all_alg_values = []
    all_opt_values = []

    # 遍历每组 n, m
    for i, n in enumerate(n_values):
        for j, m in enumerate(m_values):
            print(f"Running experiments for n={n}, m={m}...")

            # Step 1: 生成问题
            edge_distributions = generate_problem(n, m)

            # Step 2: 计算 p_j
            p_j = compute_p_j(edge_distributions, n, m, num_samples)

            # Step 3: 多次运行在线算法并记录结果
            competitive_ratios = []
            alg_values = []
            opt_values = []

            for trial in range(num_trials):
                # 运行在线算法
                ALG, OPT = run_algorithm(edge_distributions, p_j, n, m)
                alg_values.append(ALG)
                opt_values.append(OPT)

                # 计算竞争比
                if OPT > 0:
                    competitive_ratio = ALG / OPT
                    competitive_ratios.append(competitive_ratio)
                else:
                    raise ValueError("离线最大匹配 OPT 为 0")

                if OPT < ALG:
                    print("ALG:", ALG, "OPT:", OPT)
                    raise ValueError("ALG > OPT")

            # 计算竞争比均值
            competitive_ratio_means[i][j] = np.mean(competitive_ratios)

            # 记录所有实验的竞争比
            all_competitive_ratios.extend(competitive_ratios)

            # 记录所有实验的 ALG 和 OPT
            all_alg_values.extend(alg_values)
            all_opt_values.extend(opt_values)

    # Step 4: 绘制图表并保存到本地
    print("Plotting results...")

    # 竞争比随参数变化的趋势图
    plot_competitive_ratio_trend(n_values, m_values, competitive_ratio_means, save_dir)

    # 竞争比的分布图
    plot_competitive_ratio_distribution(all_competitive_ratios, save_dir)

    # 算法收益与离线最大匹配的对比图
    plot_alg_vs_opt(all_alg_values, all_opt_values, save_dir)

    # 参数敏感性分析图
    plot_parameter_sensitivity(n_values, m_values, competitive_ratio_means, save_dir)

    print("All plots saved to", save_dir)

if __name__ == "__main__":
    main()