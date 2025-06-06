<script setup>
import { ChevronLeft, ChevronRight, MailQuestion} from 'lucide-vue-next';
import {onMounted, ref} from "vue";
import emailsData from '../assets/example_emails.json'; // Stelle sicher, dass der Pfad korrekt ist

// Example E-Mail
let exampleEmail = ref("");
let emailIndex;

// User E-Mail (reaktiv machen für v-model)
let userEmail = ref("");

// State Management
let showLabelProbs = ref(false);

// Die Ziel-Prozentwerte für die Labels (8 Werte, wie im Original-Array)
let lableProbs = [79.00,2.00,5.00,19.00,1.56,2.44,0.27,0.73];

// Die Namen der Labels und ihre entsprechenden Indizes im lableProbs-Array
const labelsAndOriginalIndices = [
  { name: 'Schadensmeldung', probIndex: 0 },
  { name: 'Vertragsänderung', probIndex: 1 },
  { name: 'Rückfragen', probIndex: 2 },
  { name: 'Bewerbung', probIndex: 3 },
  { name: 'Kündigung', probIndex: 4 },
  { name: 'Spam', probIndex: 5 },
  { name: 'Sonstiges', probIndex: 6 }
];


let animatedLabelProbs = ref(Array(labelsAndOriginalIndices.length).fill(0.00));


// Life Cycle Hooks
onMounted(() => {
  exampleEmail.value = getRandomEmail();
});


//
// EXAMPLE EMAIL SLIDER
//

// Triggered on mount to load random example email
function getRandomEmail() {
  emailIndex = Math.floor(Math.random() * emailsData.length);
  return getExampleEmail(emailIndex);
}

function getExampleEmail(index){
  userEmail.value = ""; // E-Mail des Benutzers leeren beim Laden eines Beispiels
  return emailsData[index].text;
}

function positiveModulo(n, m) {
  return ((n % m) + m) % m;
}

function incEmailIndex() {
  emailIndex = positiveModulo(emailIndex + 1, emailsData.length);
  exampleEmail.value = getExampleEmail(emailIndex);

  showLabelProbs.value = false;

}

function decEmailIndex() {
  emailIndex = positiveModulo(emailIndex - 1, emailsData.length);
  exampleEmail.value = getExampleEmail(emailIndex);

  showLabelProbs.value = false;
}


//
// EVALUATION
//

function evaluateEmail() {
  const emailToEvaluate = userEmail.value || exampleEmail.value;

  if (!emailToEvaluate) {
    console.warn("Keine E-Mail zum Evaluieren vorhanden.");
    return;
  }

  console.log(emailToEvaluate);

  // Hier würde die eigentliche Modell-Evaluierung stattfinden.
  // const probabilities = await evaluate(emailToEvaluate);
  // Wenn die Probabilities vom Modell dynamisch kommen, müssten sie hier lableProbs aktualisieren.
  // lableProbs = probabilities; // <-- Wenn lableProbs auch ein ref wäre und dynamisch gesetzt wird.

  startLabelProbabilitiesAnimation();
}


//
// ANIMATION
//

function startLabelProbabilitiesAnimation() {
  showLabelProbs.value = true;
  const duration = 1500; // 1.5 Sekunden für die Animation

  // Setze animierte Werte vor Start der Animation auf 0 zurück
  animatedLabelProbs.value = Array(labelsAndOriginalIndices.length).fill(0.00);

  labelsAndOriginalIndices.forEach((labelInfo, displayIndex) => {
    const targetValue = lableProbs[labelInfo.probIndex]; // Zugriff auf den richtigen Wert im lableProbs-Array
    const startValue = 0.00;
    const startTime = performance.now();

    const animateStep = (currentTime) => {
      const elapsedTime = currentTime - startTime;
      let progress = Math.min(elapsedTime / duration, 1);

      // Die Interpolationsfunktion: cubic ease-out
      progress = 1 - Math.pow(1 - progress, 3);

      const currentValue = startValue + (targetValue - startValue) * progress;

      animatedLabelProbs.value[displayIndex] = parseFloat(currentValue.toFixed(2));

      if (progress < 1) {
        requestAnimationFrame(animateStep);
      }
    };
    requestAnimationFrame(animateStep);
  });
}

