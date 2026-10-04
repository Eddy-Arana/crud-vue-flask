<template>
  <div>
    <h1>Clientes</h1>

    <form @submit.prevent="guardarCliente">
      <h2>{{ editando ? "Editar cliente" : "Nuevo cliente" }}</h2>

      <FormField
        v-model="form.nombre"
        name="nombre"
        label="Nombre"
        placeholder="Ingrese el nombre"
        :error="errores.nombre"
      />

      <FormField
        v-model="form.correo"
        name="correo"
        label="Correo"
        type="email"
        placeholder="Ingrese el correo"
        :error="errores.correo"
      />

      <FormField
        v-model="form.telefono"
        name="telefono"
        label="Teléfono"
        placeholder="Ingrese el teléfono"
      />

      <button type="submit" :disabled="guardando">
        {{ guardando ? "Guardando..." : editando ? "Actualizar" : "Guardar" }}
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

    <LoadingMessage v-if="loading" />

    <DataTable
      v-if="!loading"
      :items="clientes"
      :columns="columns"
      @edit="editarCliente"
      @delete="eliminarCliente"
    />
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import DataTable from "../components/DataTable.vue";
import FormField from "../components/FormField.vue";
import LoadingMessage from "../components/LoadingMessage.vue";
import AlertMessage from "../components/AlertMessage.vue";
import api from "../services/api";

const clientes = ref([]);
const loading = ref(false);
const guardando = ref(false);
const editando = ref(false);

const error = ref("");
const mensaje = ref("");

const errores = reactive({
  nombre: "",
  correo: "",
});

const form = reactive({
  id: null,
  nombre: "",
  correo: "",
  telefono: "",
});

const columns = [
  {
    key: "id",
    label: "ID",
  },
  {
    key: "nombre",
    label: "Nombre",
  },
  {
    key: "correo",
    label: "Correo",
  },
  {
    key: "telefono",
    label: "Teléfono",
  },
];

function limpiarFormulario() {
  form.id = null;
  form.nombre = "";
  form.correo = "";
  form.telefono = "";

  errores.nombre = "";
  errores.correo = "";
}

function validarFormulario() {
  errores.nombre = "";
  errores.correo = "";

  let valido = true;

  if (!form.nombre.trim()) {
    errores.nombre = "El nombre es obligatorio.";
    valido = false;
  }

  if (!form.correo.trim()) {
    errores.correo = "El correo es obligatorio.";
    valido = false;
  }

  return valido;
}

async function cargarClientes() {
  loading.value = true;
  error.value = "";

  try {
    const response = await api.get("/clientes");

    clientes.value = response.data;
  } catch (err) {
    console.error(err);

    error.value = "No se pudieron cargar los clientes.";
  } finally {
    loading.value = false;
  }
}

function editarCliente(cliente) {
  editando.value = true;

  mensaje.value = "";
  error.value = "";

  form.id = cliente.id;
  form.nombre = cliente.nombre;
  form.correo = cliente.correo;
  form.telefono = cliente.telefono || "";

  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
}

function cancelarEdicion() {
  editando.value = false;
  limpiarFormulario();
}

async function guardarCliente() {
  mensaje.value = "";
  error.value = "";

  if (!validarFormulario()) {
    return;
  }

  guardando.value = true;

  try {
    if (editando.value) {
      const response = await api.put(
        `/clientes/${form.id}`,
        {
          nombre: form.nombre,
          correo: form.correo,
          telefono: form.telefono,
        }
      );

      const index = clientes.value.findIndex(
        (cliente) => cliente.id === form.id
      );

      if (index !== -1) {
        clientes.value[index] = response.data;
      }

      mensaje.value = "Cliente actualizado correctamente.";
    } else {
      const response = await api.post("/clientes", {
        nombre: form.nombre,
        correo: form.correo,
        telefono: form.telefono,
      });

      clientes.value.unshift(response.data);

      mensaje.value = "Cliente creado correctamente.";
    }

    editando.value = false;
    limpiarFormulario();
  } catch (err) {
    console.error(err);

    if (err.response?.data?.error) {
      error.value = err.response.data.error;
    } else {
      error.value = "No se pudo guardar el cliente.";
    }
  } finally {
    guardando.value = false;
  }
}

async function eliminarCliente(cliente) {
  const confirmar = window.confirm(
    `¿Desea eliminar al cliente "${cliente.nombre}"?`
  );

  if (!confirmar) {
    return;
  }

  mensaje.value = "";
  error.value = "";

  try {
    await api.delete(`/clientes/${cliente.id}`);

    clientes.value = clientes.value.filter(
      (item) => item.id !== cliente.id
    );

    mensaje.value = "Cliente eliminado correctamente.";
  } catch (err) {
    console.error(err);

    if (err.response?.data?.error) {
      error.value = err.response.data.error;
    } else {
      error.value = "No se pudo eliminar el cliente.";
    }
  }
}

onMounted(() => {
  cargarClientes();
});
</script>