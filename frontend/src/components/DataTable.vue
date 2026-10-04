<template>
  <div class="table-responsive">
    <table class="table table-striped table-hover align-middle">
      <thead class="table-dark">
        <tr>
          <th
            v-for="column in columns"
            :key="column.key"
          >
            {{ column.label }}
          </th>

          <th>Acciones</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="item in items"
          :key="item.id"
        >
          <td
            v-for="column in columns"
            :key="column.key"
          >
            {{ item[column.key] }}
          </td>

          <td>
            <button
              class="btn btn-sm btn-warning me-2"
              @click="$emit('edit', item)"
            >
              Editar
            </button>

            <button
              class="btn btn-sm btn-danger"
              @click="$emit('delete', item)"
            >
              Eliminar
            </button>
          </td>
        </tr>

        <tr v-if="items.length === 0">
          <td
            :colspan="columns.length + 1"
            class="text-center"
          >
            No hay registros.
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    default: () => [],
  },

  columns: {
    type: Array,
    default: () => [],
  },
});

defineEmits(["edit", "delete"]);
</script>