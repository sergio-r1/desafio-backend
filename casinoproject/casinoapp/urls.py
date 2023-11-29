from django.urls import path
from .views import get_balance, place_bet, win

urlpatterns = [
    path('balance/<int:player_id>/', get_balance, name='get_balance'),
    path('bet/', place_bet, name='place_bet'),
    path('win/', win, name='win'),
]