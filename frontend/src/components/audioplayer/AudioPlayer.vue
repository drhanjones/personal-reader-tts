<!-- ModernAudioPlayer.vue -->
<template>
  <div class="modern-player" :class="{ 'playing': isPlaying }">
    <!-- Cover Art Display -->
    <div class="cover-art-container">
      <img v-if="currentTrack && currentTrack.cover" :src="currentTrack.cover" alt="Album Cover" class="cover-art" />
      <div v-else class="cover-art-placeholder">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="placeholder-icon">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 14.5c-2.49 0-4.5-2.01-4.5-4.5S9.51 7.5 12 7.5s4.5 2.01 4.5 4.5-2.01 4.5-4.5 4.5zm0-5.5c-.55 0-1 .45-1 1s.45 1 1 1 1-.45 1-1-.45-1-1-1z"/>
        </svg>
      </div>
    </div>
    
    <!-- Track Info -->
    <div class="track-info">
      <div class="track-title">{{ currentTrack?.title || 'No track selected' }}</div>
      <div class="track-artist">{{ currentTrack?.artist || 'Unknown artist' }}</div>
    </div>
    
    <!-- Progress Bar -->
    <div class="progress-container">
      <div class="time current">{{ formatTime(currentTime) }}</div>
      <div class="progress-bar" @click="seek">
        <div class="progress-background"></div>
        <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
        <div class="progress-handle" :style="{ left: progressPercentage + '%' }"></div>
      </div>
      <div class="time duration">{{ formatTime(duration) }}</div>
    </div>
    
    <!-- Controls -->
    <div class="controls">
      <button @click="previousTrack" class="control-button">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="control-icon">
          <path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"/>
        </svg>
      </button>
      
      <button @click="togglePlay" class="control-button play-button">
        <svg v-if="isPlaying" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="control-icon">
          <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="control-icon">
          <path d="M8 5v14l11-7z"/>
        </svg>
      </button>
      
      <button @click="nextTrack" class="control-button">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="control-icon">
          <path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/>
        </svg>
      </button>
    </div>
    
    <!-- Volume Control -->
    <div class="volume-control">
      <button @click="toggleMute" class="volume-button">
        <svg v-if="volume > 0" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="volume-icon">
          <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
        </svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="volume-icon">
          <path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/>
        </svg>
      </button>
      
      <div class="volume-slider-container">
        <input 
          type="range" 
          min="0" 
          max="1" 
          step="0.01" 
          v-model="volume" 
          @input="updateVolume"
          class="volume-slider"
        />
      </div>
    </div>
    
    <!-- Audio Element -->
    <audio 
      ref="audioElement"
      @timeupdate="onTimeUpdate"
      @loadedmetadata="onLoadedMetadata"
      @ended="onEnded"
    ></audio>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, onBeforeUnmount } from 'vue';

// Define interfaces for our data types
interface AudioTrack {
  id: number | string;
  title: string;
  artist: string;
  src: string;
  cover?: string;
}

export default defineComponent({
  name: 'ModernAudioPlayer',
  props: {
    tracks: {
      type: Array as () => AudioTrack[],
      default: () => []
    }
  },
  setup(props) {
    // Refs (reactive data)
    const audioElement = ref<HTMLAudioElement | null>(null);
    const currentTrackIndex = ref(0);
    const isPlaying = ref(false);
    const currentTime = ref(0);
    const duration = ref(0);
    const volume = ref(0.7);
    const previousVolume = ref(0.7); // For mute/unmute
    const progressPercentage = ref(0);
    const isDragging = ref(false);

    // Computed properties
    const currentTrack = computed<AudioTrack | null>(() => {
      return props.tracks.length > 0 ? props.tracks[currentTrackIndex.value] : null;
    });

    // Methods
    function loadTrack(track: AudioTrack): void {
      if (!track || !track.src || !audioElement.value) return;
      
      audioElement.value.src = track.src;
      audioElement.value.load();
      currentTime.value = 0;
      progressPercentage.value = 0;
      
      // Auto-play if it was playing before
      if (isPlaying.value && audioElement.value) {
        audioElement.value.play().catch(error => {
          console.error('Error playing audio:', error);
        });
      }
    }

    function togglePlay(): void {
      if (!currentTrack.value || !audioElement.value) return;
      
      if (isPlaying.value) {
        audioElement.value.pause();
      } else {
        audioElement.value.play().catch(error => {
          console.error('Error playing audio:', error);
        });
      }
      isPlaying.value = !isPlaying.value;
    }

    function nextTrack(): void {
      if (props.tracks.length <= 1) return;
      
      currentTrackIndex.value = (currentTrackIndex.value + 1) % props.tracks.length;
      loadTrack(props.tracks[currentTrackIndex.value]);
    }

    function previousTrack(): void {
      if (props.tracks.length <= 1) return;
      
      // Go to previous track or restart current track if more than 3 seconds in
      if (currentTime.value > 3 && audioElement.value) {
        audioElement.value.currentTime = 0;
      } else {
        currentTrackIndex.value = (currentTrackIndex.value - 1 + props.tracks.length) % props.tracks.length;
        loadTrack(props.tracks[currentTrackIndex.value]);
      }
    }

    function seek(event: MouseEvent): void {
      if (!audioElement.value || !duration.value) return;
      
      const progressBar = event.currentTarget as HTMLElement;
      const rect = progressBar.getBoundingClientRect();
      const offsetX = event.clientX - rect.left;
      const barWidth = progressBar.clientWidth;
      const seekPercentage = offsetX / barWidth;
      
      audioElement.value.currentTime = seekPercentage * duration.value;
    }

    function onTimeUpdate(): void {
      if (!audioElement.value) return;
      currentTime.value = audioElement.value.currentTime;
      progressPercentage.value = (currentTime.value / duration.value) * 100 || 0;
    }

    function onLoadedMetadata(): void {
      if (!audioElement.value) return;
      duration.value = audioElement.value.duration;
    }

    function onEnded(): void {
      nextTrack();
    }

    function updateVolume(): void {
      if (audioElement.value) {
        audioElement.value.volume = volume.value;
      }
    }

    function toggleMute(): void {
      if (volume.value > 0) {
        previousVolume.value = volume.value;
        volume.value = 0;
      } else {
        volume.value = previousVolume.value;
      }
      updateVolume();
    }

    function formatTime(seconds: number): string {
      if (!seconds || isNaN(seconds)) return '0:00';
      
      const minutes = Math.floor(seconds / 60);
      const secondsRemainder = Math.floor(seconds % 60);
      return `${minutes}:${secondsRemainder < 10 ? '0' : ''}${secondsRemainder}`;
    }

    // Lifecycle hooks
    onMounted(() => {
      audioElement.value = document.querySelector('audio');
      updateVolume();
      
      // Load the first track if available
      if (currentTrack.value) {
        loadTrack(currentTrack.value);
      }
    });

    onBeforeUnmount(() => {
      // Stop audio playback
      if (audioElement.value) {
        audioElement.value.pause();
        audioElement.value.src = '';
      }
    });

    // Return everything that's used in the template
    return {
      audioElement,
      currentTrackIndex,
      isPlaying,
      currentTime,
      duration,
      volume,
      previousVolume,
      progressPercentage,
      isDragging,
      currentTrack,
      loadTrack,
      togglePlay,
      nextTrack,
      previousTrack,
      seek,
      onTimeUpdate,
      onLoadedMetadata,
      onEnded,
      updateVolume,
      toggleMute,
      formatTime
    };
  }
});
</script>

