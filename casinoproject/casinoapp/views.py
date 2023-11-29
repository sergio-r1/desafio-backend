from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
import json

from .models import Player, Transaction


@require_GET
def get_balance(request, player_id):
    """ Endpoint para obter o saldo na carteira de um player

    Args:
        request: Requisição HTTP
        player_id: ID de identificação do player

    Returns:
        Retorna um arquivo JSON contendo o player e o saldo no formato {"player": ID, "balance": SALDO}
    """
    #Verifica se o player existe, caso não, gera erro
    player = get_object_or_404(Player, pk=player_id)

    #Retorna o arquivo JSON
    return JsonResponse({"player": player_id, "balance": str(player.balance)})


@csrf_exempt
@require_POST
def place_bet(request):
    """ Endpoint para realizar uma aposta usando a carteira de um player.

    Args:
        request: Requisição HTTP recebida contendo dados JSON no corpo.

    Returns:
        Retorna uma resposta JSON contendo o saldo atualizado da carteira e o ID da transação realizada.
        Este endpoint só aceita solicitações HTTP POST e desabilita a proteção CSRF.
    """

    try:
        #Analise do JSON recebido na requisição
        data = json.loads(request.body.decode('utf-8'))
        player_id = data.get("player")
        value = data.get("value")

        # Obtém o player ou retorna 404 se não encontrado
        player = get_object_or_404(Player, pk=player_id)

        # Verifica se o saldo do player é maior do que o valor da aposta, caso não, retorna um JSON com erro informado
        if player.balance < value:
            return JsonResponse({"error": "Insufficient funds"}, status=400)

        # Atualiza o saldo do player
        player.balance -= value
        player.save()

        # Cria uma transação e retorna a resposta em JSON
        transaction = Transaction.objects.create(player=player, transaction_type='bet', value=value)
        return JsonResponse({"player": player_id, "balance": str(player.balance), "txn": transaction.pk})

    except Exception as e:
        # Em caso de exceção, retorna um erro e o status HTTP 400 (Requisição inválida)
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
@require_POST
def win(request):
    """ Endpoint para marcar vitória, e ganhos, usando a carteira de um player.

    Args:
        request: Requisição HTTP recebida contendo dados JSON no corpo.

    Returns:
        Retorna uma resposta JSON contendo o saldo atualizado da carteira e o ID da transação realizada.
        Este endpoint só aceita solicitações HTTP POST e desabilita a proteção CSRF.
    """

    try:
        #Analise do JSON recebido na requisição
        data = json.loads(request.body.decode('utf-8'))
        player_id = data.get("player")
        value = data.get("value")

        # Verifica se o jogador existe, cria um novo se não existir
        player, created = Player.objects.get_or_create(pk=player_id, defaults={"balance": 0})

        # Atualiza o saldo do player
        player.balance += value
        player.save()

        # Cria uma transação e retorna a resposta em JSON
        transaction = Transaction.objects.create(player=player, transaction_type='win', value=value)
        return JsonResponse({"player": player_id, "balance": str(player.balance), "txn": transaction.pk})

    except Exception as e:
        # Em caso de exceção, retorna um erro e o status HTTP 400 (Requisição inválida)
        return JsonResponse({"error": str(e)}, status=400)
    

