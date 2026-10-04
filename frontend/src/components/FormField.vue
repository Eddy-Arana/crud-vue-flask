<template>
  <div class="mb-3">
    <label
      :for="name"
      class="form-label"
    >
      {{ label }}
    </label>

    <input
      :id="name"
      :name="name"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      class="form-control"
      :class="{ 'is-invalid': error }"
      @input="$emit('update:modelValue', $event.target.value)"
    />

    <div
      v-if="error"
      class="invalid-feedback"
    >
      {{ error }}
    </div>
  </div>
</template>

<script setup>
defineProps({
  name: {
    type: String,
    required: true,
  },

  label: {
    type: String,
    required: true,
  },

  type: {
    type: String,
    default: "text",
  },

  modelValue: {
    type: [String, Number],
    default: "",
  },

  placeholder: {
    type: String,
    default: "",
  },

  error: {
    type: String,
    default: "",
  },
});

defineEmits(["update:modelValue"]);
</script>