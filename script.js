let questions = [];
let currentIndex = 0;

// Load questions from JSON
fetch("questions.json")
    .then(response => response.json())
    .then(data => {
        questions = data;
        showQuestion();
    });

function showQuestion() {
    let q = questions[currentIndex];
    document.getElementById("question-number").innerText = `Question ${q.question_number}`;
    document.getElementById("question-text").innerText = q.question;
    document.getElementById("category-title").innerText = q.categories[0];
    document.getElementById("question-image").src = q.image;
    
    let answersContainer = document.getElementById("answer-options");
    answersContainer.innerHTML = ""; 

    q.options.forEach(option => {
        let btn = document.createElement("button");
        btn.innerText = option.text;
        btn.style.background = option.correct ? "lightgreen" : "white";
        btn.disabled = true;  // Answers are displayed without selection
        answersContainer.appendChild(btn);
    });

    updateProgress();
}

function updateProgress() {
    let progress = (currentIndex + 1) / questions.length * 100;
    document.getElementById("progress-bar").style.width = `${progress}%`;
}

document.getElementById("next-btn").addEventListener("click", () => {
    if (currentIndex < questions.length - 1) {
        currentIndex++;
        showQuestion();
    }
});

document.getElementById("prev-btn").addEventListener("click", () => {
    if (currentIndex > 0) {
        currentIndex--;
        showQuestion();
    }
});
