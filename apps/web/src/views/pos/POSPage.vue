<template>
  <div class="section">
    <div class="container">
      <h1 v-motion-fade-visible>Punto de Venta</h1>
      <p class="section__subtitle">Interfaz POS para cajeros — cobros en efectivo, tarjeta, transferencia y monedero.</p>
      <!-- La implementación completa del POS será en Fase 4 -->
      <div class="pos-placeholder card">
        <span class="pos__icon">💳</span>
        <h3>POS en Construcción</h3>
        <p>El módulo de punto de venta con pago mixto estará disponible en la Fase 4.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pos-placeholder {
  max-width: 480px;
  margin: 2rem auto;
  text-align: center;
  padding: 3rem;
}
.pos__icon { font-size: 4rem; display: block; margin-bottom: 1rem; }
</style>
