<template>
  <div>
    <h1>Pedidos</h1>

    <form @submit.prevent="guardarPedido">
      <h2>{{ editando ? "Editar pedido" : "Nuevo pedido" }}</h2>

      <label for="cliente">
        Cliente
      </label>

      <select
        id="cliente"
        v-model.number="form.cliente_id"
      >
        <option value="">
          Seleccione un cliente
        </option>

        <option
          v-for="cliente in clientes"
          :key="cliente.id"
          :value="cliente.id"
        >
          {{ cliente.nombre }}
        </option>
      </select>

      <br /><br />

      <label for="producto">
        Producto
      </label>

      <select
        id="producto"
        v-model.number="form.producto_id"
      >
        <option value="">
          Seleccione un producto
        </option>

        <option
          v-for="producto in productos"
          :key="producto.id"
          :value="producto.id"
        >
          {{ producto.nombre }}
        </option>
      </select>

      <br /><br />

      <FormField
        v-model="form.cantidad"
        name="cantidad"
        label="Cantidad"
        type="number"
        placeholder="Ingrese la cantidad"
        :error="errores.cantidad"
      />

      <label for="estado">
        Estado
      </label>

      <select
        id="estado"
        v-model="form.estado"
      >
        <option value="pendiente">
          Pendiente
        </option>

        <option value="pagado">
          Pagado
        </option>

        <option value="enviado">
          Enviado
        </option>

        <option value="cancelado">
          Cancelado
        </option>
      </select>

      <br /><br />

      <button
        type="submit"
        :disabled="guardando"
      >
        {{
          guardando
            ? "Guardando..."
            : editando
              ? "Actualizar"
              : "Guardar"
        }}
      </button>

      <button
        v-if="editando"
        type="button"
        @click="cancelarEdicion"
      >
        Cancelar
      </button>
    </form>

    <AlertMessage
  :message="mensaje"
  type="success"
/>

<AlertMessage
  :message="error"
  type="danger"
/>

    <hr />

    <p v-if="loading">
      Cargando pedidos...
    </p>

    <DataTable
      v-if="!loading"
      :items="pedidos"
      :columns="columns"
      @edit="editarPedido"
      @delete="eliminarPedido"
    />
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import DataTable from "../components/DataTable.vue";
import FormField from "../components/FormField.vue";
import AlertMessage from "../components/AlertMessage.vue";
import api from "../services/api";

const pedidos = ref([]);
const clientes = ref([]);
const productos = ref([]);

const loading = ref(false);
const guardando = ref(false);
const editando = ref(false);

const error = ref("");
const mensaje = ref("");

const errores = reactive({
  cantidad: "",
});

const form = reactive({
  id: null,
  cliente_id: "",
  producto_id: "",
  cantidad: "",
  estado: "pendiente",
});

const columns = [
  {
    key: "id",
    label: "ID",
  },
  {
    key: "cliente",
    label: "Cliente",
  },
  {
    key: "producto",
    label: "Producto",
  },
  {
    key: "cantidad",
    label: "Cantidad",
  },
  {
    key: "estado",
    label: "Estado",
  },
  {
    key: "total",
    label: "Total",
  },
];

function limpiarFormulario() {
  form.id = null;
  form.cliente_id = "";
  form.producto_id = "";
  form.cantidad = "";
  form.estado = "pendiente";

  errores.cantidad = "";
}

function validarFormulario() {
  errores.cantidad = "";
  error.value = "";

  let valido = true;

  if (!form.cliente_id) {
    error.value = "Debe seleccionar un cliente.";
    valido = false;
  }

  if (!form.producto_id) {
    if (error.value) {
      error.value += " Debe seleccionar un producto.";
    } else {
      error.value = "Debe seleccionar un producto.";
    }

    valido = false;
  }

  if (
    form.cantidad === "" ||
    !Number.isInteger(Number(form.cantidad)) ||
    Number(form.cantidad) <= 0
  ) {
    errores.cantidad =
      "La cantidad debe ser un entero mayor que cero.";

    valido = false;
  }

  return valido;
}

async function cargarDatos() {
  loading.value = true;
  error.value = "";

  try {
    const [clientesResponse, productosResponse, pedidosResponse] =
      await Promise.all([
        api.get("/clientes"),
        api.get("/productos"),
        api.get("/pedidos"),
      ]);

    clientes.value = clientesResponse.data;
    productos.value = productosResponse.data;
    pedidos.value = pedidosResponse.data;
  } catch (err) {
    console.error(err);

    error.value =
      "No se pudieron cargar los datos de pedidos.";
  } finally {
    loading.value = false;
  }
}

function editarPedido(pedido) {
  editando.value = true;

  mensaje.value = "";
  error.value = "";

  form.id = pedido.id;
  form.cliente_id = pedido.cliente_id;
  form.producto_id = pedido.producto_id;
  form.cantidad = pedido.cantidad;
  form.estado = pedido.estado;

  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
}

function cancelarEdicion() {
  editando.value = false;
  limpiarFormulario();
}

async function guardarPedido() {
  mensaje.value = "";
  error.value = "";

 if (!editando.value && !validarFormulario()) {
  return;
}

  guardando.value = true;

let datos;

if (editando.value) {
  datos = {
    estado: form.estado,
  };
} else {
  datos = {
    cliente_id: Number(form.cliente_id),
    producto_id: Number(form.producto_id),
    cantidad: Number(form.cantidad),
  };
}

  try {
    if (editando.value) {
      const response = await api.put(
        `/pedidos/${form.id}`,
        datos
      );

      const index = pedidos.value.findIndex(
        (pedido) => pedido.id === form.id
      );

      if (index !== -1) {
        pedidos.value[index] = response.data;
      }

      mensaje.value =
        "Pedido actualizado correctamente.";
    } else {
      const response = await api.post(
        "/pedidos",
        datos
      );

      pedidos.value.unshift(response.data);

      mensaje.value =
        "Pedido creado correctamente.";
    }

    editando.value = false;
    limpiarFormulario();

    await cargarDatos();
  } catch (err) {
    console.error(err);

    if (err.response?.data?.error) {
      error.value = err.response.data.error;
    } else {
      error.value =
        "No se pudo guardar el pedido.";
    }
  } finally {
    guardando.value = false;
  }
}

async function eliminarPedido(pedido) {
  const confirmar = window.confirm(
    `¿Desea eliminar el pedido #${pedido.id}?`
  );

  if (!confirmar) {
    return;
  }

  mensaje.value = "";
  error.value = "";

  try {
    await api.delete(
      `/pedidos/${pedido.id}`
    );

    pedidos.value = pedidos.value.filter(
      (item) => item.id !== pedido.id
    );

    mensaje.value =
      "Pedido eliminado correctamente.";
  } catch (err) {
    console.error(err);

    if (err.response?.data?.error) {
      error.value = err.response.data.error;
    } else {
      error.value =
        "No se pudo eliminar el pedido.";
    }
  }
}

onMounted(() => {
  cargarDatos();
});
</script>