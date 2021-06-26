import {
  $get, $patch
} from '@/utils/request'

export default {
  getUserInfo(id) {
    return $get('/user/' + id, {})
  },
  updateUser(id, data) {
    return $patch('/user/' + id + '/', data)
  }
}
