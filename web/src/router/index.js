import Vue from 'vue'
import Router from 'vue-router'
import GetLog from '@/components/GetLog'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'GetLog',
      component: GetLog
    }
  ]
})
