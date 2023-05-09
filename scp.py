class SCPNode:
    class State:
        INIT = 0
        PREPARED = 1
        COMMITTED = 2
        EXTERNALIZED = 3
    
    def __init__(self, node_id, threshold=1):
        self.node_id = node_id
        self.state = SCPNode.State.INIT
        self.ballot_protocol = None
        self.value_to_ballot = {}
        self.threshold = threshold
        self.validators = set()
        self.quorum_slices = []

    def add_vote(self, slot_index, value):
        if slot_index not in self.nomination_protocol_state:
            self.nomination_protocol_state[slot_index] = {'votes': set(), 'accepted': set()}
        self.nomination_protocol_state[slot_index]['votes'].add(value)

    def add_validator_set(self, validators):
        """
        Add a set of validators as a quorum slice.

        :param validators: A list of SCPNode instances.
        """
        if len(validators) >= self.threshold:
            self.quorum_slices.append(set(validators))

    def nominate(self, slot_index, value):
        self.add_vote(slot_index, value)
        message = SCPMessage(
            message_type='nominate',
            sender=self.node_id,
            slot_index=slot_index,
            quorum_slice=self.quorum_slices[0],
            value=value
        )
        return message

    def receive_message(self, message):
        if message.message_type == 'nominate':
            self.process_nomination_protocol(message)
        elif message.message_type == 'ballot':
            self.process_ballot_protocol(message)

    def process_nomination_protocol(self, message):
        slot_index = message.slot_index
        value = message.value
        quorum_slice = message.quorum_slice

        self.add_vote(slot_index, value)

        # Check if the value is accepted by a quorum slice
        if self.node_id in quorum_slice.validator_set and self.is_accepted_by_quorum_slice(slot_index, value, quorum_slice):
            self.nomination_protocol_state[slot_index]['accepted'].add(value)

        # Broadcast a new nomination message if the value is not already accepted by the node
        if value not in self.nomination_protocol_state[slot_index]['accepted']:
            new_message = SCPMessage(
                message_type='nominate',
                sender=self.node_id,
                slot_index=slot_index,
                quorum_slice=self.quorum_slices[0],
                value=value
            )
            return new_message

    def process_ballot_protocol(self, message):
        slot_index = message.slot_index
        ballot = message.ballot
        quorum_slice = message.quorum_slice
        ballot_state = self.ballot_protocol_state.get(slot_index)

        if not ballot_state:
            # Initialize the ballot state for this slot index
            self.ballot_protocol_state[slot_index] = {
                'current_ballot': None,
                'preparing': None,
                'prepared': None,
                'committing': None,
                'committed': None,
                'externalized': None
            }
            ballot_state = self.ballot_protocol_state[slot_index]

        if message.message_type == 'prepare':
            self.process_prepare(ballot_state, message, quorum_slice)

        elif message.message_type == 'commit':
            self.process_commit(ballot_state, message, quorum_slice)

        elif message.message_type == 'externalize':
            self.process_externalize(ballot_state, message, quorum_slice)

    def process_prepare(self, ballot_state, message, quorum_slice):
        # Implementation of the prepare sub-protocol
        pass

    def process_commit(self, ballot_state, message, quorum_slice):
        # Implementation of the commit sub-protocol
        pass

    def process_externalize(self, ballot_state, message, quorum_slice):
        # Implementation of the externalize sub-protocol
        pass

    def is_accepted_by_quorum_slice(self, slot_index, value, quorum_slice):
        count = 0
        for node in quorum_slice.validator_set:
            if node == self.node_id:
                continue
            if node.nomination_protocol_state.get(slot_index, {}).get('votes', None) and value in node.nomination_protocol_state[slot_index]['votes']:
                count += 1
            if count >= quorum_slice.threshold:
                return True
        return False

class QuorumSlice:
    def __init__(self, threshold, validator_set):
        self.threshold = threshold
        self.validator_set = validator_set

    def contains(self, node_id):
        return node_id in self.validator_set

    def is_quorum(self, node_set):
        count = 0
        for node in self.validator_set:
            if node.node_id in node_set:
                count += 1
            if count >= self.threshold:
                return True
        return False

class SCPMessage:
    def __init__(self, message_type, sender, slot_index, quorum_slice, value=None, ballot=None):
        self.message_type = message_type
        self.sender = sender
        self.slot_index = slot_index
        self.quorum_slice = quorum_slice
        self.value = value
        self.ballot = ballot

    def to_dict(self):
        message_dict = {
            'message_type': self.message_type,
            'sender': self.sender,
            'slot_index': self.slot_index,
            'quorum_slice': {
                'threshold': self.quorum_slice.threshold,
                'validator_set': [node.node_id for node in self.quorum_slice.validator_set]
            }
        }
        if self.value is not None:
            message_dict['value'] = self.value
        if self.ballot is not None:
            message_dict['ballot'] = {
                'counter': self.ballot.counter,
                'value': self.ballot.value
            }
        return message_dict

    @classmethod
    def from_dict(cls, message_dict, nodes):
        quorum_slice_dict = message_dict['quorum_slice']
        quorum_slice = QuorumSlice(
            threshold=quorum_slice_dict['threshold'],
            validator_set=[nodes[node_id] for node_id in quorum_slice_dict['validator_set']]
        )
        ballot_dict = message_dict.get('ballot')
        ballot = None
        if ballot_dict:
            ballot = SCPBallot(
                counter=ballot_dict['counter'],
                value=ballot_dict['value']
            )
        return cls(
            message_type=message_dict['message_type'],
            sender=message_dict['sender'],
            slot_index=message_dict['slot_index'],
            quorum_slice=quorum_slice,
            value=message_dict.get('value'),
            ballot=ballot
        )

class SCPBallot:
    def __init__(self, counter, value):
        self.counter = counter
        self.value = value

    def __eq__(self, other):
        if not isinstance(other, SCPBallot):
            return False
        return self.counter == other.counter and self.value == other.value

    def __lt__(self, other):
        if not isinstance(other, SCPBallot):
            return NotImplemented
        if self.counter < other.counter:
            return True
        if self.counter == other.counter:
            return self.value < other.value
        return False

    def __le__(self, other):
        if not isinstance(other, SCPBallot):
            return NotImplemented
        return self == other or self < other

    def __gt__(self, other):
        if not isinstance(other, SCPBallot):
            return NotImplemented
        return not self <= other

    def __ge__(self, other):
        if not isinstance(other, SCPBallot):
            return NotImplemented
        return self == other or self > other

    def __repr__(self):
        return f"SCPBallot(counter={self.counter}, value={self.value})"
