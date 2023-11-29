from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
from .models import Player, Transaction
import json

class CasinoAppTestCase(TestCase):
    
    def setUp(self):
        # Configuração inicial antes de cada teste para player e carteira
        self.player = Player.objects.create(pk=1, balance=1000)


    def test_get_balance(self):
        url = reverse('get_balance', args=[self.player.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['player'], self.player.pk)
        self.assertEqual(data['balance'], f"{float(self.player.balance):.1f}") # forçando o tipo da variavel e usando um format para acrescentar .0 ao fazer a comparação
    
    
    def test_place_bet(self):
        url = reverse('place_bet')
        data = {"player": self.player.pk, "value": 5}

        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['player'], self.player.pk)
        self.assertEqual(data['balance'], str(self.player.balance - 5.0))


    def test_win(self):
        url = reverse('win')
        data = {"player": self.player.pk, "value": 100}

        response = self.client.post(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['player'], self.player.pk)
        self.assertEqual(data['balance'], str(self.player.balance + 100.0))
