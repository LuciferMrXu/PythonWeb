import {
  $get, $put, $post, $delete, $rainbow, $patch
} from '@/utils/request'
export default {
  delNode(id) {
    return $delete('/nodeAPI/' + id + '/', {})
  },
  getNode(page_num, page_size, search) {
    return $get('/nodeAPI/?ordering=-add_time&page_num=' + page_num + '&page_size=' + page_size + '&search=' + search, {})
  },
  readNode(id) {
    return $get('/nodeAPI/' + id + '/', {})
  },
  updateNode(id, data) {
    return $patch('/nodeAPI/' + id + '/', data)
  },
  createNode(data) {
    return $post('/nodeAPI/', data)
  },
  delTask(id) {
    return $delete('/taskAPI/' + id + '/', {})
  },
  getTask(page_num, page_size, search) {
    return $get('/taskAPI/?ordering=-add_time&page_num=' + page_num + '&page_size=' + page_size + '&search=' + search, {})
  },
  readTask(id) {
    return $get('/taskAPI/' + id + '/', {})
  },
  updateTask(id, data) {
    return $patch('/taskAPI/' + id + '/', data)
  },
  createTask(data) {
    return $post('/taskAPI/', data)
  },
  delGroup(id) {
    return $delete('/groupAPI/' + id + '/', {})
  },
  delJira(id) {
    return $delete('/jiraAPI/' + id + '/', {})
  },
  getProject() {
    return $get('/relation/', {})
  },
  delProject(id) {
    return $delete('/projectAPI/' + id + '/', {})
  },
  updateProject(id, data) {
    return $put('/projectAPI/' + id + '/', data)
  },
  createProject(data) {
    return $post('/projectAPI/', data)
  },
  getInfo(page_num, page_size, search) {
    return $get('/projects/?ordering=-add_time&page_num=' + page_num + '&page_size=' + page_size + '&search=' + search, {})
  },
  readInfo(id) {
    return $get('/projectAPI/' + id + '/', {})
  },
  releaseInfo() {
    return $get('/projectAPI/', {})
  },
  sendInfo(data) {
    return $rainbow('/updateParams/', data)
  },
  delInfo(data) {
    return $rainbow('/deleteParams/', data)
  },
  uploadJson(id, data) {
    return $patch('/upload/' + id + '/', data, true)
  }
}
