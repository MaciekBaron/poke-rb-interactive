from pkmn.websockets import add_message
from pkmn.singleton import Singleton
from pkmn.wrapper import InteractivePkmn
from pkmn.actions import ACTIONS
from typing import Callable
import json
import time

@Singleton
class VoteManager():
    def __init__(self):
        self.points = {}

    def set_game_instance(self, game):
        self.game = game

    def set_current_poll(self, poll, duration = 30):
        assert isinstance(poll, Poll)
        self.poll = poll
        self.reset()
        self.is_poll_active = True
        self.end_time = time.time() + duration
        if isinstance(poll, OptionPoll):
            for option in poll.options:
                self.votes[option] = 0
        self.send_poll_state()

    def reset(self):
        self.users_voted = []
        self.votes = {}
        self.is_poll_active = False

    def cast_vote(self, user, vote):
        """Casts a vote by a given user."""
        if not self.is_poll_available():
            return
        vote = self.poll.validate_vote(vote)
        if vote and (user not in self.users_voted):
            if isinstance(self.poll, OptionPoll) and vote not in self.poll.options:
                try:
                    vote = self.poll.options[int(vote) - 1]
                except:
                    vote = vote.lower()
            if vote in self.votes:
                self.votes[vote] += 1
            else:
                self.votes[vote] = 1
            self.users_voted.append(user)
            self.send_poll_state()
            if user in self.points:
                self.points[user] += 1
            else:
                self.points[user] = 1

    def get_points_for_user(self, user):
        try:
            return self.points[user]
        except:
            return 0

    def spend_points(self, user, action, argument):
        try:
            points = self.points[user]
            if action in ACTIONS:
                selection = ACTIONS[action]
                if points >= selection.cost:
                    selection.execute(self.game, argument)
                    self.points[user] = points - selection.cost
                    return True
            return False
        except:
            return False

    def send_poll_state(self):
        state = {
            'question': self.poll.question,
            'votes': self.votes,
            'time_left': max(0, self.end_time - time.time())
        }

        if isinstance(self.poll, OptionPoll):
            state['descriptions'] = self.poll.descriptions
            state['type'] = 'option'
        else:
            state['type'] = self.poll.type
        add_message(json.dumps(state))

    def get_winning_option(self):
        """Returns the name of the winning option."""
        winning = None
        best_score = -1
        for vote in self.votes:
            if self.votes[vote] > best_score:
                winning = vote
                best_score = self.votes[vote]
        return winning

    def get_results(self):
        """Returns a dictionary with all votes."""
        return self.votes

    def activate_poll(self):
        self.is_poll_active = True

    def deactivate_poll(self):
        self.is_poll_active = False

    def get_current_question(self):
        return self.poll.question

    def is_poll_available(self):
        return self.is_poll_active and self.end_time > time.time()

    def resolve_poll(self, pkmn: InteractivePkmn):
        try:
            self.poll.resolve(pkmn, self.get_winning_option(), self.get_results())
        except:
            print("Could not resolve poll")


class Poll():
    def __init__(self, question, resolve: Callable[[InteractivePkmn, str], None]):
        self.question = question
        self.resolve = resolve

class OptionPoll(Poll):
    def __init__(self, question, resolve, options, descriptions):
        super().__init__(question=question, resolve=resolve)
        self.options = options
        self.descriptions = descriptions

    def validate_vote(self, answer):
        try:
            number = int(answer)
            if number > 0 and number <= len(self.options):
                return answer
        except:
            if answer.lower() in self.options:
                return answer

class OpenPoll(Poll):
    def __init__(self, question, resolve, validate, type):
        super().__init__(question=question, resolve=resolve)
        self.validate_vote = validate
        self.type = type

