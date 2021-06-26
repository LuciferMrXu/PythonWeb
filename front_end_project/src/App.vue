<template>
  <div id="app">
    <el-scrollbar
      style="height: 100%"
      wrap-class="scrollbar-wrapper"
      view-style="font-weight: bold;height:100%;"
    >
      <router-view />
    </el-scrollbar>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>
<style lang="scss">
.scrollbar-wrapper {
  overflow-x: hidden !important;
}
</style>
