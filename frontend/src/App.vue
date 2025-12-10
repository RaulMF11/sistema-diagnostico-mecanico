<script setup></script>

<!-- <template>
  <h1>You did it!</h1>
  <p>
    Visit <a href="https://vuejs.org/" target="_blank" rel="noopener">vuejs.org</a> to read the
    documentation
  </p>
</template> -->

<template>
  <div id="app">
    <h1>Sistema de Diagnóstico Mecánico</h1>
    <DiagnosticoForm />
  </div>
</template>

<script>
import DiagnosticoForm from './components/DiagnosticoForm.vue'

export default {
  name: 'App',
  components: { DiagnosticoForm }
}
</script>
