<template>
    <!-- <div id="app">
      <div style="position: absolute; top: 0; left: 0;">
        <UploadPdf />
      </div>
    </div> -->
  
    <div class="app-container">
      <div id="file-upload" class="component file-upload">
          <UploadPdf @uploaded="refreshList"/>
      </div>
      
      <div id="content-list" class="component content-list">
        <h2>Content List Component</h2>
        <ListFiles @fileSelected="handleFileSelected" ref="listRef" />
      </div>

      <div id="audio-player" class="component audio-player">
        <AudioPlayerLandscape
          :tracks="tracks"
        />
      </div>
      
      <div id="content-display" class="component content-display">
        <ContentLauncher
          v-if="selectedFile"
          :file="selectedFile"
          @processed="refreshList"
        />
      </div>
    </div>
  
</template>
  
  
<style>
body {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
}

.app-container {
    display: grid;
    grid-template-columns: auto 1fr;
    grid-template-rows: auto 1fr 1fr 1fr;
    gap: 1rem;
    height: 100vh;
    width: 100vw;
    padding: 1rem;
    box-sizing: border-box;
}

.component {
    background-color: #f5f5f5;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.file-upload {
    background-color: #e3f2fd;
    grid-column: 1;
    grid-row: 1;
}

.content-list {
    background-color: #e8f5e9;
    grid-column: 1;
    grid-row: 2/5;
}

.audio-player {
    background-color: #fff3e0;
    grid-column: 2;
    grid-row: 1 / 3;
}

.content-display {
    background-color: #fce4ec;
    grid-column: 2;
    grid-row: 3 / 5;
}
</style>

<script lang="ts">

import { defineComponent, ref, computed} from 'vue';
import UploadPdf from './UploadPdf.vue';
import ListFiles from './ListFiles.vue';
import ContentLauncher from './ContentLauncher.vue';
import AudioPlayerLandscape from './audioplayer/AudioPlayerLandscape.vue';

export default defineComponent({
  name: 'Dashboard',
  components: {
    UploadPdf,
    ListFiles,
    ContentLauncher,
    AudioPlayerLandscape
  },
    setup() {
  
    const selectedFile = ref<{ id: string; name: string; processed: boolean } > ({
        id: '',
        name: '',
        processed: false
    })
    const listRef = ref<InstanceType<typeof ListFiles> | null>(null);

    function handleFileSelected(file: { id: string; name: string ; processed: boolean }) {
        console.log('File selected:', file);
        selectedFile.value = file;
    }

    function onProcessed(fileId: string) {
        if (selectedFile.value?.id === fileId) {
        selectedFile.value.processed = true;
        }
        listRef.value?.fetchFiles?.();
    }

    function refreshList() {
    listRef.value?.fetchFiles?.();
    }

    const tracks = computed(() => {
      if (!selectedFile.value.id) return []
      console.log('Selected file for audio:', selectedFile.value);
      return [
        {
          id: selectedFile.value.id,
          title: selectedFile.value.name,
          artist: 'PDF Reader TTS',
          src: `/api/files/${selectedFile.value.name}/audio`,
          cover: ''  // or supply a URL if you have cover art
        }
      ]
    })

    
    return {
    selectedFile,
    handleFileSelected,
    refreshList,
    listRef,
    onProcessed,
    tracks
    };
 
    }
});



</script>