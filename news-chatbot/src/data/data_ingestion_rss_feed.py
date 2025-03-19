import feedparser
import pandas as pd


class RssFeed:
    def __init__(self):
        self.rss_urls = {
            "AU_general": [
                "http://www.abc.net.au/news/feed/46182/rss.xml",
                "http://feeds.feedburner.com/TheAustralianTheNationNews",
                "http://feeds.smh.com.au/rssheadlines/national.xml",
                "http://www.theguardian.com/au/rss",
                "http://www.abc.net.au/local/rss/sydney/news.xml",
                "http://www.channelnewsasia.com/starterkit/servlet/cna/rss/asiapacific.xml",
                "http://feeds.brisbanetimes.com.au/rssheadlines/national.xml",
                "http://feeds.brisbanetimes.com.au/rssheadlines/world.xml",
                "http://feeds.theage.com.au/rssheadlines/national.xml",
                "http://au.ibtimes.com/rss/articles/countries/13.rss",
                "http://rss.nzherald.co.nz/rss/xml/nzhrsscid_000000002.xml",
                "http://www.gmanetwork.com/news/rss/news",
                "http://feeds.bbci.co.uk/news/world/asia/rss.xml",
                "http://www.dailymail.co.uk/auhome/index.rss",
                "http://feeds.feedburner.com/dailytelegraphnationalnewsndm?format=xml",
                "http://feeds.news.com.au/public/rss/2.0/bcm_top_stories_257.xml",
                "http://feeds.news.com.au/public/rss/2.0/anow_topstories_250.xml",
                "http://feeds.news.com.au/heraldsun/rss/heraldsun_news_morenews_2794.xml",
                "http://feeds.news.com.au/public/rss/2.0/The%20Mercury%20%7C%20Top%20Stories_3304.xml",
                "http://feeds.news.com.au/public/rss/2.0/wtn_top_3368.xml"
            ],
            "AU_politics": [
                "http://feeds.feedburner.com/TheAustralianPolitics",
                "http://feeds.news.com.au/public/rss/2.0/au_national_affairs_news_13_3296.xml",
                "http://feeds.feedburner.com/TheAustralianMediaNews",
                "http://www.businessspectator.com.au/bs/rss.xml",
                "http://www.abc.net.au/news/feed/1534/rss.xml",
                "http://www.abc.net.au/radionational/feed/3727018/rss.xml",
                "http://www.abc.net.au/radionational/feed/2884582/rss.xml",
                "http://www.pm.gov.au/rss-feeds/press-office",
                "http://www.rba.gov.au/rss/rss-cb-media-releases.xml",
                "http://www.crikey.com.au/politics/feed",
                "http://www.economist.com/topics/australia/index.xml",
                "http://www.theguardian.com/world/australian-politics/rss",
                "http://mashable.com/category/australian-politics/rss/"
            ],
            "AU_business": [
                "http://www.businessspectator.com.au/bs/rss.xml",
                "http://www.cio.com/index.rss",
                "http://www.dynamicbusiness.com.au/feed",
                "http://feeds.feedburner.com/TheAustralianBusNews?format=xml",
                "http://feeds.feedburner.com/TheAustralianBusAviation?format=xml",
                "http://feeds.feedburner.com/TheAustralianBusinessWorldBusNews?format=xml",
                "http://feeds.news.com.au/public/rss/2.0/business_top_stories_346.xml",
                "http://www.abc.net.au/news/feed/51892/rss.xml",
                "http://www.smh.com.au/rssheadlines/business.xml",
                "http://feeds.news.com.au/heraldsun/rss/heraldsun_news_business_2783.xml",
                "http://abns.com.au/feed/"
            ],
            "AU_health": [
                "http://www.smh.com.au/rssheadlines/health/article/rss.xml",
                "http://www.womenshealthandfitness.com.au/component/obrss/women-s-health-fitness-combined-feed?format=",
                "http://feeds.news.com.au/public/rss/2.0/news_lifestyle_3171.xml",
                "http://www.telegraph.co.uk/health/rss",
                "http://www.shapemagazine.com.au/feed/",
                "http://www.alive.com/articles/rss",
                "http://www.wellbeing.com.au/blog/feed/",
                "http://www.mensfitnessmagazine.com.au/topics/health-nutrition/feed/",
                "http://www.dailyrecord.co.uk/lifestyle/health-fitness/rss.xml",
                "http://www.starobserver.com.au/category/features/healthy-living/feed"
            ],
            "AU_science": [
                "http://feeds.news.com.au/public/rss/2.0/news_tech_506.xml",
                "http://www.smh.com.au/rssheadlines/health/article/rss.xml",
                "http://www.sbs.com.au/news/rss/news/science-technology.xml",
                "http://www.theage.com.au/rssheadlines/technology-news/article/rss.xml",
                "http://www.watoday.com.au/rssheadlines/technology-news/article/rss.xml",
                "http://www.australianscience.com.au/feed/",
                "http://www.scienceweek.net.au/homepage/feed/"
            ],
            "AU_sports": [
                "http://feeds.news.com.au/public/rss/2.0/fs_breaking_news_13.xml",
                "http://www.abc.net.au/news/feed/45924/rss.xml",
                "http://feeds.feedburner.com/TheAustralianSportsNews",
                "http://feeds.news.com.au/public/rss/2.0/news_sport_3168.xml",
                "http://feeds.smh.com.au/rssheadlines/sport.xml",
                "http://feeds.theage.com.au/rssheadlines/sport.xml",
                "http://feeds.news.com.au/rss/newslocal/dt_nlocal_sport_3214.xml",
                "http://feeds.news.com.au/heraldsun/rss/heraldsun_news_sport_2789.xml",
                "http://feeds.bbci.co.uk/sport/0/cricket/rss.xml?edition=uk",
                "http://sbs.feedsportal.com/c/34692/f/637526/index.rss",
                "http://wwos.ninemsn.com.au/rss/headlines/"
            ],
            "AU_tech": [
                "http://feeds.gizmodo.com.au/gizmodoaustraliaau",
                "http://www.smh.com.au/rssheadlines/technology-news/article/rss.xml",
                "http://feeds.news.com.au/public/rss/2.0/ausit_exec_topstories_385.xml",
                "http://feeds.news.com.au/heraldsun/rss/heraldsun_news_technology_2790.xml",
                "http://feeds.news.com.au/public/rss/2.0/news_tech_506.xml",
                "http://techau.com.au/feed/",
                "http://www.techrepublic.com/rssfeeds/blog/australian-technology/"
            ],
            "AU_entertainment": [
                "http://feeds.smh.com.au/rssheadlines/entertainment.xml",
                "http://www.news.com.au/entertainment",
                "http://feeds.news.com.au/public/rss/2.0/cpost_news_entertainment_3329.xml",
                "http://feeds.news.com.au/public/rss/2.0/The%20Mercury%20|%20Entertainment_3306.xml",
                "http://www.goldcoastbulletin.com.au/entertainment",
                "http://www.spotlightreport.net/feed",
                "http://www.popsugar.com.au/celebrity/feed",
                "http://www.okmagazine.com.au/rss.axd?channel=entertainment_articles",
                "http://www.studiotv.com.au/feed/",
                "http://feeds.feedburner.com/sunshinecoastdailyentertainmen"
            ]
        }

    def parse_feed(self):
        all_items = []
        for category, urls in self.rss_urls.items():
            print(category)
            for url in urls:
                feed = feedparser.parse(url)
                print("......", url)

            # Extract relevant fields for each entry
                for entry in feed.entries:
                    item = {
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.published,
                        'summary': entry.summary,
                        # Extract category if available
                        "sub_category": entry.get('category', 'No category available'),
                        "category": category,
                        "author": entry.get('author', 'No author available')

                    }
                    all_items.append(item)
        df = pd.DataFrame(all_items)

        df.to_csv('news-chatbot/data/raw/abc_news_feed.csv', index=False)


def main():
    rss_feed = RssFeed()
    rss_feed.parse_feed()


if __name__ == "__main__":
    main()
