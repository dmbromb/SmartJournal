document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("ai-question-form");
  const answersContainer = document.getElementById("ai-answers");
  const clearButton = document.getElementById("clear-button");
  let conversation_history = [];

  form.addEventListener("submit", function(event) {
    event.preventDefault();

    const formData = new FormData(form);
    const question = formData.get("ai_question");

    conversation_history.push({ role: "user", content: question });

    fetch(form.action, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ai_question: question, conversation_history: conversation_history })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        const chatItem = createAnswerElement(question, data.answer);
        answersContainer.appendChild(chatItem);
        conversation_history.push({ role: "assistant", content: data.answer });
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

  clearButton.addEventListener("click", function() {
    answersContainer.innerHTML = '';
    conversation_history = [];
  });

  function createAnswerElement(question, answer) {
    const chatItem = document.createElement("div");
    chatItem.classList.add("chat-item");

    const questionElement = document.createElement("div");
    questionElement.classList.add("chat-bubble", "chat-bubble-question");
    questionElement.textContent = question;

    const answerElement = document.createElement("div");
    answerElement.classList.add("chat-bubble", "chat-bubble-answer");
    chatItem.appendChild(questionElement);
    chatItem.appendChild(answerElement);

    typeText(answer, answerElement);

    return chatItem;
  }

  function typeText(text, element) {
    element.textContent = "";
    let index = 0;
    const speed = 10; // Adjust the speed of typing here (lower value = faster typing)

    function type() {
      if (index < text.length) {
        element.textContent += text.charAt(index);
        index++;
        setTimeout(type, speed);
      }
    }

    type();
  }
});




