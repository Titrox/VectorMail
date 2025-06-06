<script setup>

</script>

<template>
  <body>
  <slot>
  </slot>
  </body>
</template>

<style scoped>
body {
  --dot-bg: #ececec;
  --dot-color: black;
  --dot-size: 1px;
  --dot-space: 22px;
  background:
      linear-gradient(90deg, var(--dot-bg) calc(var(--dot-space) - var(--dot-size)), transparent 1%) center / var(--dot-space) var(--dot-space),
      linear-gradient(var(--dot-bg) calc(var(--dot-space) - var(--dot-size)), transparent 1%) center / var(--dot-space) var(--dot-space),
      var(--dot-color);
}
</style>