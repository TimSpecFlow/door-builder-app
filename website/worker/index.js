// Cloudflare Worker to store contact form submissions in a Cloudflare KV namespace.
// Bind a KV namespace with binding name `CONTACTS_KV` in `wrangler.toml`.

export default {
  async fetch(request, env) {
    if (request.method.toUpperCase() !== 'POST') {
      return new Response('Method not allowed', { status: 405 })
    }

    let data
    try {
      data = await request.json()
    } catch (err) {
      return new Response(JSON.stringify({ error: 'Invalid JSON' }), { status: 400, headers: { 'Content-Type': 'application/json' } })
    }

    const name = (data.name || '').trim()
    const email = (data.email || '').trim()
    const message = (data.message || '').trim()

    if (!name || !email || !message) {
      return new Response(JSON.stringify({ error: 'Missing required fields' }), { status: 400, headers: { 'Content-Type': 'application/json' } })
    }

    if (!env.CONTACTS_KV) {
      return new Response(JSON.stringify({ error: 'KV binding not configured' }), { status: 500, headers: { 'Content-Type': 'application/json' } })
    }

    // Create a record and store it in KV with a UUID key
    const id = (typeof crypto !== 'undefined' && crypto.randomUUID) ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(36).slice(2,9)}`
    const record = {
      id,
      name,
      email,
      message,
      created_at: new Date().toISOString()
    }

    try {
      await env.CONTACTS_KV.put(`contact:${id}`, JSON.stringify(record))
    } catch (err) {
      return new Response(JSON.stringify({ error: 'Failed to store message', detail: String(err) }), { status: 500, headers: { 'Content-Type': 'application/json' } })
    }

    return new Response(JSON.stringify({ ok: true, id }), { status: 200, headers: { 'Content-Type': 'application/json' } })
  }
}
