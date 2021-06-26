<template>
  <div class="dashboard-container">
    <!-- <div class="dashboard-text">name: {{ name }}</div>
    <div class="dashboard-text">roles: <span v-for="role in roles" :key="role">{{ role }}</span></div> -->
    <iframe src="http://172.31.128.180:3000/d/w8MGqOTMz/docker-monitoring?orgId=1&refresh=10s&kiosk=tv" width="100%" height="100%" frfameborder="0" />
  </div>
</template>

<script>
// import { mapGetters } from 'vuex'

export default {
  name: 'Dashboard'
  // computed: {
  //   ...mapGetters([
  //     'name',
  //     'roles'
  //   ])
  // }
}
</script>

<style lang="scss" scoped>
.dashboard {
  &-container {
    /*margin: 30px;*/
    height: 95vh;
  }
  &-text {
    font-size: 30px;
    line-height: 46px;
  }
}
</style>
