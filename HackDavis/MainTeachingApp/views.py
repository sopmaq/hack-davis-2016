from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .models import Score

def homePage(request):
    context = {}
    if request.user.is_authenticated():
        return redirect('/leaderboard')

    return render(request, 'MainTeachingApp/index.html', context)

def leaderboardPage(request):
    context = {}
    if not request.user.is_authenticated():
        return redirect('/')

    # Get all the score entries found
    scoreList = Score.objects.all().order_by('-theHighScore')
    print("The score list is", scoreList)
    context['studentDict'] = scoreList

    return render(request, 'MainTeachingApp/leaderboard.html', context)

def processSignIn(request):
    context = {}
    if request.user.is_authenticated() or not request.method == 'POST':
        return redirect('/')

    username = request.POST.get('usernameBox', '')
    password = request.POST.get('passwordBox', '')

    print(username + ' -> ' + password)
    user = authenticate(username=username, password=password)
    if user is None:
        print("The credentials aren't valid.")
        return redirect('/invalidCredentials')

    login(request, user)
    return redirect('/leaderboard')

def gamePage(request):
    context = {}
    if not request.user.is_authenticated():
        return redirect('/')

    thisUserScoreList = Score.objects.all().filter(theUserWhoEarnedIt__username=request.user.username)
    if not len(thisUserScoreList) == 0:
        thisUserScoreList = thisUserScoreList[0]
        currHighScore = thisUserScoreList.theHighScore
        context['currHighScore'] = currHighScore


    return render(request, 'MainTeachingApp/play.html', context)

def processGameAnswers(request):
    context = {}
    if not request.user.is_authenticated() or not request.method == 'GET':
        return redirect('/')

    score = request.GET.get('score', None)
    if score == None:
        return redirect('/')

    score = int(score)
    context['score'] = score

    thisUserScore = Score.objects.all().filter(theUserWhoEarnedIt__username=request.user.username)
    if not len(thisUserScore) == 0:
        thisUserScore = thisUserScore[0]
    else:
        newScore = Score()
        newScore.theUserWhoEarnedIt = request.user
        newScore.theHighScore = score
        newScore.theNumOfGamesPlayed = 1
        newScore.save()

    oldHighScore = int(thisUserScore.theHighScore)
    if oldHighScore < score:
        thisUserScore.theHighScore = score

    thisUserScore.theNumOfGamesPlayed = thisUserScore.theNumOfGamesPlayed + 1
    thisUserScore.save()

    return redirect('/leaderboard')

def logoutUser(request):
    logout(request)
    return redirect('/')
    
