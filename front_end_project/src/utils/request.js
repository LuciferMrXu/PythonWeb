import axios from 'axios'
import { MessageBox, Message } from 'element-ui'
import store from '@/store'
import { getToken } from '@/utils/auth'

// create an axios instance
const service = axios.create({
  baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000 // request timeout
})

// request interceptor
service.interceptors.request.use(
  config => {
    // do something before request is sent

    if (store.getters.token) {
      // let each request carry token
      // ['X-Token'] is a custom headers key
      // please modify it according to the actual situation
      config.headers['JWT'] = getToken()
    }
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// // response interceptor
// service.interceptors.response.use(
//   /**
//    * If you want to get http information such as headers or status
//    * Please return  response => response
//   */

//   /**
//    * Determine the request status by custom code
//    * Here is just an example
//    * You can also judge the status by HTTP Status Code
//    */
//   response => {
//     const res = response.data

//     // if the custom code is not 20000, it is judged as an error.
//     if (res.code !== 200) {
//       debugger
//       Message({
//         message: res.message || 'Error',
//         type: 'error',
//         duration: 5 * 1000
//       })

//       // 50008: Illegal token; 50012: Other clients logged in; 50014: Token expired;
//       if (res.code === 508 || res.code === 512 || res.code === 514) {
//         // to re-login
//         MessageBox.confirm('You have been logged out, you can cancel to stay on this page, or log in again', 'Confirm logout', {
//           confirmButtonText: 'Re-Login',
//           cancelButtonText: 'Cancel',
//           type: 'warning'
//         }).then(() => {
//           store.dispatch('user/resetToken').then(() => {
//             location.reload()
//           })
//         })
//       }
//       return Promise.reject(new Error(res.message || 'Error'))
//     } else {
//       return res
//     }
//   },
//   error => {
//     console.log('err' + error) // for debug
//     Message({
//       message: error.message,
//       type: 'error',
//       duration: 5 * 1000
//     })
//     return Promise.reject(error)
//   }
// )

// export default service

function rdNum(n) {
  var rnd = ''
  for (var i = 0; i < n; i++) {
    rnd += Math.floor(Math.random() * 10)
  }
  return rnd
}

function createHeader(token, isformdata) {
  const contentType = isformdata ? 'multipart/form-data' : 'application/json'
  if (store.getters.token) {
    token = getToken()
  }
  return {
    'Content-Type': contentType,
    'time': new Date().getTime(),
    'salt': rdNum(6),
    'Authorization': 'JWT ' + token
    // 'token': token ? `${token}` : ''
  }
}

// 响应拦截器
axios.interceptors.response.use(
  response => {
    if (response.status === 200 || response.status === 201 || response.status === 204) {
      if (response.data && response.data.code === 302) {
        window.location = response.data.redirectUrl
        return
      }

      /* if (response.data === undefined) {
        data = JSON.parse(response.request.responseText)
      } else {
        data = response.data.data
      }*/

      const data = response.data
      if (response.data.message) {
        Message.success(response.data.message)
      }
      return { data }
    } else {
      Message.error(response.data.message || '请求失败')
      return Promise.reject()
    }
  },
  error => {
    // cas 302跨域异常
    if (error.message === 'Network Error') {
      MessageBox.confirm('You have been logged out, you can cancel to stay on this page, or log in again', 'Confirm logout', {
        confirmButtonText: 'Re-Login',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(() => {
        store.dispatch('user/resetToken').then(() => {
          location.reload()
        })
      })
    }
    // 401 过期，重登
    if (error.response) {
      if (error.response.status === 400) {
        Message.error(error.response.data)
        // window.location = '/cas/login'
        return Promise.reject(error)
      }
      if (error.response.status === 401) {
        Message.error('登录过期，请重新登录')
        // window.location = '/cas/login'
        return Promise.reject(error)
      }
      if (error.response.status === 403) {
        Message.error('无权访问，请先登录')
        // window.location = '/cas/login'
        return Promise.reject(error)
      }
      if (error.response.status === 500) {
        Message.error('内部服务器异常')
        return Promise.reject(error)
      }
    }
    if (error.response.data && error.response.data.message) {
      // Message.error(error.response.data.message)
      Message({
        message: error.response.data.message,
        type: 'error',
        showClose: true
        // duration:0
      })
    }
    return Promise.reject(error)
  }
)

const baseURL = process.env.VUE_APP_BASE_API
// GET请求
export const $get = function(method, params) {
  return new Promise((resolve, reject) => {
    axios({
      method: 'get',
      url: method,
      headers: createHeader(getToken()),
      params,
      baseURL: baseURL
    })
      .then(res => {
        resolve(res)
      })
      .catch(error => {
        reject(error)
      })
  })
}

// POST请求
export const $post = function(method, param, isformdata) {
  return new Promise((resolve, reject) => {
    axios({
      method: 'post',
      url: method,
      headers: createHeader(getToken(), isformdata),
      data: param || '',
      baseURL: baseURL
    })
      .then(res => {
        resolve(res)
      })
      .catch(error => {
        reject(error)
      })
  })
}

// DELETE请求
export const $delete = function(method, params) {
  return new Promise((resolve, reject) => {
    axios({
      method: 'delete',
      url: method,
      headers: createHeader(getToken()),
      params,
      baseURL: baseURL
    })
      .then(res => {
        resolve(res)
      })
      .catch(error => {
        reject(error)
      })
  })
}

// PUT请求
export const $put = function(method, params, isformdata) {
  return new Promise((resolve, reject) => {
    axios({
      method: 'put',
      url: method,
      headers: createHeader(getToken(), isformdata),
      data: params || '',
      baseURL: baseURL
    })
      .then(res => {
        resolve(res)
      })
      .catch(error => {
        reject(error)
      })
  })
}

// PATCH请求
export const $patch = function(method, params, isformdata) {
  return new Promise((resolve, reject) => {
    axios({
      method: 'patch',
      url: method,
      headers: createHeader(getToken(), isformdata),
      data: params || '',
      baseURL: baseURL
    })
      .then(res => {
        resolve(res)
      })
      .catch(error => {
        reject(error)
      })
  })
}

// 特殊接口，与彩虹平台对接
export const $rainbow = function(method, param) {
  return new Promise((resolve, reject) => {
    axios({
      method: 'post',
      url: method,
      headers: createHeader(getToken()),
      data: param || '',
      // baseURL: 'http://10.3.17.31:8081/api'
      baseURL: 'http://172.31.187.4:7004/api'
      // baseURL: 'http://172.31.130.108:7004/api'
      // baseURL: 'http://172.31.128.180:7004/api'
    })
      .then(res => {
        resolve(res)
      })
      .catch(error => {
        reject(error)
      })
  })
}
