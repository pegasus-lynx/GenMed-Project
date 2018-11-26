from django.contrib.syndication.views import Feed
from .models import Comment
from  django.urls import reverse

# Show comment feed
class ShopCommentFeed(Feed):
    title="Shop's Comments"
    link="/shopcomments/"
    description = "Recent comments on shop's"

    def items(self):
        return Comment.objects.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.comment_no

    def item_link(self, item):
        return reverse('shop:feeds', kwargs={'comment_no': item.pk })