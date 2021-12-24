from datetime import datetime
from django.db.models import QuerySet, Count


class ClickQueryset(QuerySet):

    def for_current_month(self):
        return self.filter(
            created_at__date__month=datetime.now().month,
            created_at__date__year=datetime.now().year,
        )

    def aggregate_by_browser(self):
        return self.values('browser').annotate(browser_count=Count('browser'))

    def aggregate_by_platform(self):
        return self.values('platform').annotate(platform_count=Count('platform'))
