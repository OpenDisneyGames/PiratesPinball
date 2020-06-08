# uncompyle6 version 3.7.0
# Python bytecode 2.4 (62061)
# Decompiled from: PyPy Python 3.6.9 (2ad108f17bdb, Apr 07 2020, 03:05:35)
# [PyPy 7.3.1 with MSC v.1912 32 bit]
# Embedded file name: Cheater.py
from direct.showbase.DirectObject import DirectObject

class Cheater(DirectObject):
    __module__ = __name__
    cheaterCount = 0

    def __init__(self, word, callbackFunction, args=None):
        Cheater.cheaterCount += 1
        self.myNumber = Cheater.cheaterCount
        self.word = word
        self.callbackFunction = callbackFunction
        self.args = args
        self.waitingForLetterIndex = 0
        self.setupHooks()
        self.timeToReset = 0.3

    def setupHooks(self):
        usedLetters = ''
        for i in range(len(self.word)):
            if self.word[i] not in usedLetters:
                usedLetters += self.word[i]
                self.accept(self.word[i], self.letterHit, [self.word[i]])

    def letterHit(self, letter):
        if letter == self.word[self.waitingForLetterIndex]:
            self.waitingForLetterIndex += 1
            if self.waitingForLetterIndex == len(self.word):
                if self.args:
                    self.callbackFunction(self.args)
                else:
                    self.callbackFunction()
            taskMgr.remove('word%d' % self.myNumber)
            taskMgr.doMethodLater(self.timeToReset, self.timesUp, 'word%d' % self.myNumber)
        else:
            self.waitingForLetterIndex = 0

    def timesUp(self, task=None):
        self.waitingForLetterIndex = 0

    def wake(self):
        self.setupHooks()

    def sleep(self):
        taskMgr.remove('word%d' % self.myNumber)
        self.ignoreAll()

    def destroy(self):
        self.ignoreAll()