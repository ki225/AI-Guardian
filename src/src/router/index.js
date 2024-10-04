import { createRouter, createWebHashHistory } from 'vue-router'
import MainAppView from '../views/MainAppView.vue'
import LoginView from "../views/LoginView.vue"
import BuildView from "../views/BuildView.vue"
import AiChatView from '../views/AiChatView.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/waf-manager/chat',
    name: 'Waf Manager ai',
    component: AiChatView,
    meta: { requiresAuth: true }
  },
  {
    path: '/waf-manager',
    name: 'Waf Manager',
    component: MainAppView,
    meta: { requiresAuth: true }
  },
  {
    path: '/build-progress',
    name: 'Resource Build Progress',
    component: BuildView,
    meta: { requiresAuth: true, requiresProgrammaticNavigation: true }
  }
]

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes
})

let isProgrammaticNavigation = false

const originalPush = router.push
router.push = function(...args) {
  isProgrammaticNavigation = true
  return originalPush.apply(this, args)
}

// Improved global navigation guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true'

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } 
    else if (to.meta.requiresProgrammaticNavigation && !isProgrammaticNavigation) {
      // Redirect to waf-manager if trying to access build-progress directly
      if(from.name == "Waf Manager ai"){
        next('/waf-manager/chat')
      }
      else{
        next('/waf-manager')
      }
    }
    else {
      next()
    }
  } 
  else if (to.path === '/login' && isAuthenticated) {
    if(from.name == "Waf Manager ai"){
      next('/waf-manager/chat')
    }
    else{
      next('/waf-manager')
    }
  } 
  else {
    next()
  }

  // Reset the flag after navigation
  isProgrammaticNavigation = false
})

export default router