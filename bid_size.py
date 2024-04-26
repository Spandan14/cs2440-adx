from adx.structures import Campaign

BLK_FACTOR_LIMIT = 0.7
BASELINE_ALPHA = 3
MAX_ALPHA = 9


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


CAMPAIGN_BID_MAX = 1.0
CAMPAIGN_BID_MIN = 0.3


def get_campaign_bid_from_competition(alpha: float, campaign: Campaign) -> float:
    alpha_ratio = alpha / MAX_ALPHA
    return (1 - alpha_ratio) * CAMPAIGN_BID_MIN + alpha_ratio * CAMPAIGN_BID_MAX * campaign.reach
