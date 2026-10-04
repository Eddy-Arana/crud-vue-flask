<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <router-link
          class="navbar-brand"
          to="/"
        >
          Sistema CRUD
        </router-link>

        <div class="navbar-nav">
          <router-link
            class="nav-link"
            to="/clientes"
          >
            Clientes
          </router-link>

          <router-link
            class="nav-link"
            to="/productos"
          >
            Productos
          </router-link>

          <router-link
            class="nav-link"
            to="/pedidos"
          >
            Pedidos
          </router-link>
        </div>
      </div>
    </nav>

    <main class="container py-4">
      <router-view />
    </main>
  </div>
</template>

<script setup>
</script>