<style scoped>
.modern-player {
  background-color: #17171D;
  color: #FFFFFF;
  border-radius: 16px;
  padding: 24px;
  width: 100%;
  max-width: 360px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.cover-art-container {
  width: 100%;
  height: 200px;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 20px;
  background-color: #222228;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cover-art {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-art-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  background-color: #2D2D36;
}

.placeholder-icon {
  width: 64px;
  height: 64px;
  fill: #8E8E96;
}

.track-info {
  text-align: center;
  margin-bottom: 16px;
}

.track-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.track-artist {
  font-size: 14px;
  color: #8E8E96;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.progress-container {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.time {
  font-size: 12px;
  color: #8E8E96;
  min-width: 40px;
}

.time.current {
  text-align: left;
}

.time.duration {
  text-align: right;
}

.progress-bar {
  flex-grow: 1;
  height: 4px;
  position: relative;
  cursor: pointer;
  padding: 8px 0;
}

.progress-background {
  height: 4px;
  width: 100%;
  background-color: #2D2D36;
  border-radius: 2px;
  position: absolute;
}

.progress-fill {
  height: 4px;
  background: linear-gradient(90deg, #4A90E2, #60BFFF);
  border-radius: 2px;
  position: absolute;
  transition: width 0.1s linear;
}

.progress-handle {
  width: 12px;
  height: 12px;
  background-color: #FFFFFF;
  border-radius: 50%;
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: transform 0.1s ease-in-out;
}

.progress-handle:hover {
  transform: translate(-50%, -50%) scale(1.2);
}

.controls {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.control-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #FFFFFF;
}

.play-button {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #4A90E2, #60BFFF);
  border-radius: 50%;
  transition: transform 0.2s ease-in-out;
}

.play-button:hover {
  transform: scale(1.05);
}

.play-button:active {
  transform: scale(0.95);
}

.control-icon {
  width: 24px;
  height: 24px;
  fill: currentColor;
}

.play-button .control-icon {
  width: 28px;
  height: 28px;
}

.volume-control {
  display: flex;
  align-items: center;
  gap: 12px;
}

.volume-button {
  background: none;
  border: none;
  cursor: pointer;
  color: #8E8E96;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.volume-icon {
  width: 20px;
  height: 20px;
  fill: currentColor;
}

.volume-slider-container {
  flex-grow: 1;
}

.volume-slider {
  width: 100%;
  height: 4px;
  -webkit-appearance: none;
  appearance: none;
  background: #2D2D36;
  outline: none;
  border-radius: 2px;
  cursor: pointer;
}

.volume-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #FFFFFF;
  cursor: pointer;
  transition: transform 0.1s ease-in-out;
}

.volume-slider::-webkit-slider-thumb:hover {
  transform: scale(1.2);
}

.volume-slider::-moz-range-thumb {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #FFFFFF;
  cursor: pointer;
  border: none;
  transition: transform 0.1s ease-in-out;
}

.volume-slider::-moz-range-thumb:hover {
  transform: scale(1.2);
}

.volume-slider::-webkit-slider-runnable-track {
  height: 4px;
  border-radius: 2px;
  background: linear-gradient(
    to right,
    #4A90E2 0%,
    #4A90E2 calc(var(--volume) * 100%),
    #2D2D36 calc(var(--volume) * 100%),
    #2D2D36 100%
  );
}

/* Animation for play state */
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.modern-player.playing .cover-art {
  animation: pulse 2s infinite ease-in-out;
}
</style>