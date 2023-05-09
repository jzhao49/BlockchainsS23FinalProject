from cryptography.exceptions import InvalidSignature

class Transaction:
    def __init__(self, sender, receiver, amount, signature=None):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = signature
    
    def sign(self, sender_sk):
        self.signature = sender_sk.sign(self.__str__().encode('utf-8'))

    def verify(self, sender_pk):
        try:
            sender_pk.verify(self.signature, self.__str__().encode('utf-8'))
            return True
        except InvalidSignature:
            return False

    def __repr__(self):
        return f"{self.sender} -> {self.receiver}: {self.amount}"

