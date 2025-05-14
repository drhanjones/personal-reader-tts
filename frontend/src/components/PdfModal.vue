<!-- src/components/PdfModal.vue -->
<template>
    <div v-if="visible">
      <!-- backdrop -->
      <div class="modal-backdrop fade show"></div>
  
      <!-- modal dialog -->
      <div
        class="modal fade show d-block"
        tabindex="-1"
        role="dialog"
        aria-modal="true"
      >
        <div class="modal-dialog modal-xl modal-dialog-centered" role="document">
          <div class="modal-content">
  
            <!-- header with close button -->
            <div class="modal-header">
              <h5 class="modal-title">PDF Preview</h5>
              <button
                type="button"
                class="btn-close"
                aria-label="Close"
                @click="$emit('close')"
              ></button>
            </div>
  
            <!-- body: slot for our embed -->
            <div class="modal-body p-0">
              <slot />
            </div>
  
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  
  export default defineComponent({
    name: 'PdfModal',
    props: {
      visible: { type: Boolean, required: true }
    }
  });
  </script>
  