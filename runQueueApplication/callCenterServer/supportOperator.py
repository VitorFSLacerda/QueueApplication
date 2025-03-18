class SupportOperator:

    def __init__(self, operator_id):

        self.operator_id = operator_id
        self.status = 'available'
        self.timeout_call = None
        self.call = None


    def set_status(self, status):
        """Changes the operator's status."""
        
        self.status = status


    def assign_call(self, call):
        """Assigns a call to the operator and changes their status and the call's status to ringing."""

        self.call = call
        self.call.set_status('ringing')
        self.set_status('ringing')
        

    def answer_call(self):
        """Changes the status of the call and the operator to busy."""

        self.call.set_status('busy')
        self.set_status('busy')
