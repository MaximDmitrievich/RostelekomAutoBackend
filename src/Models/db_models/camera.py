class Camera:
    def __init__(self, id=None, long=None, lat=None, url=None, address=None):
        self.__id = id
        self.__long = long
        self.__lat = lat
        self.__url = url
        self.__address = address
        self.__b64str = b''

    @property
    def id(self):
        return self.__id

    @property
    def address(self):
        return self.__address

    @property
    def url(self):
        return self.__url

    @property
    def geodot(self):
        return (self.__lat, self.__long)
    
    @property
    def b64str(self):
        return self.__b64str

    @b64str.setter
    def b64str(self, value):
        self.__b64str = value