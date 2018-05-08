from bugs import Bugs
from melon import Melon

m = Melon()
b=Bugs()

choose = input('1. Bugs to Melon\n2. Melon to Bugs\n')
melonId = input('input Melon ID: ')
melonPW = input('input Melon password: ')
melonList = input('input Melon playlist name(correctly!!): ')
bugsId = input('input Bugs ID: ')
bugsPW = input('input Bugs password: ')
bugsList = input('input Bugs playlist name(correctly!!): ')


if choose=='1':
    m.login(melonId, melonPW)
    artists, songs = m.getlist(melonList)
    b.login(bugsId, bugsPW)
    b.addlist(artists, songs, bugsList)
elif choose=='2':
    b.login(bugsId,bugsPW)
    artists, songs = b.getlist(bugsList)
    m.login(melonId, melonPW)
    m.addlist(artists, songs, melonList)




