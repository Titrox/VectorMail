<script setup>

</script>

<template>

  <div class="container container--top">

    <div class="container--logo">
      <img src="../assets/logo.png" alt="logo">
    </div>

    <div class="container container--text">
      <p class="title"><b>Vectormail</b></p>
      <p>Entwickelt von <b> Tim Terbach </b></p>
    </div>



  </div>

</template>

<style scoped>

img {
  height: 80%;
  width: auto;
}

p {
  margin: 0;
}

.container--top {
  height: 15vh;
  width: 100%;
  background-color: #e0e0e0;

  box-shadow: rgba(0,0,0,0.2) 0 3px;

  position: fixed;
  display: flex;
  justify-content: left;
  align-items: center;
  flex-direction: row;

  padding-left: 2vw;
}

.container--text {
  display: flex;
  justify-content: space-around;
  align-items: start;
  flex-direction: column;
}

.container--logo {
  position: relative;
  height: 100%;

  display: flex;
  justify-content: center;
  align-items: center;
}


.title {
  font-size: 150%;
}

</style>