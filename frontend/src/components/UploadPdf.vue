<!-- frontend/src/components/UploadPdf.vue -->
<template>
    <div class="position-relative">
      <div

      >
        <div class="card shadow-sm">
          <div class="card-body">
            <h3 class="card-title mb-3">PDF Uploader</h3>
  
            <input
              class="form-control mb-3"
              type="file"
              accept="application/pdf"
              @change="onFileChange"
            />
  
            <button
              v-if="previewUrl"
              class="btn btn-primary"
              @click="openPreview"
            >
              Preview PDF
            </button>

            <button
            v-if="selectedFile"             
            class="btn btn-success"
            @click="parsePdf"              
            >
            Upload PDF
            </button>
            
          </div>
        </div>
      </div>
  
      <PdfModal :visible="isModalOpen" @close="closePreview">
        <embed
          :src="previewUrl"
          type="application/pdf"
          width="100%"
          height="600px"
        />  
      </PdfModal>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref } from 'vue';
  import PdfModal from './PdfModal.vue';
  
  export default defineComponent({
    name: 'UploadPdf',
    components: { PdfModal },
    setup() {
      const selectedFile = ref<File|null>(null);
      const previewUrl   = ref<string|null>(null);
      const isModalOpen  = ref(false);

      function onFileChange(e: Event) {
        const input = e.target as HTMLInputElement;
        if (!input.files?.length) return;
        selectedFile.value = input.files[0];                 // <-- store the File
        previewUrl.value = URL.createObjectURL(selectedFile.value);
      }

      async function parsePdf() {
        if (!selectedFile.value) {
            console.error('No file selected');
            return;
        }
    

        // 1) Create a “package” (FormData) and put the file in it
        const formData = new FormData();
        formData.append('file', selectedFile.value);         // 'file' is the field name
        console.log('FormData:', formData.get('file'));
        // 2) Send it to the server with fetch()
        try {
            const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData,
            });

            if (!response.ok) {
            throw new Error(`Upload failed: ${response.statusText}`);
            }
            const result = await response.json();
            console.log('Server returned:', result);
            // TODO: store result and render it in the UI

            
        } catch (err: any) {
            console.error('Upload error:', err.message);
        }
        }


      function openPreview()  { if (previewUrl.value) isModalOpen.value = true; }
      function closePreview() { isModalOpen.value = false; }
  
      return { previewUrl, isModalOpen, selectedFile, onFileChange, openPreview, closePreview, parsePdf };
    }
  });
  </script>
  
<style scoped>
/* 1. Full-screen flexbox centering */
.upload-container {
  display: flex;              
  align-items: center;        
  justify-content: center;    
  min-height: 100vh;          
  background: #f0f2f5;        /* light grey background */
}

/* 2. The “card” look */
.upload-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  text-align: center;
  width: 90%;
  max-width: 400px;
}

/* 3. Page title inside the card */
.title {
  margin-bottom: 1rem;
  font-size: 1.5rem;
  color: #333;
}

/* 4. Styled button */
.btn {
  margin-top: 1rem;
  background-color: #4f46e5;  /* a pleasant purple-blue */
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}
.btn:hover {
  background-color: #4338ca;  /* slightly darker on hover */
}
</style>
