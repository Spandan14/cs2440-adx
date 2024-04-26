from adx.structures import Campaign, MarketSegment
from better_market_segments import is_market_segment_competing, expected_daily_camp_reach, expected_long_camp_reach


class CampaignObservations:
    def __init__(self, num_players):
        self.waiting_campaigns = []
        self.auction_campaigns = []
        self.dead_campaigns = []
        self.num_players = num_players

    def update_campaigns(self, current_day):
        for campaign in self.auction_campaigns:
            if campaign.end_day < current_day:
                self.dead_campaigns.append(campaign)
                self.auction_campaigns.remove(campaign)

        for campaign in self.waiting_campaigns:
            if campaign.start_day <= current_day:
                self.auction_campaigns.append(campaign)
                self.waiting_campaigns.remove(campaign)

    def add_campaign(self, campaign: Campaign, current_day):
        if campaign.start_day > current_day:
            self.waiting_campaigns.append(campaign)
        elif campaign.start_day <= current_day <= campaign.end_day:
            self.auction_campaigns.append(campaign)
        else:
            raise ValueError(f"Campaign {campaign} is finished. Day: {current_day}")

    def remove_campaign(self, campaign: Campaign):
        if campaign in self.waiting_campaigns:
            self.waiting_campaigns.remove(campaign)
        else:
            raise ValueError("Only waiting campaigns are removable.")

    def get_observed_reach(self, mkt_seg: MarketSegment, campaigns):
        total_reach = 0

        for campaign in campaigns:
            if is_market_segment_competing(mkt_seg, campaign.target_segment):
                total_reach += campaign.reach / (campaign.end_day - campaign.start_day + 1)

        return total_reach + expected_daily_camp_reach(mkt_seg, self.num_players)

    def get_expected_reach(self, mkt_seg: MarketSegment, campaigns):
        return expected_long_camp_reach(mkt_seg, len(campaigns)) + \
            expected_daily_camp_reach(mkt_seg, self.num_players)

    def get_competition_value(self, mkt_seg: MarketSegment):
        return self.get_observed_reach(mkt_seg, self.auction_campaigns) / \
            self.get_expected_reach(mkt_seg, self.auction_campaigns)

    def get_tentative_competition_value(self, mkt_seg: MarketSegment):
        return self.get_observed_reach(mkt_seg, self.auction_campaigns + self.waiting_campaigns) / \
            self.get_expected_reach(mkt_seg, self.auction_campaigns + self.waiting_campaigns)
