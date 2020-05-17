const app = new Vue({
  el: '#app',
  data: {
    message: 'Connecting...',
    question: '',
    visibleQuestion: '',
    options: [],
    timeLeft: 0,
    suggestion: '',
    pollType: '',
  },
});

let questionTimeout;

setInterval(() => {
  app.timeLeft = Math.max(0, app.timeLeft - .1);
}, 100);

const showQuestion = (count) => {
  clearInterval(questionTimeout);
  count += 1;
  app.visibleQuestion = app.question.substr(0, count);

  if (app.visibleQuestion.length < app.question.length) {
    questionTimeout = setTimeout(() => showQuestion(count), 50);
  }
};

const updatePoll = (data) => {
  if (app.question != data.question || data.time_left > app.timeLeft) {
    app.question = data.question;
    showQuestion(0);
  }
  const options = [];
  let i = 0;
  for (let key in data.votes) {
    i += 1;
    options.push({
      label: key,
      votes: data.votes[key],
      index: i,
      description: (data.descriptions) ? data.descriptions[i - 1]: '',
    });
  }

  if (data.type == 'open' || data.type == 'monster') {
    app.suggestion = 'banana';
  } else {
    app.suggestion = options[0].label;
  }

  options.sort((a, b) => b.votes - a.votes);
  app.options = options;

  app.timeLeft = data.time_left;
  console.log(data.time_left)
  app.pollType = data.type;
}

const onMessage = (msg) => {
  if (msg.data === "alive") {
    return;
  }
  try {
    const data = JSON.parse(msg.data);
    updatePoll(data);
    app.message = '';
  } catch {}
};

const webSocket = new WebSocket('ws://localhost:8765');
webSocket.addEventListener("message", (msg) => onMessage(msg));
