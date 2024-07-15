const textToTranslate = document.getElementById("textToTranslate");
const languages = document.getElementById("languages");
const translatorForm = document.getElementById("translatorForm");
const progressBar = document.getElementById("progressBar");
const translationResultCont = document.getElementById("translationResultCont");
const translationID = document.getElementById("translationID");
const baseUrl = "http://127.0.0.1:8080";
let translationObj = {};

async function getStatus(taskId) {
  const status = await axios({
    method: "get",
    url: `${baseUrl}/translate/${taskId}`,
  });

  return status.data;
}

async function getTranslationResult(taskId) {
  translationObj = await getStatus(taskId);

  const p = document.createElement("p");
  p.innerText = `Translation ID: ${taskId}`;
  translationResultCont.append(p);

  if (translationObj.translation.length == 0) {
    const p = document.createElement("p");
    p.innerText = "No translation.";
    translationResultCont.appendChild(p);
  }

  translationObj.translation.forEach((translation) => {
    const p = document.createElement("p");
    const span1 = document.createElement("span");
    span1.innerText = `${Object.keys(translation)[0]?.toUpperCase()}: `;
    span1.classList.add("fw-bold");
    const span2 = document.createElement("span");
    span2.innerText = translation[Object.keys(translation)[0]];
    p.appendChild(span1);
    p.appendChild(span2);
    translationResultCont.appendChild(p);
  });
}

translatorForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  translatorForm.querySelector("button").disabled = true;

  let progressBarPercent = 0;
  translationResultCont.innerHTML = "";
  const p = document.createElement("p");
  p.innerHTML = "Translation Result: ";
  p.classList.add("fw-bold");
  translationResultCont.append(p);

  const textToTranslateVal = textToTranslate.value.trim();
  const languagesVal = languages.value.trim();

  if (!textToTranslateVal || !languagesVal) {
    alert("Please provide both text and language/s.");
    translatorForm.querySelector("button").disabled = false;
    return;
  }

  translationResultCont.classList.add("hide");
  translationResultCont.classList.remove("show");
  progressBar.parentElement.style.height = "";

  const reqVal = {
    text: textToTranslateVal,
    languages: languagesVal.split(","),
  };

  const res = await axios({
    method: "post",
    url: `${baseUrl}/translate`,
    data: reqVal,
  });

  const taskId = await res.data?.task_id;

  const interval = setInterval(async () => {
    progressBarPercent += 20;
    progressBar.style.width = `${progressBarPercent}%`;

    if (progressBarPercent >= 100) {
      translationResultCont.classList.add("show");
      translationResultCont.classList.remove("hide");
      progressBarPercent = 0;
      progressBar.style.width = `${progressBarPercent}%`;
      progressBar.parentElement.style.height = "0";
      translatorForm.querySelector("button").disabled = false;

      getTranslationResult(taskId);

      clearInterval(interval);
    }
  }, 200);

  translatorForm.reset();
});

async function checkStatus() {
  const translationIDVal = translationID.value;
  if (translationIDVal) {
    try {
      const res = await getStatus(translationIDVal);
      if (res.status) {
        alert(
          `Status for translation ID (${translationIDVal}) is: ${res.status.toUpperCase()}`
        );
      } else {
        alert("Invalid translation ID. Try again.");
      }
    } catch (e) {
      alert("Invalid translation ID. Try again.");
    }
  }
}

async function checkContent() {
  const translationIDVal = translationID.value;
  if (translationIDVal) {
    try {
      const res = await getStatus(translationIDVal);
      if (res.task_id) {
        let content = `Text to be translated: ${res.text}\nTranslations:`;
        res.translation.forEach((translation) => {
          const key = Object.keys(translation)[0];
          content += `\n${key.toUpperCase()}: ${translation[key]}`;
        });

        alert(
          `\nContent for translation ID (${translationIDVal}) is: \n${content}`
        );
        translationID.value = "";
      } else {
        alert("Invalid translation ID. Try again.");
      }
    } catch (e) {
      alert("Invalid translation ID. Try again.");
    }
  }
}
