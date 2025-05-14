<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <!-- Brand -->
        <router-link class="navbar-brand" to="/">PDF Reader</router-link>
  
        <!-- Toggler for mobile -->
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#mainNavbar"
          aria-controls="mainNavbar"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
  
        <!-- Nav links -->
        <div class="collapse navbar-collapse" id="mainNavbar">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <!-- Home/dashboard -->
            <li class="nav-item">
              <router-link class="nav-link" :to="{ path: '/' }">Dashboard</router-link>
            </li>
            <!-- Reader (no specific file) -->
            <li class="nav-item">
              <router-link class="nav-link" :to="{ path: '/reader', query: { fileId: '', page: '1' } }">
                Reader
              </router-link>
            </li>
            <!-- You can add more links here as you build features -->
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script lang="ts" setup>
  // No props for now – static links.
  // If you later want to highlight "active", you can pull in useRoute() 
  // and compare route.path/query.
  </script>
  
  <style scoped>
  /* You can override/add classes here later for custom colors, spacing, etc. */
  </style>
  