document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("ai-question-form");
  const answerContainer = document.getElementById("ai-answer");
  const answerContent = document.getElementById("ai-answer-content");

  form.addEventListener("submit", function(event) {
    event.preventDefault();

    const formData = new FormData(form);
    const question = formData.get("ai_question");

    fetch(form.action, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": formData.get("csrf_token")
      },
      body: JSON.stringify({ ai_question: question })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        answerContent.textContent = data.answer;
        answerContainer.style.display = "block";
      } else {
        answerContent.textContent = "There was an error processing your request.";
        answerContainer.style.display = "block";
      }
    })
    .catch(error => {
      console.error("Error:", error);
      answerContent.textContent = "There was an error processing your request.";
      answerContainer.style.display = "block";
    });
  });
});
