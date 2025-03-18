from twisted.protocols.basic import LineReceiver
from twisted.internet import protocol, reactor
from supportOperator import SupportOperator
from call import Call
import json


class CallCenterServer(LineReceiver):

    def __init__(self):
        self.operators = [SupportOperator('A'),  SupportOperator('B')]
        self.queue = []


    def lineReceived(self, line):
        """This method is called every time a line of data is received from the client."""

        try:
            data = json.loads(line.decode('utf-8'))
            command = data.get("command")
            id = data.get("id")
                
            if command == "call":
                self.do_call(id)
            elif command == "answer":
                self.do_answer(id)
            elif command == "reject":
                self.do_reject(id)
            elif command == "hangup":
                self.do_hangup(id)
            else:
                self.sendResponse("Invalid command")

        except json.JSONDecodeError:
            self.sendResponse("Error parsing JSON")
        except Exception as e:
            self.sendResponse(f"Error: {str(e)}")


    def sendResponse(self, response_message):
        """Sends the response to the client in JSON format."""

        response_data = {"response": response_message}
        self.sendLine(json.dumps(response_data).encode('utf-8'))

    
    def do_call(self, call_id):
        """Receives a call."""

        call = Call(call_id)
        call.set_status('received')
        self.sendResponse(f"Call {call_id} received")
        self.dispatch_call(call)


    def dispatch_call(self, call):
        """Attempts to assign the call to an available operator or puts it in the queue."""

        operator = next((op for op in self.operators if op.status == 'available'), None)

        if operator:
            operator.assign_call(call)
            self.sendResponse(f"Call {call.id} ringing for operator {operator.operator_id}")
            operator.timeout_call = reactor.callLater(10, self.check_timeout, operator, call.id)

        else:
            self.queue.append(call)
            self.sendResponse(f"Call {call.id} waiting in queue")


    def do_answer(self, operator_id):
        """The operator answers the call."""

        operator = next((op for op in self.operators if op.operator_id == operator_id), None)
        self.abort_timeout(operator)
        if operator and operator.status == 'ringing':
            operator.answer_call()
            self.sendResponse(f"Call {operator.call.id} answered by operator {operator_id}")


    def do_reject(self, operator_id):
        """The operator rejects a call."""

        operator = next((op for op in self.operators if op.operator_id == operator_id), None)
        
        if operator and operator.timeout_call and operator.timeout_call.active() and operator.status == 'ringing':
            self.abort_timeout(operator)
            operator.call.set_status('available')
            self.sendResponse(f"Call {operator.call.id} rejected by operator {operator_id}")
            next_call = operator.call
            operator.call = None
            operator.set_status('available')
            self.dispatch_call(next_call)


    def do_hangup(self, call_id):
        """Ends the call."""

        operator = next((op for op in self.operators if op.call and op.call.id == call_id), None)

        if operator:
            if operator.status != 'busy':
                self.sendResponse(f"Call {call_id} missed")
            else:
                self.sendResponse(f"Call {call_id} finished and operator {operator.operator_id} available")
            
            operator.call = None
            operator.set_status('available')
            self.verify_status()

        else:
            for call in self.queue:
                if call.id == call_id:
                    self.queue.remove(call)
            self.sendResponse(f"Call {call_id} missed")


    def verify_status(self):
        """Checks the operator's status."""

        if (self.operators[0].status == 'available' or self.operators[1].status == 'available') and self.queue:
            self.dispatch_call(self.next_queue_call())
    

    def next_queue_call(self):
        """Takes the next call from the queue and removes it from the queue."""

        if self.queue:
            return self.queue.pop(0)
        return None
    

    def check_timeout(self, operator, call_id):

        self.abort_timeout(operator)

        if operator.status == 'ringing' and operator.call and operator.call.id == call_id:
            self.sendResponse(f"Call {call_id} ignored by operator {operator.operator_id}")
            operator.call = None
            operator.set_status('available')
            self.verify_status()


    def abort_timeout(self, operator):
        
        if operator.timeout_call and operator.timeout_call.active():
            operator.timeout_call.cancel()
            operator.timeout_call = None


class CallCenterServerFactory(protocol.Factory):

    def buildProtocol(self, _):

        return CallCenterServer()  


def start_server():

    reactor.listenTCP(5678, CallCenterServerFactory())  
    reactor.run()


if __name__ == '__main__':
    start_server()
