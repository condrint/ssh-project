class Sessions():
    def __init__(self):
        self.key = 'asdfasdf'

    def storeSession(self, host, username='', password=''):
        """
        saves a session
        returns true if successful
        """ 
        file = open('sessions.txt', 'a', encoding='latin-1')
        file.write('%s,%s,%s\n' % (self._encode(host), self._encode(username), self._encode(password)))
        file.close()
    
    def getSessions(self):
        """
        returns a list of tuples
        where each tuple is a session entry with
        host, username, password
        """
        sessions = []
        file = open('sessions.txt', 'r', encoding='latin-1')

        for line in file:
            if not line.strip():
                continue
            host, username, password = line.strip().split(',')
            sessions.append(tuple([self._decode(host), self._decode(username), self._decode(password)]))

        file.close()
        return sessions

    def _encode(self, string):
        key = self.key

        encoded_chars = []
        for i in range(len(string)):
            key_c = key[i % len(key)]
            encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
            encoded_chars.append(encoded_c)
        encoded_string = "".join(encoded_chars)
        return encoded_string

    def _decode(self, string):
        key = self.key

        encoded_chars = []
        for i in range(len(string)):
            key_c = key[i % len(key)]
            encoded_c = chr(ord(string[i]) - ord(key_c) % 256)
            encoded_chars.append(encoded_c)
        encoded_string = "".join(encoded_chars)
        return encoded_string
"""
s = Sessions()
s.storeSession('hi','how','are')
print(s.getSessions())
"""