// Funktion zum Mappen einer Wahrscheinlichkeit auf eine HSL-Farbe (Rot zu Grün)
function getColorForProbability(prob) {

  // Wahrscheinlichkeit auf den Bereich 0-100 klemmen
  const clampedProb = Math.max(0, Math.min(100, prob));

  // Wahrscheinlichkeit auf den Farbton (Hue) mappen (0 = Rot, 120 = Grün)
  const hue = (clampedProb / 100) * 120;

  const saturation = 50;
  const lightness = 45;

  return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
}

</script>

<template>
  <div class="container container-page-container">
    <div class="container container--email-label">
      <div class="container container--lable-container">

        <div class="container container--label-prob" v-for="(labelInfo, displayIndex) in labelsAndOriginalIndices" :key="labelInfo.name">
          <div class="label"
               :class="{ 'animated-label': !showLabelProbs }"
               :style="showLabelProbs ? { backgroundColor: getColorForProbability(animatedLabelProbs[displayIndex]) } : {}">
            {{ labelInfo.name }}
          </div>

          <div
              class="label-prob"
              :class="{ 'label-prob--visible': showLabelProbs }"
              v-show="true"
              :style="{ transitionDelay: `${displayIndex * 120}ms` }"
          >
            <p>{{ animatedLabelProbs[displayIndex] }}%</p>
          </div>
        </div>

      </div>


      <div class="container container--email-input">

        <div style="color: rgba(0,0,0,0.5); font-size: 80%">Probiere <b>Vectormail</b> mit Beispiel E-Mails oder verfasse eine eigene</div>
        <div style="color: rgba(0,0,0,0.5); font-size: 80%">Beim Schreiben einer eigenen E-Mail betrachte die Hinweise der <b>README.md</b>.</div>

        <textarea class="textarea textarea--email-input" :placeholder="exampleEmail" v-model="userEmail"></textarea>

        <div class="container container--mail-select">

          <ChevronLeft
              class="clickable-icon icon--left-arrow"
              size="32"
              @click="decEmailIndex"
          />

          <ChevronRight
              class="clickable-icon icon--right-arrow"
              size="32"
              @click="incEmailIndex"
          />

        </div>

      </div>

      <button class="button button--classify" @click="evaluateEmail()">
        Klassifizieren
        <MailQuestion/>
      </button>


    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=DynaPuff:wght@400..700&family=Jersey+25&display=swap');

/**
Container
 */

.container-page-container {
  padding-top: 4vh; /* Place for header */
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.container--email-label {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 5vh;
}


.container--label-prob {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.container--email-input {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  gap: 1vh
}

.container--lable-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  gap: 3vw;
}

.container--mail-select {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-direction: row;

  height: 3vh;
  width: 3vw;
  border-radius: 30px;
  background-color: white;
  box-shadow: rgba(0,0,0,0.2) 3px 3px;
}





/**
Label
 */

.label {
  padding: 1vh 1vw;
  border-radius: 10px;
  /* Die ursprüngliche background-color wird von der Animation überschrieben */
  background-color: #b93d3d; /* Diese Farbe ist jetzt der Startpunkt, falls die Animation nicht sofort lädt oder nicht unterstützt wird */

}


.label-prob {
  opacity: 0;
  transform: translateY(-10px);
  transition: opacity 0.5s ease, transform 0.5s ease
}

.label-prob--visible {
  opacity: 1;
  transform: translateY(0);
}

/* --- Animation Definition --- */
@keyframes pendulum-color {
  0% {
    background-color: #b93d3d; /* Castell Rot */
  }
  50% {
    background-color: #00B050; /* Castell Grün */
  }
  100% {
    background-color: #b93d3d; /* Zurück zu Castell Rot */
  }
}

/* --- Anwendung der Animation --- */
.animated-label {
  animation: pendulum-color 10s infinite alternate ease-in-out;
}



/**
Input
 */

.textarea--email-input {
  width: 40vw;
  height: 30vh;
  padding: 1vh;
  resize: none;
  border-radius: 10px;
  font-family: 'Jersey 25', Arial, sans-serif;
  font-size: 120%;
  box-shadow: rgba(0,0,0,0.2) 3px 3px;
}


/**
BUTTONS
**/

.button--classify {
  height: 5vh;
  width: 10vw;
  border: none;
  border-radius: 10px;
  background-color: #00B050;
  font-family: 'Jersey 25', Arial, sans-serif;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

}


.button--classify:hover {
  cursor: pointer;
  background-color: #008c40;
}

/**
Icons
 */


.clickable-icon:hover {
  cursor: pointer;
  transform: scale(110%);
}

</style>