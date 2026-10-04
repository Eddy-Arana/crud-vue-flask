<template>
  <div>
    <h1>Productos</h1>

    <form @submit.prevent="guardarProducto">
      <h2>{{ editando ? "Editar producto" : "Nuevo producto" }}</h2>

      <FormField
        v-model="form.nombre"
        name="nombre"
        label="Nombre"
        placeholder="Ingrese el nombre"
        :error="errores.nombre"
      />

      <FormField
        v-model="form.descripcion"
        name="descripcion"
        label="Descripción"
        placeholder="Ingrese la descripción"
      />

      <FormField
        v-model="form.precio"
        name="precio"
        label="Precio"
        type="number"
        placeholder="Ingrese el precio"
        :error="errores.precio"
      />

      <FormField
        v-model="form.stock"
        name="stock"
        label="Stock"
        type="number"
        placeholder="Ingrese el stock"
        :error="errores.stock"
      />

      <label>
        <input
          v-model="form.activo"
          type="checkbox"
        />
        Producto activo
      </label>

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
      Cargando productos...
    </p>

    <DataTable
      v-if="!loading"
      :items="productos"
      :columns="columns"
      @edit="editarProducto"
      @delete="eliminarProducto"
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

const productos = ref([]);
const loading = ref(false);
const guardando = ref(false);
const editando = ref(false);

const error = ref("");
const mensaje = ref("");

const errores = reactive({
  nombre: "",
  precio: "",
  stock: "",
});

const form = reactive({
  id: null,
  nombre: "",
  descripcion: "",
  precio: "",
  stock: "",
  activo: true,
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
    key: "descripcion",
    label: "Descripción",
  },
  {
    key: "precio",
    label: "Precio",
  },
  {
    key: "stock",
    label: "Stock",
  },
  {
    key: "activo",
    label: "Activo",
  },
];

function limpiarFormulario() {
  form.id = null;
  form.nombre = "";
  form.descripcion = "";
  form.precio = "";
  form.stock = "";
  form.activo = true;

  errores.nombre = "";
  errores.precio = "";
  errores.stock = "";
}

function validarFormulario() {
  errores.nombre = "";
  errores.precio = "";
  errores.stock = "";

  let valido = true;

  if (!form.nombre.trim()) {
    errores.nombre = "El nombre es obligatorio.";
    valido = false;
  }

  if (form.precio === "" || Number(form.precio) < 0) {
    errores.precio = "El precio debe ser mayor o igual a cero.";
    valido = false;
  }

  if (
    form.stock === "" ||
    !Number.isInteger(Number(form.stock)) ||
    Number(form.stock) < 0
  ) {
    errores.stock = "El stock debe ser un entero mayor o igual a cero.";
    valido = false;
  }

  return valido;
}

async function cargarProductos() {
  loading.value = true;
  error.value = "";

  try {
    const response = await api.get("/productos");

    productos.value = response.data;
  } catch (err) {
    console.error(err);

    error.value = "No se pudieron cargar los productos.";
  } finally {
    loading.value = false;
  }
}

function editarProducto(producto) {
  editando.value = true;

  mensaje.value = "";
  error.value = "";

  form.id = producto.id;
  form.nombre = producto.nombre;
  form.descripcion = producto.descripcion || "";
  form.precio = producto.precio;
  form.stock = producto.stock;
  form.activo = producto.activo;

  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
}

function cancelarEdicion() {
  editando.value = false;
  limpiarFormulario();
}

async function guardarProducto() {
  mensaje.value = "";
  error.value = "";

  if (!validarFormulario()) {
    return;
  }

  guardando.value = true;

  const datos = {
    nombre: form.nombre,
    descripcion: form.descripcion,
    precio: Number(form.precio),
    stock: Number(form.stock),
    activo: form.activo,
  };

  try {
    if (editando.value) {
      const response = await api.put(
        `/productos/${form.id}`,
        datos
      );

      const index = productos.value.findIndex(
        (producto) => producto.id === form.id
      );

      if (index !== -1) {
        productos.value[index] = response.data;
      }

      mensaje.value =
        "Producto actualizado correctamente.";
    } else {
      const response = await api.post(
        "/productos",
        datos
      );

      productos.value.unshift(response.data);

      mensaje.value =
        "Producto creado correctamente.";
    }

    editando.value = false;
    limpiarFormulario();
  } catch (err) {
    console.error(err);

    if (err.response?.data?.error) {
      error.value = err.response.data.error;
    } else {
      error.value =
        "No se pudo guardar el producto.";
    }
  } finally {
    guardando.value = false;
  }
}

async function eliminarProducto(producto) {
  const confirmar = window.confirm(
    `¿Desea eliminar el producto "${producto.nombre}"?`
  );

  if (!confirmar) {
    return;
  }

  mensaje.value = "";
  error.value = "";

  try {
    await api.delete(
      `/productos/${producto.id}`
    );

    productos.value = productos.value.filter(
      (item) => item.id !== producto.id
    );

    mensaje.value =
      "Producto eliminado correctamente.";
  } catch (err) {
    console.error(err);

    if (err.response?.data?.error) {
      error.value = err.response.data.error;
    } else {
      error.value =
        "No se pudo eliminar el producto.";
    }
  }
}

onMounted(() => {
  cargarProductos();
});
</script>