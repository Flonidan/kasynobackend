from django.http import JsonResponse
from . import userapi


def slot(request):
	mid1 = request.POST.get('mid1')
	mid2 = request.POST.get('mid2')
	mid3 = request.POST.get('mid3')
	betamount = float(request.POST.get('betamount'))
	if mid1==mid2==mid3:#jesli srodkowy wiersz ma 3 takie same znaczki
	#symbole oczywiscie moga sie zmienic - tu komentarze i wygrane sa z grafiki z trello
		if mid1=='1':#winogorona x2
			betamount=betamount*2
		if mid1=='2':#wisnie x3
			betamount=betamount*3
		if mid1=='3':#banany x4
			betamount=betamount*4
		if mid1=='4':#gruszki x6
			betamount=betamount*6
		if mid1=='5':#pomarancze x10
			betamount=betamount*10
		if mid1=='6':#serduszka x15
			betamount=betamount*15
		if mid1=='7':#monety x20
			betamount=betamount*20
		if mid1=='8':#jackpot x30
			betamount=betamount*30
	else: #przegrana
		betamount=-betamount
	callModifyBalance(request,betamount)
	return JsonResponse({'amount':betamount})
def roulette(request):
	return JsonResponse({"status":"Roulette not implemented"})
def dice(request):
	return JsonResponse({"status":"Dices not implemented"})
def blackjack(request):
	betamount = float(request.POST.get('betamount'))
	bankCards = makeArrayOfIntsFromString(request,'bank')
	playerCards = makeArrayOfIntsFromString(request,'player')
	bankScore = blackjackScore(bankCards)
	playerScore = blackjackScore(playerCards)
	amount = 0
	if bankScore > playerScore:
		amount = - betamount
	elif bankScore < playerScore:
		amount = betamount
	callModifyBalance(request,amount)
	return JsonResponse({"amount":amount})
def poker(request):
	return JsonResponse({"status":"Poker not implemented"})
def baccarat(request):
	betamount = float(request.POST.get('betamount'))
	bet = request.POST.get('bet')
	bankCards = makeArrayOfIntsFromString(request,'bank')
	playerCards = makeArrayOfIntsFromString(request,'player')
	bankScore = baccaratScore(bankCards)
	playerScore = baccaratScore(playerCards)
	result = ''
	amount = 0
	if bankScore == playerScore:
		result = 'tie'
	elif bankScore > playerScore:
		result = 'bank'
	else:
		result = 'player'
	if result==bet:
		if bet == 'player':
			amount = 2 * betamount
		elif bet == 'bank':
			amount = 1.95 * betamount
		else :
			amount = 8 * betamount
	else :
		amount = - betamount
	callModifyBalance(request, amount)
	return JsonResponse({'amount':amount})
def cointoss(request):
	betamount = float(request.POST.get('betamount'))
	bet = request.POST.get('bet')
	toss = request.POST.get('toss')
	if bet==toss:
		betamount = betamount * 1.9
	else:
		betamount=-betamount
	callModifyBalance(request,betamount)
	return JsonResponse({'amount':betamount})
	
#pomocniczne metody
def makeArrayOfIntsFromString(request,postKey):
	arr = request.POST.get(postKey)
	arr = arr.split(',')
	arr = [int(value) for value in arr]
	return arr
def callModifyBalance(request,amount):
	mutable = request.POST._mutable
	request.POST._mutable = True
	request.POST['amount'] = amount
	request.POST._mutable = mutable
	response=userapi.modifyBalance(request)
def baccaratScore(arrayOfInts):
	arrayOfInts = [ value%13 for value in arrayOfInts ]
	result = 0;
	for value in arrayOfInts:
		if value < 10:
			result = result + value
	return result % 10
def blackjackScore(arrayOfInts):
	arrayOfInts = [value%13 for value in arrayOfInts]
	result = 0
	numberOfAces = 0
	for value in arrayOfInts:
		if value >=2 and value <=10:
			result = result + value
		elif value == 0 or value == 11 or value == 12: #krol od walet or dama
			result = result + 10
		elif value == 1:#as
			numberOfAces = numberOfAces + 1
	#tu mamy juz policzone wszystkie karty z wyjatkiem asow
	valueFromAces = 0
	bestOption = result + numberOfAces # najmniejszy mozliwy wynik ( punkty z karty + asy za jeden )
	for i in range(1,numberOfAces+1):
		valueFromAces = (numberOfAces-i) * 1 + i*10#tu jest liczona wartosc jezeli z n asow i bedzie traktowane jako '1' a n-i jako 10
		if  result + valueFromAces > 21:#wartosc liczona u gory jest rosnaca wiec jesli ktoras przekroczy 21 to konczymy petle
			break
		else:
			if (result + valueFromAces) > bestOption:#sprawdzamy czy ten podzial na '1' i '10' jest lepszy
				bestOption = result + valueFromAces
	result = bestOption
	if result > 21:
		result = 0
	return result