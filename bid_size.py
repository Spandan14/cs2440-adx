from adx.structures import Campaign
from adx.structures import MarketSegment
from scipy.optimize import fsolve
import math

BLK_FACTOR_LIMIT = 1 # has to be fucking over 1
BASELINE_ALPHA = 3
MAX_ALPHA = 20


def get_block_size_from_competition(alpha: float, campaign: Campaign, current_day: int) -> float:
    reach_ratio = 1 / (campaign.end_day - current_day + 1)

    if alpha < BASELINE_ALPHA:
        a_ratio = alpha / BASELINE_ALPHA
        blk_factor = (1 - a_ratio) * (BLK_FACTOR_LIMIT - reach_ratio) + reach_ratio
        left_reach = campaign.reach - campaign.cumulative_reach  # R_l
        return max(0.0, min(BLK_FACTOR_LIMIT * left_reach, blk_factor * left_reach))
    elif alpha > BASELINE_ALPHA:
        a_ratio = (alpha - BASELINE_ALPHA) / (MAX_ALPHA - BASELINE_ALPHA)
        blk_factor = (1 - a_ratio) * reach_ratio
        left_reach = campaign.reach - campaign.cumulative_reach
        return max(0.0, blk_factor * left_reach)


CAMPAIGN_BID_MAX = 0.9
CAMPAIGN_BID_MIN = 0.25
CAMPAIGN_MAX_ALPHA = 10


def get_campaign_bid_from_competition(alpha: float, campaign: Campaign) -> float:
    alpha_ratio = alpha / CAMPAIGN_MAX_ALPHA
    return ((1 - alpha_ratio) * CAMPAIGN_BID_MIN + alpha_ratio * CAMPAIGN_BID_MAX) * campaign.reach
    # return solve_for_y(alpha_ratio, campaign.reach)

# def equation(y, x):
#     # purple curve on desmos
#     # return ((y - 3)**2 / 2**2) - (x**2 / 0.145**2) - 1
#     # blue curve on desmos
#     return (y**2 / 2**2) - (x**2 / 0.11**2) - 1

# def solve_for_y(x):
#     # initial_guess = 6  # Initial guess for y
#     initial_guess = 2
#     solution = fsolve(equation, initial_guess, args=(x,))
#     return max(solution)

def solve_for_y(x, reach):
    y = (reach / 20) * math.sqrt(4 + ((4 * (x**2)) / (0.11**2)))
    return y




# # sanity check
# import matplotlib.pyplot as plt
# import numpy as np
#
# x = np.linspace(0, 5, 100)
#
# c = Campaign(100, MarketSegment.all_segments()[0], 1, 2)
# c.cumulative_reach = 70
# y = [get_block_size_from_competition(xi, c, 2) for xi in x]
#
# plt.plot(x, y)
# plt.show()