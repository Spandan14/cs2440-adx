from adx.agents import NDaysNCampaignsAgent
from adx.tier1_ndays_ncampaign_agent import Tier1NDaysNCampaignsAgent
from adx.adx_game_simulator import AdXGameSimulator
from adx.structures import Bid, Campaign, BidBundle 
from typing import Set, Dict

from bid_size import *
from campaign_observations import CampaignObservations
from math_utils import avg_effective_reach


class MyNDaysNCampaignsAgent(NDaysNCampaignsAgent):
    def __init__(self):
        # TODO: fill this in (if necessary)
        super().__init__()
        self.name = "Samuel Benjamin Bankman-Fried"  # TODO: enter a name.
        self.NUM_PLAYERS = 10
        self.campaign_obs = CampaignObservations(self.NUM_PLAYERS)
        self.current_day = 0

    def on_new_game(self) -> None:
        # TODO: fill this in (if necessary)
        self.campaign_obs = CampaignObservations(self.NUM_PLAYERS)
        self.current_day = 0

    def get_ad_bids(self) -> Set[BidBundle]:
        # TODO: fill this in
        bundles = set()
        for campaign in self.get_active_campaigns():
            alpha = self.campaign_obs.get_competition_value(campaign.target_segment)
            blk_size = get_block_size_from_competition(alpha, campaign, self.current_day)
            bid_amt = avg_effective_reach(campaign.cumulative_reach, campaign.cumulative_reach + blk_size,
                                          campaign.reach)
            total_limit = blk_size * bid_amt
            if total_limit == 0:
                bid_amt = 0

            bid = Bid(self, campaign.target_segment, bid_amt, total_limit)
            bundle = BidBundle(campaign.uid, total_limit, {bid})
            bundles.add(bundle)

        return bundles

    def get_campaign_bids(self, campaigns_for_auction:  Set[Campaign]) -> Dict[Campaign, float]:
        # TODO: fill this in
        self.current_day += 1
        self.campaign_obs.update_campaigns(self.current_day)
        for campaign in campaigns_for_auction:
            self.campaign_obs.add_campaign(campaign, self.current_day)

        bids = {}

        for campaign in campaigns_for_auction:
            mkt_seg = campaign.target_segment
            alpha = self.campaign_obs.get_tentative_competition_value(mkt_seg)
            bids[campaign] = get_campaign_bid_from_competition(alpha, campaign)

        return bids


if __name__ == "__main__":
    # Here's an opportunity to test offline against some TA agents. Just run this file to do so.
    test_agents = [MyNDaysNCampaignsAgent()] + [Tier1NDaysNCampaignsAgent(name=f"Agent {i + 1}") for i in range(9)]

    # Don't change this. Adapt initialization to your environment
    simulator = AdXGameSimulator()
    simulator.run_simulation(agents=test_agents, num_simulations=500)
