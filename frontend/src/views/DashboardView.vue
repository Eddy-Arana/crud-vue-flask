<template>
  <div class="text-center">
    <h1>Sistema CRUD</h1>

    <p class="lead">
      Aplicación de gestión de clientes, productos y pedidos.
    </p>

    <div class="row mt-4">
      <div class="col-md-4 mb-3">
        <div class="card">
          <div class="card-body">
            <h5>Clientes</h5>
            <router-link
              to="/clientes"
              class="btn-menta"
            >
              Administrar
            </router-link>
          </div>
        </div>
      </div>

      <div class="col-md-4 mb-3">
        <div class="card">
          <div class="card-body">
            <h5>Productos</h5>
            <router-link
              to="/productos"
              class="btn-menta"
            >
              Administrar
            </router-link>
          </div>
        </div>
      </div>

      <div class="col-md-4 mb-3">
        <div class="card">
          <div class="card-body">
            <h5>Pedidos</h5>
            <router-link
              to="/pedidos"
              class="btn-menta"
            >
              Administrar
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.btn-menta {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 6px;
  background-color: #5eead4;
  border: 1px solid #5eead4;
  color: #134e4a;
  text-decoration: none;
  font-weight: 500;
}

.btn-menta:hover {
  background-color: #2dd4bf;
  border-color: #2dd4bf;
  color: #134e4a;
}
</style>