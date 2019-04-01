
class Sessions():
    def __init__(self):
        self.encryption = 'asdf'

    def storeSession(self, host, username='', password=''):
        """
        saves a session
        returns true if successful
        """ 
        file = open('sessions.txt', 'a')
        file.write('%s,%s,%s\n' % (host, username, password))
        file.close()
    
    def getSessions(self):
        """
        returns a list of tuples
        where each tuple is a session entry with
        host, username, password
        """
        sessions = []
        file = open('sessions.txt', 'r')

        for line in file:
            host, name, password = line.strip().split(',')
            sessions.append(tuple([host, name, password]))

        file.close()
        return sessions
