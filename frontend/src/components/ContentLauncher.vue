<template>
    <div class="p-3 border rounded text-center">
      <template v-if="file">
        <!-- NOT yet processed -->
        <div v-if="!file.processed">
          <p>This PDF for {{file.name }} hasn’t been converted to HTML yet.</p>
          <button class="btn btn-warning" @click="process">
            Process for Reader Mode
          </button>
        </div>
  
        <!-- Already processed -->
        <div v-else>
          <p>Ready to read in the Reader:</p>
          <button class="btn btn-primary" @click="openReader">
            Open in Reader Mode
          </button>
        </div>
      </template>
      <p v-else class="text-muted">Select a file above to proceed.</p>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { defineProps, defineEmits } from 'vue'
  import { useRouter } from 'vue-router'
  
  interface FileInfo { id: string; processed: boolean, name: string }
  
  const props = defineProps<{ file: FileInfo | null }>()
  
  // Here we define each event name as a key, with a payload signature as its type.
  const emit = defineEmits<{
    processed: (id: string) => void
  }>()
  
  const router = useRouter()
  
  async function process() {
    if (!props.file) return
    const res = await fetch(`/api/files/${props.file.name}/extract`, { method: 'POST' })
    if (!res.ok) throw new Error(await res.text())
    emit('processed', props.file.id)
  }
  
  function openReader() {
    if (!props.file) return
    const href = router.resolve({
      name: 'Reader',
      query: { fileId: props.file.name, page: '1' }
    }).href
    window.open(href, '_blank')
  }
  </script>
  
  