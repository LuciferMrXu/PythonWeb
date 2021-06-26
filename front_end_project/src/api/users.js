import {
  $get, $put, $post, $delete, $patch
} from '@/utils/request'

export default {
  getUserInfo(id) {
    return $get('/user/' + id, {})
  },
  updateUser(id, data) {
    return $put('/user/' + id + '/', data)
  },
  getUsers(page_num, page_size, search) {
    return $get('/users/?ordering=-date_joined&page_num=' + page_num + '&page_size=' + page_size + '&search=' + search, {})
  },
  createUser(data) {
    return $post('/users/', data)
  },
  delUser(id) {
    return $delete('/users/' + id + '/', {})
  },
  editUser(id, data) {
    return $patch('/users/' + id + '/', data)
  }
}
