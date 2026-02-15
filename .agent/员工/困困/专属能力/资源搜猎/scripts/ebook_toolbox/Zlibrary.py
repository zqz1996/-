class Zlibrary:
    def __init__(self, email=None, password=None, remix_userid=None, remix_userkey=None):
        self.email = email
        self.password = password
        self.remix_userid = remix_userid
        self.remix_userkey = remix_userkey

    def search(self, message, languages=None):
        _ = message
        _ = languages
        return {"books": []}

    def downloadBook(self, book):
        _ = book
        return ("", b"")
