import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/profile',
    component: Layout,
    redirect: '/profile/index',
    hidden: true,
    children: [
      {
        path: 'index',
        component: () => import('@/views/profile/index'),
        name: 'Profile',
        meta: { title: '个人中心' }
      }
    ]
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '首页', icon: 'dashboard' }
    }]
  },

  {
    path: '/template',
    component: Layout,
    redirect: '/template/templateEdit',
    hidden: true,
    children: [
      {
        path: 'templateEdit',
        component: () => import('@/views/xtest/templateEdit'),
        name: 'TemplateEdit',
        meta: { title: '模板编辑' }
      }
    ]
  },

  {
    path: '/statistics',
    component: Layout,
    redirect: '/statistics/month',
    name: 'Statistics',
    meta: { title: '数据统计', icon: 'el-icon-s-help' },
    children: [
      {
        path: 'month',
        name: 'Month',
        component: () => import('@/views/form/index'),
        meta: { title: '月度概览', icon: 'table' }
      },
      {
        path: 'detail',
        name: 'Detail',
        component: () => import('@/views/tree/index'),
        meta: { title: '详细指标', icon: 'tree' }
      }
    ]
  }
]

/**
 * asyncRoutes
 * the routes that need to be dynamically loaded based on user roles
 */
export const asyncRoutes = [
  {
    path: '/manage',
    component: Layout,
    redirect: '/manage/rainbow',
    name: 'Manage',
    meta: {
      title: '平台管理',
      icon: 'nested',
      roles: ['admin', 'editor']
    },
    children: [
      {
        path: 'rainbow',
        name: 'Rainbow',
        component: () => import('@/views/rainbow/index'),
        meta: { title: '彩虹平台' }
      },
      {
        path: 'xtest',
        component: () => import('@/views/xtest/index'),
        name: 'Xtest',
        meta: { title: '测试平台' }
      }
    ]
  },
  {
    path: '/users',
    component: Layout,
    children: [
      {
        path: 'index',
        name: 'Users',
        component: () => import('@/views/users/index'),
        meta: {
          title: '用户管理',
          icon: 'form',
          roles: ['admin']
        }
      }
    ]
  },
  {
    path: 'external-link',
    component: Layout,
    children: [
      {
        path: 'http://rainbow.iflytek.cn/',
        meta: {
          roles: ['admin', 'editor'],
          title: 'External Link',
          icon: 'link'
        }
      }
    ]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
