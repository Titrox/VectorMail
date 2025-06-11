<script setup>
import { ChevronLeft, ChevronRight, MailQuestion } from 'lucide-vue-next';
import {onMounted, ref, watch} from "vue";
import emailsData from '../assets/example_emails.json';
import axios from "axios";

// Backend API URL
const springBootUrl = "http://localhost:8080";

// Example email and index
let exampleEmail = ref("");
let emailIndex;

// User input (editable)
let userEmail = ref("");

// UI state: whether to show probability labels
let showLabelProbs = ref(false);

// Final classification scores (to be updated by backend)
let lableProbs = [0.00,0.00,0.00,0.00,0.00];

// Classification categories (must match backend keys)
const labelsAndOriginalIndices = [
  'Kfz-Schaden',
  'Hausrat-Schaden',
  'Haftpflicht',
  'Reiseschaden',
  'Tierkrankheit',
];

// Animated values for smooth progress display
let animatedLabelProbs = ref(Array(labelsAndOriginalIndices.length).fill(0.00));

// Load first random example email on mount
onMounted(() => {
  exampleEmail.value = getRandomEmail();
});


// Hide label probabilities if user changes custom email
watch(userEmail, (newValue, oldValue) => {

  if (newValue !== oldValue) {
    showLabelProbs.value = false;
  }

});


//
// EXAMPLE EMAIL SLIDER
//

function getRandomEmail() {
  emailIndex = Math.floor(Math.random() * emailsData.length);
  return getExampleEmail(emailIndex);
}

function getExampleEmail(index) {
  userEmail.value = "";
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

async function evaluateEmail() {
  const emailToEvaluate = userEmail.value || exampleEmail.value;

  if (!emailToEvaluate) {
    console.warn("No email provided for evaluation.");
    return;
  }

  await getProbs(emailToEvaluate);
  startLabelProbabilitiesAnimation();
}

// Call Spring Boot backend to get classification results
async function getProbs(emailToEvaluate) {
  try {
    const response = await axios.post(
        `${springBootUrl}/evaluate-email`,
        emailToEvaluate,
        {
          headers: {
            'Content-Type': 'application/json' // Otherwise Content-Type = Plain-Text -> error because flask is expecting JSON on /evaluate-email
          }
        }
    );
    updateProbs(response.data);
  } catch (e) {
    alert(`Verbindung zum Backend gescheitert: ${e.message}. \n Läuft Springboot? Läuft Docker?`)
  }
}

// Update label probability array with backend response
function updateProbs(labelProbsJson) {
  labelsAndOriginalIndices.forEach((label, index) => {
    console.log(label);
    lableProbs[index] = labelProbsJson[label] ?? 0.00;
  });
}


//
// ANIMATION
//

function startLabelProbabilitiesAnimation() {
  showLabelProbs.value = true;
  const duration = 1500;

  animatedLabelProbs.value = Array(labelsAndOriginalIndices.length).fill(0.00);

  labelsAndOriginalIndices.forEach((_, displayIndex) => {
    const targetValue = lableProbs[displayIndex];
    const startValue = 0.00;
    const startTime = performance.now();

    const animateStep = (currentTime) => {
      const elapsedTime = currentTime - startTime;
      let progress = Math.min(elapsedTime / duration, 1);

      // Ease-out interpolation
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

// Map a probability (0–100) to an HSL color (red → green)
function getColorForProbability(prob) {
  const clampedProb = Math.max(0, Math.min(100, prob));
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

        <div class="container container--label-prob" v-for="(label, displayIndex) in labelsAndOriginalIndices" :key="label">
          <div class="label"
               :class="{ 'animated-label': !showLabelProbs }"
               :style="showLabelProbs ? {
                 backgroundColor: getColorForProbability(animatedLabelProbs[displayIndex])
               } : {
                 animationDelay: `${displayIndex * 150}ms` // Wave effect
               }">
            {{ label }}
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
  transition: opacity 0.3s ease, transform 0.3s ease
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
*/

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