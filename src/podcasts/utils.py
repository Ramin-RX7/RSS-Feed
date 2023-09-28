from django.db.models import Q

from core.parser import *
from .models import PodcastRSS



def get_categories_count(podcasts):
    categories = {}
    for podcast in podcasts:
        category = podcast.main_fields.category
        categories.setdefault(category, 0)
        categories[category] += 1
    sorted_categories = {k:v for k,v in sorted(categories.items(), key=lambda item:item[1], reverse=True)}
    return sorted_categories




def subscription_based_recommended_podcasts(user):
    all_podcasts = PodcastRSS.objects.all()
    user_podcasts = all_podcasts.filter(subscribe__user=user)
    sorted_categories = get_categories_count(user_podcasts)
    podcasts = all_podcasts.exclude(Q(subscribe__user=user) | Q(main_fields__category=None)
                    ).filter(main_fields__category__in=sorted_categories.keys())
    podcasts_ids = podcasts.values_list("id", flat=True)
    return list(podcasts_ids)




    podcasts = all_podcasts.exclude(Q(subscribe__user=user) | Q(main_fields__category=None)).filter(main_fields__category__in=sorted_categories)
    podcasts_ids = podcasts.values_list("id", flat=True)
    return list(podcasts_ids)
