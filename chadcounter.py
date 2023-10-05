import json

#Made by Metalface (Logan M)
#the word we're counting shouldn't be counted a thousand times per second
#by this, so i'm only saving the count on json
#i will likely regret this later when someone types 'chad' a million times

class WordCounter:
    def __init__(self, filename, word):
        self.enabled = True
        self.filename = filename
        self.word = word

    #Parse the message given to the counter, look for the word and increment counter by the amount found
    def parseMessage(self, message):
        if not self.enabled:
            return False

        words = message.content.split()
        count = 0
        for word in words:
            if word == self.word:
                count += 1

        if count > 0:
            return self.incrementCount(count)
        
        return True

    #Increment the count by a chosen number. Returns true if worked, false if not.
    def incrementCount(self, incrementAmount = 1):
        if incrementAmount > 0 and self.enabled:
            count = self.getCount()
            count += incrementAmount
            self._saveCount(count)
            return True
        return self.enabled

    #Re-enables the counter if it failed somehow
    def enableCounter(self):
        self.enabled = True

    #Gets the current count
    def getCount(self):
        if not self.enabled:
            return False

        try:
            with open(self.filename, "r+") as file:
                jsonobj = json.load(file)
                file.close()
                return jsonobj
                

        except json.JSONDecodeError:
            print("Malformed JSON! Could not retrieve original count!")
            self.enabled = False

        except FileNotFoundError:
            self._createCountFile()
            return 0

        except Exception as e:
            print("Exception while opening count file: " + str(e))
            self.enabled = False
            raise e
    
    def _saveCount(self, count):
        try:
            with open(self.filename, "w") as file:
                file.write(json.dumps(count))
        except Exception as e:
            self.enabled = False
            print("Failed to save count!")
            raise e


    def _createCountFile(self):
        try:
            with open(self.filename, "w") as file:
                file.write(json.dumps(0))
            print("New count file " + self.filename + " created.")

        except Exception as e:
            print("Error while creating count file")
            self.enabled = False
            raise e
