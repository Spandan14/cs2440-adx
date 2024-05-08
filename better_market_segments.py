from adx.structures import MarketSegment
from adx.adx_game_simulator import CONFIG


def segment_to_group_set(segment: MarketSegment) -> set:
    if segment == MarketSegment(("Male", "Young")):
        return {"Male", "Young"}
    elif segment == MarketSegment(("Male", "Old")):
        return {"Male", "Old"}
    elif segment == MarketSegment(("Male", "LowIncome")):
        return {"Male", "LowIncome"}
    elif segment == MarketSegment(("Male", "HighIncome")):
        return {"Male", "HighIncome"}
    elif segment == MarketSegment(("Female", "Young")):
        return {"Female", "Young"}
    elif segment == MarketSegment(("Female", "Old")):
        return {"Female", "Old"}
    elif segment == MarketSegment(("Female", "LowIncome")):
        return {"Female", "LowIncome"}
    elif segment == MarketSegment(("Female", "HighIncome")):
        return {"Female", "HighIncome"}
    elif segment == MarketSegment(("Young", "LowIncome")):
        return {"Young", "LowIncome"}
    elif segment == MarketSegment(("Old", "LowIncome")):
        return {"Old", "LowIncome"}
    elif segment == MarketSegment(("Young", "HighIncome")):
        return {"Young", "HighIncome"}
    elif segment == MarketSegment(("Old", "HighIncome")):
        return {"Old", "HighIncome"}
    elif segment == MarketSegment(("Male", "Young", "LowIncome")):
        return {"Male", "Young", "LowIncome"}
    elif segment == MarketSegment(("Female", "Young", "LowIncome")):
        return {"Female", "Young", "LowIncome"}
    elif segment == MarketSegment(("Male", "Old", "LowIncome")):
        return {"Male", "Old", "LowIncome"}
    elif segment == MarketSegment(("Male", "Young", "HighIncome")):
        return {"Male", "Young", "HighIncome"}
    elif segment == MarketSegment(("Female", "Old", "LowIncome")):
        return {"Female", "Old", "LowIncome"}
    elif segment == MarketSegment(("Female", "Young", "HighIncome")):
        return {"Female", "Young", "HighIncome"}
    elif segment == MarketSegment(("Male", "Old", "HighIncome")):
        return {"Male", "Old", "HighIncome"}
    elif segment == MarketSegment(("Female", "Old", "HighIncome")):
        return {"Female", "Old", "HighIncome"}
    else:
        raise ValueError("segment_to_group_set: Invalid MarketSegment")


# Check if campaign with "other" market segment can bid on "base" market segment
def is_market_segment_competing(base: MarketSegment, other: MarketSegment) -> bool:
    base_set = segment_to_group_set(base)
    other_set = segment_to_group_set(other)
    return base_set.intersection(other_set) == other_set


# Returns all the market segments that a campaign with "base" market segment can bid on
def get_biddable_segments(mkt_seg: MarketSegment) -> set:
    all_segments = MarketSegment.all_segments()
    biddable = set()
    for segment in all_segments:
        if is_market_segment_competing(segment, mkt_seg):
            biddable.add(segment)

    return biddable


def expected_long_camp_reach(mkt_seg: MarketSegment, num_campaigns):
    prob_of_segment = 1 / len(CONFIG['market_segment_dist'])
    # expected_days = sum(CONFIG['campaign_length_dist']) / len(CONFIG['campaign_length_dist'])
    # unused currently in generate_campaign from adx_game_simulator.py
    expected_delta = sum(CONFIG['campaign_reach_dist']) / len(CONFIG['campaign_reach_dist'])

    return CONFIG['market_segment_pop'][mkt_seg] * prob_of_segment * num_campaigns * expected_delta


def expected_daily_camp_reach(mkt_seg: MarketSegment, num_campaigns):
    prob_of_segment = 1 / len(CONFIG['market_segment_dist'])
    # expected_days = 1
    # unused currently in generate_campaign from adx_game_simulator.py
    expected_delta = sum(CONFIG['campaign_reach_dist']) / len(CONFIG['campaign_reach_dist'])

    return CONFIG['market_segment_pop'][mkt_seg] * prob_of_segment * num_campaigns * expected_delta
