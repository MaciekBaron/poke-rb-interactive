class VoteManager():
  def set_current_poll(self, poll):
    assert isinstance(poll, Poll)
    self.poll = poll
    self.reset()
    self.is_poll_active = True

  def reset(self):
    self.users_voted = []
    self.votes = {}
    self.is_poll_active = False

  def cast_vote(self, user, vote):
    """Casts a vote by a given user."""
    if (self.poll.validate_vote(vote)) and (user not in self.users_voted):
      if vote in self.votes:
        self.votes[vote] += 1
      else:
        self.votes[vote] = 1
      self.users_voted.append(user)

  def get_winning_option(self):
    """Returns the name of the winning option."""
    winning = None
    best_score = 0
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
    return self.poll.get_question()

class Poll():
  def __init__(self, question, validate):
    self.question = question
    self.validate_vote = validate

  def get_question(self):
    return self.question

good_or_bad_poll = Poll(
  "Do a good or bad thing to the player?",
  lambda answer: answer in ('good', 'bad')
)
