// API 基础地址
const BASE_URL = 'http://localhost:8000'

// 通用请求函数
async function request(path, options = {}) {
  const token = localStorage.getItem('ms_token')

  const res = await fetch(BASE_URL + path, {
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      ...options.headers
    },
    ...options
  })

  const data = await res.json()

  if (!res.ok) {
    throw new Error(data.detail || '请求失败')
  }

  return data
}

// ── 认证相关 ──
const Auth = {
  // 注册
  async register(username, password) {
    return request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    })
  },

  // 登录
  async login(username, password) {
    return request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    })
  },

  // 保存登录状态
  saveLogin(data) {
    localStorage.setItem('ms_token', data.access_token)
    localStorage.setItem('ms_user', JSON.stringify(data.user))
  },

  // 退出登录
  logout() {
    localStorage.removeItem('ms_token')
    localStorage.removeItem('ms_user')
    window.location.href = 'index.html'
  },

  // 获取当前用户
  getUser() {
    const u = localStorage.getItem('ms_user')
    return u ? JSON.parse(u) : null
  },

  // 是否已登录
  isLoggedIn() {
    return !!localStorage.getItem('ms_token')
  }
}

// ── 视频相关 ──
const VideoAPI = {
  // 获取视频列表
  async getList(params = {}) {
    const query = new URLSearchParams(params).toString()
    return request(`/api/videos/?${query}`)
  },

  // 获取单个视频
  async getOne(id) {
    return request(`/api/videos/${id}`)
  }
}