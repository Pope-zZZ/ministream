// 给所有页面的搜索框绑定搜索功能
document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.querySelector('.nav-search input')
  if (!searchInput) return

  // 读取当前搜索词（如果是搜索结果页）
  const params = new URLSearchParams(window.location.search)
  const currentKeyword = params.get('keyword')
  if (currentKeyword) {
    searchInput.value = currentKeyword
  }

  // 按回车跳转到搜索结果页
  searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const keyword = searchInput.value.trim()
      if (keyword) {
        window.location.href = `search.html?keyword=${encodeURIComponent(keyword)}`
      }
    }
  })

  // 点搜索图标也能触发
  const searchIcon = document.querySelector('.nav-search svg')
  if (searchIcon) {
    searchIcon.style.cursor = 'pointer'
    searchIcon.addEventListener('click', () => {
      const keyword = searchInput.value.trim()
      if (keyword) {
        window.location.href = `search.html?keyword=${encodeURIComponent(keyword)}`
      }
    })
  }
})