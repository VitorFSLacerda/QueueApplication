class Call:

    def __init__(self, call_id):

        self.id = call_id
        self.status = 'received'


    def set_status(self, status):
        """Changes the call's status."""
        
        self.status = status