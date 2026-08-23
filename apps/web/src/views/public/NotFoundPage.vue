<template>
  <div class="section text-center">
    <div class="container">
      <span class="not-found__emoji">🔍</span>
      <h1>Página no encontrada</h1>
      <p>Lo sentimos, esta página no existe o fue movida.</p>
      <RouterLink to="/" class="btn btn--primary" style="margin-top: 2rem;">Volver al Inicio</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.not-found__emoji {
  font-size: 5rem;
  display: block;
  margin-bottom: 1rem;
}
</style>
