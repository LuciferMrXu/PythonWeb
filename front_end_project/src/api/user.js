// import request from '@/utils/request'
import {
  $get,
  $post
} from '@/utils/request'

export function login(data) {
  return $post('/user/login', data)
}
export function getInfo(token) {
  return $get('/user/info?token=' + token)
}
export function logout() {
  return $get('/user/logout')
}
