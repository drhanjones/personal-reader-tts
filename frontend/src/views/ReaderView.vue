<template>
    <div class="container my-4">
      <div class="d-flex justify-content-between mb-3">
        <button :disabled="page<=1" @click="go(page-1)">
          ← Previous
        </button>
        <span>Page {{ page }} / {{ totalPages }}</span>
        <button :disabled="page>=totalPages" @click="go(page+1)">
          Next →
        </button>
      </div>
      <!-- Render the HTML for this page -->
      <div v-html="htmlContent" class="border p-3"></div>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref, onMounted, watch } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  
  const route = useRoute()
  const router = useRouter()
  
  const fileId = ref<string>(route.query.fileId as string || '')
  const page   = ref<number>(route.query.page as unknown as number || 1)
  const totalPages  = ref<number>(1)
  const htmlContent = ref<string>('Loading…')
  
  async function fetchPageCount() {
    const res = await fetch(`/api/files/${fileId.value}/pages`)
    const all = await res.json() as string[]
    totalPages.value = all.length
  }
  
  async function fetchPage() {
    const res = await fetch(`/api/files/${fileId.value}/pages/${page.value}`)
    htmlContent.value = await res.text()
  }
  
  function go(newPage: number) {
    router.replace({ 
      name: 'Reader', 
      query: { fileId: fileId.value, page: String(newPage) } 
    })
  }
  
  onMounted(async () => {
    await fetchPageCount()
    await fetchPage()
  })
  
  // whenever `page` changes, re-fetch that HTML
  watch(page, fetchPage)
  </script>
  