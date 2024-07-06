const textToTranslate = document.getElementById("textToTranslate");
const languages = document.getElementById("languages");
const translatorForm = document.getElementById("translatorForm");
const progressBar = document.getElementById("progressBar");
const translationResultCont = document.getElementById("translationResultCont");

translatorForm.addEventListener("submit", (e) => {
  e.preventDefault();
  translatorForm.querySelector("button").disabled = true;

  let progressBarPercent = 0;

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

  const interval = setInterval(() => {
    progressBarPercent += 10;
    progressBar.style.width = `${progressBarPercent}%`;

    if (progressBarPercent >= 100) {
      translationResultCont.classList.add("show");
      translationResultCont.classList.remove("hide");
      progressBarPercent = 0;
      progressBar.style.width = `${progressBarPercent}%`;
      progressBar.parentElement.style.height = "0";
      translatorForm.querySelector("button").disabled = false;

      clearInterval(interval);
    }
  }, 200);

  translatorForm.reset();
});
