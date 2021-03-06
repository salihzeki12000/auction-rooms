from django.contrib.sitemaps import Sitemap

from auction_rooms.auctions.models import Auction


class AuctionStaticSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Auction.objects.all()

    def lastmod(self, obj):
        return obj.modified
