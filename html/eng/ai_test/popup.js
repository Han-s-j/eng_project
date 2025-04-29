
  async function correctSentence(text) {
    const response = await fetch("https://api-inference.huggingface.co/models/pszemraj/grammar-correction", {
      method: "POST",
      headers: {
        Authorization: "Bhf_xxPmvbGwGHoOUlAWoawLTlZtESoMPSQBnR",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ inputs: text })
    });
  
    const data = await response.json();
    return data[0]?.generated_text || text;
  }
  
  // 🔧 편집거리(Levenshtein Distance) 기반 점수 계산
  function levenshtein(a, b) {
    const matrix = Array.from({ length: a.length + 1 }, () =>
      Array(b.length + 1).fill(0)
    );
  
    for (let i = 0; i <= a.length; i++) matrix[i][0] = i;
    for (let j = 0; j <= b.length; j++) matrix[0][j] = j;
  
    for (let i = 1; i <= a.length; i++) {
      for (let j = 1; j <= b.length; j++) {
        const cost = a[i - 1] === b[j - 1] ? 0 : 1;
        matrix[i][j] = Math.min(
          matrix[i - 1][j] + 1,
          matrix[i][j - 1] + 1,
          matrix[i - 1][j - 1] + cost
        );
      }
    }
  
    return matrix[a.length][b.length];
  }
  
  function getScore(original, corrected) {
    const distance = levenshtein(original.toLowerCase(), corrected.toLowerCase());
    const maxLen = Math.max(original.length, corrected.length);
    const accuracy = ((maxLen - distance) / maxLen) * 100;
    return Math.round(accuracy);
  }
  
  document.getElementById("checkBtn").addEventListener("click", async () => {
    const inputText = document.getElementById("inputSentence").value.trim();
    if (!inputText) {
      alert("문장을 입력해주세요!");
      return;
    }
  
    const corrected = await correctSentence(inputText);
    const score = getScore(inputText, corrected);
  
    document.getElementById("corrected").textContent = corrected;
    document.getElementById("score").textContent = `${score}점`;
  
    const feedback = (inputText === corrected)
      ? "정확하게 잘 썼어요! 👏"
      : "수정이 필요한 부분이 있어요. 다시 한 번 확인해볼까요?";
      
    document.getElementById("feedback").textContent = feedback;
    document.getElementById("result").style.display = "block";
  });
  
  