<script setup>

import EmailInput from "@/components/EmailInput.vue";
import Background from "@/components/Background.vue";
import Header from "@/components/Header.vue";
</script>



<template>
  <Background>
    <Header />
    <EmailInput />
  </Background>
</template>



<style>

@import url('https://fonts.googleapis.com/css2?family=DynaPuff:wght@400..700&family=Jersey+25&display=swap');

html,
body {
  font-family: 'Jersey 25', Arial, sans-serif;
  margin: 0;
  border: none;
  width: 100vw;
  height: 100vh;

  overflow-y: hidden;
}



</style>
