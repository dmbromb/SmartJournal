document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("ai-question-form");
  const answersContainer = document.getElementById("ai-answers");

  form.addEventListener("submit", function(event) {
    event.preventDefault();

    const formData = new FormData(form);
    const question = formData.get("ai_question");

    fetch(form.action, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ai_question: question })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        const answerElement = createAnswerElement(question, data.answer);
        answersContainer.appendChild(answerElement);
        form.reset(); // Clear the input field after submission
        answersContainer.scrollTop = answersContainer.scrollHeight; // Scroll to the bottom
      } else {
        console.error("There was an error processing your request.");
      }
    })
    .catch(error => {
      console.error("Error:", error);
    });
  });

  function createAnswerElement(question, answer) {
    const chatItem = document.createElement("div");
    chatItem.classList.add("chat-item");

    const questionElement = document.createElement("div");
    questionElement.classList.add("chat-bubble", "chat-bubble-question");
    questionElement.textContent = question;

    const answerElement = document.createElement("div");
    answerElement.classList.add("chat-bubble", "chat-bubble-answer");
    answerElement.textContent = answer;

    chatItem.appendChild(questionElement);
    chatItem.appendChild(answerElement);

    return chatItem;
  }
});
