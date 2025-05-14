<template>
    <div class="p-3 border rounded shadow-sm">
      <h5>Uploaded Files</h5>
      <ul class="list-unstyled">
        <!-- Loop over our files and show each as a button -->
        <li
          v-for="file in files"
          :key="file.id"
          class="mb-1"
        >
          <button
            class="btn btn-outline-primary btn-sm w-100 text-start"
            @click="selectFile(file)"
          >
            {{ file.name }}
          <span
            v-if="file.processed"
            class="badge bg-success ms-1"
          >✓</span>
          <span
            v-else
            class="badge bg-warning ms-1"
          >Unprocessed</span>
          </button>
        </li>
        <!-- If no files yet -->
        <li v-if="files.length === 0" class="text-muted">
          No files uploaded yet.
        </li>
      </ul>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue';
  
  export default defineComponent({
    name: 'ListFiles',
    emits: ['fileSelected'],
    setup(_, { emit }) {
      // 1) “files” holds our fetched list
      const files = ref<{ id: string; name: string }[]>([]);
  
      // 2) Fetch from GET /api/files on mount
      async function fetchFiles() {
        try {
          const res = await fetch('/api/files');
          if (!res.ok) throw new Error(res.statusText);
          files.value = await res.json();  
          // Expect JSON like [{ id: "abc123", name: "doc1.pdf" }, ...]
        } catch (err: any) {
          console.error('Could not load files:', err.message);
        }
      }
  
      // 3) When a button is clicked, send the file up
      function selectFile(file: { id: string; name: string }) {
        emit('fileSelected', file);
      }
  
      onMounted(fetchFiles);
  
      return { files, selectFile, fetchFiles };
    }
  });
  </script>
  
  <style scoped>
  /* just a bit of spacing */
  button:focus {
    outline: none;
    box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
  }
  </style>
  