const $ = sel => document.querySelector(sel)
const $$ = sel => Array.from(document.querySelectorAll(sel))

let ADMIN_TOKEN = ''
const base = '/api/admin/messages'

function setTokenFromInput(){
  const el = document.querySelector('#token-input')
  ADMIN_TOKEN = el ? el.value.trim() : ''
  const btn = document.querySelector('#save-token')
  if(ADMIN_TOKEN) btn.textContent = 'Saved'
  else btn.textContent = 'Save'
}

async function api(path, opts={}){
  const headers = opts.headers || {}
  if(ADMIN_TOKEN) headers['x-admin-token'] = ADMIN_TOKEN
  const res = await fetch(path, {...opts, headers})
  if(!res.ok) throw new Error(await res.text())
  return res.json()
}

async function loadList(){
  try{
    const data = await api(base)
    const ul = document.querySelector('#messages-list')
    ul.innerHTML = ''
    data.sort((a,b)=> new Date(b.created)-new Date(a.created))
    for(const item of data){
      const li = document.createElement('li')
      li.dataset.key = item.key
      li.innerHTML = `<strong>${item.name||'—'}</strong><div class="meta">${item.email||''} • ${new Date(item.created).toLocaleString()}</div>`
      li.addEventListener('click', ()=> showDetail(item.key))
      ul.appendChild(li)
    }
  }catch(err){
    alert('Error loading messages: '+err.message)
  }
}

async function showDetail(key){
  try{
    const item = await api(base+`/${encodeURIComponent(key)}`)
    const container = document.querySelector('#detail-inner')
    container.innerHTML = `
      <h3>${item.name||'—'}</h3>
      <div class="meta">${item.email||''} • ${new Date(item.created).toLocaleString()}</div>
      <hr/>
      <pre>${JSON.stringify(item.payload,null,2)}</pre>
      <div class="actions"><button id="delete-btn" data-key="${key}">Delete</button></div>
    `
    const del = document.querySelector('#delete-btn')
    if(del) del.addEventListener('click', ()=> deleteMessage(key))
  }catch(err){
    alert('Error loading message: '+err.message)
  }
}

async function deleteMessage(key){
  if(!confirm('Delete this message?')) return
  try{
    await api(base+`/${encodeURIComponent(key)}`, {method:'DELETE'})
    loadList()
    $('#detail').innerHTML = '<em>Deleted.</em>'
  }catch(err){
    alert('Error deleting message: '+err.message)
  }
}

function setup(){
  const save = document.querySelector('#save-token')
  if(save) save.addEventListener('click', ()=>{ setTokenFromInput(); loadList() })
  const tokenInput = document.querySelector('#token-input')
  if(tokenInput) tokenInput.addEventListener('keydown', e=>{ if(e.key==='Enter'){ setTokenFromInput(); loadList() } })
  const refresh = document.querySelector('#refresh')
  if(refresh) refresh.addEventListener('click', loadList)
  loadList()
}

window.addEventListener('DOMContentLoaded', setup)
