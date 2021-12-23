from django.db.models import QuerySet, Count


class ClickQueryset(QuerySet):
    def aggregate_by_browser(self):
        return self.values('browser').annotate(browser_count=Count('browser'))

    def aggregate_by_platform(self):
        return self.values('platform').annotate(platform_count=Count('platform'))
