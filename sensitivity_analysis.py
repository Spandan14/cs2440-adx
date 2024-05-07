import numpy as np
import matplotlib.pyplot as plt
import tqdm

from adx.tier1_ndays_ncampaign_agent import Tier1NDaysNCampaignsAgent
from my_ndays_ncampaign_agent import run_simulation, MyNDaysNCampaignsAgent

from bid_size import BLK_FACTOR_LIMIT, BASELINE_ALPHA, MAX_ALPHA

N_DAYS = 10
N_AGENTS = 5
N_GENS = 100


def sensitivity_analysis(params):
    blk_factor_limit, baseline_alpha, max_alpha = params

    assert(len(blk_factor_limit) == 1)
    assert(len(max_alpha) == 1)

    days = np.arange(1, N_DAYS + 1)

    avg_qs_tensor = np.zeros((len(blk_factor_limit), len(baseline_alpha), len(max_alpha), N_DAYS))
    avg_profits_tensor = np.zeros((len(blk_factor_limit), len(baseline_alpha), len(max_alpha), N_DAYS))
    avg_active_camps_tensor = np.zeros((len(blk_factor_limit), len(baseline_alpha), len(max_alpha), N_DAYS))
    avg_alpha_tensor = np.zeros((len(blk_factor_limit), len(baseline_alpha), len(max_alpha), N_DAYS))

    for i, bfl in enumerate(blk_factor_limit):
        for j, ba in tqdm.tqdm(enumerate(baseline_alpha)):
            for k, ma in enumerate(max_alpha):
                print(f"Running simulation with blk_factor_limit: {bfl}, baseline_alpha: {ba}, max_alpha: {ma}")
                agents = [MyNDaysNCampaignsAgent(bfl, ba, ma)] + \
                         [Tier1NDaysNCampaignsAgent(name=f"Agent {i + 1}") for i in range(N_AGENTS - 1)]
                quality_scores, profits, active_camps, our_alpha = run_simulation(agents, N_GENS)

                our_avg_qs = np.mean(quality_scores, axis=0)[:, 0].reshape(-1)
                our_avg_profits = np.mean(profits, axis=0)[:, 0].reshape(-1)
                our_avg_active_camps = np.mean(active_camps, axis=0)[:, 0].reshape(-1)
                our_daily_alpha = np.mean(our_alpha, axis=0).reshape(-1)

                avg_qs_tensor[i, j, k] = our_avg_qs
                avg_profits_tensor[i, j, k] = our_avg_profits
                avg_active_camps_tensor[i, j, k] = our_avg_active_camps
                avg_alpha_tensor[i, j, k] = our_daily_alpha

    print("Simulation complete!")

    def get_val(tensor, day, x):
        return tensor[0, x, 0][day]

    # plotting quality scores
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(f'Average Quality Scores with Different Baseline Alphas Over {N_GENS} Games')

    colors = plt.cm.get_cmap('rainbow', len(baseline_alpha))
    for i, ba in enumerate(baseline_alpha):
        ax.scatter(days, [ba] * len(days), avg_qs_tensor[0, i, 0], color=colors(i))

    ax.set_xlabel('Day')
    ax.set_ylabel('Baseline Alpha')
    ax.set_zlabel('Quality Score')
    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(f'Average Profits with Different Baseline Alphas Over {N_GENS} Games')

    colors = plt.cm.get_cmap('rainbow', len(baseline_alpha))
    for i, ba in enumerate(baseline_alpha):
        ax.scatter(days, [ba] * len(days), avg_profits_tensor[0, i, 0], color=colors(i))

    ax.set_xlabel('Day')
    ax.set_ylabel('Baseline Alpha')
    ax.set_zlabel('Profits')
    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(f'Average Active Campaigns with Different Baseline Alphas Over {N_GENS} Games')

    colors = plt.cm.get_cmap('rainbow', len(baseline_alpha))
    for i, ba in enumerate(baseline_alpha):
        ax.scatter(days, [ba] * len(days), avg_active_camps_tensor[0, i, 0], color=colors(i))

    ax.set_xlabel('Day')
    ax.set_ylabel('Baseline Alpha')
    ax.set_zlabel('Active Campaigns')
    plt.show()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(f'Average Agent Alpha with Different Baseline Alphas Over {N_GENS} Games')

    colors = plt.cm.get_cmap('rainbow', len(baseline_alpha))
    for i, ba in enumerate(baseline_alpha):
        ax.scatter(days, [ba] * len(days), avg_alpha_tensor[0, i, 0], color=colors(i))

    ax.set_xlabel('Day')
    ax.set_ylabel('Baseline Alpha')
    ax.set_zlabel('Agent Alpha')
    plt.show()

    # save tensors to file
    np.save('avg_qs_tensor.npy', avg_qs_tensor)
    np.save('avg_profits_tensor.npy', avg_profits_tensor)
    np.save('avg_active_camps_tensor.npy', avg_active_camps_tensor)
    np.save('avg_alpha_tensor.npy', avg_alpha_tensor)


alphas = [3.75 + 0.1 * n for n in range(-5, 5)]

sensitivity_analysis(([BLK_FACTOR_LIMIT], alphas, [MAX_ALPHA]))
