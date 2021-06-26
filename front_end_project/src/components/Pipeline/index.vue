<template>
  <ul class="Steps">
    <li v-for="(item, key) in data" :key="key" :class="item.status">{{ item.name }}</li>
  </ul>
</template>

<script>
export default {
  name: 'Pipeline',
  inheritAttrs: false,
  props: {
    data: {
      type: Array,
      default: () => []
    }
  }
}
</script>
<style lang="scss">
.Steps {
   height: 10px;
   margin:auto;
 }
.Steps li {
  padding: 0px 0px 0px 20px;
  line-height: 30px;
  background: #D4D4D4;
  display: inline-block;
  color: #fff;
  position: relative;
  float: left;
  font-size: 12px;
  margin-right: 5px;
}
.Steps li:after {
  content: '';
  display: block;
  border-top: 15px solid #D4D4D4;
  border-bottom: 15px solid #D4D4D4;
  border-left: 15px solid #fff;
  position: absolute;
  right: -15px;
  top: 0;
}
.Steps li:after {
  content: '';
  display: block;
  border-top: 15px solid transparent;
  border-bottom: 15px solid transparent;
  border-left: 15px solid #D4D4D4;
  position: absolute;
  right: -15px;
  top: 0;
  z-index: 10;
}
.Steps li:before {
  content: '';
  display: block;
  border-top: 15px solid #D4D4D4;
  border-bottom: 15px solid #D4D4D4;
  border-left: 15px solid #fff;
  position: absolute;
  left: 0px;
  top: 0;
}
/* .Steps li:first-child {
  border-radius: 4px 0 0 4px;
 }
.Steps li:first-child:before {
  display: none;
} */
.Steps li.active {
  background-color: #019BF2;
}
.Steps li.active:after {
  border-left-color: #019BF2;
}
.Steps li.active:before {
  border-top-color: #019BF2;
  border-bottom-color: #019BF2;
}
.Steps li.sucess {
  background-color: #67C23A;
}
.Steps li.sucess:after {
  border-left-color: #67C23A;
}
.Steps li.sucess:before {
  border-top-color: #67C23A;
  border-bottom-color: #67C23A;
}
.Steps li.fail {
  background-color: #F56C6C;
}
.Steps li.fail:after {
  border-left-color: #F56C6C;
}
.Steps li.fail:before {
  border-top-color: #F56C6C;
  border-bottom-color: #F56C6C;
}
</style>
