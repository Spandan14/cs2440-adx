from adx.agents import NDaysNCampaignsAgent
from adx.tier1_ndays_ncampaign_agent import Tier1NDaysNCampaignsAgent
from adx.adx_game_simulator import AdXGameSimulator
from adx.structures import Bid, Campaign, BidBundle 
from typing import Set, Dict

from bid_size import *
from campaign_observations import CampaignObservations
from math_utils import avg_effective_reach

import numpy as np
import matplotlib.pyplot as plt


class MyNDaysNCampaignsAgent(NDaysNCampaignsAgent):
    def __init__(self):
        # TODO: fill this in (if necessary)
        super().__init__()
        self.name = "Samuel Benjamin Bankman-Fried"  # TODO: enter a name.
        self.NUM_PLAYERS = 10
        self.campaign_obs = CampaignObservations(self.NUM_PLAYERS)
        self.current_day = 0
        self.avg_alpha = 0

    def on_new_game(self) -> None:
        # TODO: fill this in (if necessary)
        self.campaign_obs = CampaignObservations(self.NUM_PLAYERS)
        self.current_day = 0

    def get_ad_bids(self) -> Set[BidBundle]:
        # TODO: fill this in
        bundles = set()
        day_alpha = 0
        self.current_day += 1
        print(f"Day {self.current_day}: campaigns up: {len(self.get_active_campaigns())}")
        for campaign in self.get_active_campaigns():
            alpha = self.campaign_obs.get_competition_value(campaign.target_segment)
            day_alpha += alpha
            blk_size = get_block_size_from_competition(alpha, campaign, self.current_day)
            bid_amt = avg_effective_reach(campaign.cumulative_reach, campaign.cumulative_reach + blk_size,
                                          campaign.reach)
            total_limit = blk_size * bid_amt
            if total_limit == 0:
                bid_amt = 0

            print(f"campaign {campaign.uid} bid: {bid_amt} limit: {total_limit} blk_size: {blk_size / campaign.reach} "
                  f"days left: {campaign.end_day - self.current_day + 1}/{campaign.end_day - campaign.start_day + 1}")
            bid = Bid(self, campaign.target_segment, bid_amt, total_limit)
            bundle = BidBundle(campaign.uid, total_limit, {bid})
            bundles.add(bundle)

        self.avg_alpha = day_alpha / len(self.get_active_campaigns()) if len(self.get_active_campaigns()) > 0 else 0
        return bundles

    def get_campaign_bids(self, campaigns_for_auction:  Set[Campaign]) -> Dict[Campaign, float]:
        # TODO: fill this in
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
    quality_scores, profits, active_camps, our_alpha = simulator.run_simulation(agents=test_agents, num_simulations=25)

    days = np.arange(1, quality_scores.shape[1] + 1)
    num_agents = quality_scores.shape[2]

    avg_qs = np.mean(quality_scores, axis=0)
    for i in range(num_agents):
        plt.plot(days, avg_qs[:, i], label=f"Agent {i + 1}", color='b' if i == 0 else 'orange')

    plt.title("Quality Scores")
    plt.legend()
    plt.show()

    avg_profits = np.mean(profits, axis=0)
    for i in range(num_agents):
        plt.plot(days, avg_profits[:, i], label=f"Agent {i + 1}", color='b' if i == 0 else 'orange')

    plt.title("Profits")
    plt.legend()
    plt.show()

    avg_active_camps = np.mean(active_camps, axis=0)
    for i in range(num_agents):
        plt.plot(days, avg_active_camps[:, i], label=f"Agent {i + 1}", color='b' if i == 0 else 'orange')

    plt.title("Active Campaigns")
    plt.legend()
    plt.show()

    daily_alpha = np.mean(our_alpha, axis=0)
    plt.plot(days, daily_alpha, label="Our Alpha", color='b')
    plt.title("Our Alpha")
    plt.legend()
    plt.show()


