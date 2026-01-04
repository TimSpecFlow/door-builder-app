// Admin Worker for reading contact submissions from CONTACTS_KV
// Protects endpoints with an ADMIN_TOKEN header

export default {
  async fetch(request, env) {
    const headerToken = request.headers.get('x-admin-token')
    if (!env.ADMIN_TOKEN || headerToken !== env.ADMIN_TOKEN) {
      return new Response('Unauthorized', { status: 401 })
    }

    const url = new URL(request.url)
    const path = url.pathname.replace(/\/+$/, '')

    // GET /messages -> list recent messages (limit 100)
    if (request.method === 'GET' && path.endsWith('/messages')) {
      try {
        const list = await env.CONTACTS_KV.list({ prefix: 'contact:', limit: 100 })
        const keys = list.keys.map(k => k.name)
        const items = await Promise.all(keys.map(async key => {
          const v = await env.CONTACTS_KV.get(key)
          try { return JSON.parse(v) } catch { return { key, value: v } }
        }))
        return new Response(JSON.stringify({ items }), { headers: { 'Content-Type': 'application/json' } })
      } catch (err) {
        return new Response(JSON.stringify({ error: 'KV list error', detail: String(err) }), { status: 500, headers: { 'Content-Type': 'application/json' } })
      }
    }

    // GET /messages/:id -> fetch a single message
    const singleMatch = path.match(/\/messages\/(.+)$/)
    if (request.method === 'GET' && singleMatch) {
      const id = singleMatch[1]
      const key = `contact:${id}`
      const v = await env.CONTACTS_KV.get(key)
      if (!v) return new Response(JSON.stringify({ error: 'Not found' }), { status: 404, headers: { 'Content-Type': 'application/json' } })
      return new Response(v, { headers: { 'Content-Type': 'application/json' } })
    }

    // DELETE /messages/:id -> delete a message
    if (request.method === 'DELETE' && singleMatch) {
      const id = singleMatch[1]
      const key = `contact:${id}`
      await env.CONTACTS_KV.delete(key)
      return new Response(JSON.stringify({ ok: true }), { headers: { 'Content-Type': 'application/json' } })
    }

    return new Response('Not found', { status: 404 })
  }
}
