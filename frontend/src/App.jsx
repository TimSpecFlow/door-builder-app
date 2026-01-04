import React, { useState, useEffect, useCallback } from 'react'

function useDebouncedEffect(fn, deps, delay) {
  useEffect(() => {
    const id = setTimeout(() => fn(), delay)
    return () => clearTimeout(id)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...(deps || []), delay])
}

export default function App() {
  const [width, setWidth] = useState(36)
  const [height, setHeight] = useState(80)
  const [material, setMaterial] = useState('wood')
  const [hardware, setHardware] = useState({ hinges: true, handle: true, lockset: false })
  const [estimate, setEstimate] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const hardwareList = Object.keys(hardware)

  const compute = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const body = {
        width: Number(width),
        height: Number(height),
        material,
        hardware: hardwareList.filter(h => hardware[h])
      }

      const res = await fetch('/api/estimate/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
      if (!res.ok) throw new Error('Estimate request failed')
      const data = await res.json()
      setEstimate(data.estimate)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [width, height, material, hardware])

  // debounce rapid input changes
  useDebouncedEffect(() => { compute() }, [width, height, material, hardware], 350)

  function toggleHardware(name) {
    setHardware(h => ({ ...h, [name]: !h[name] }))
  }

  return (
    <div className="container">
      <h1>Door Spec Builder</h1>
      <div className="row">
        <label>Width (in)</label>
        <input type="number" value={width} onChange={e => setWidth(e.target.value)} />
      </div>
      <div className="row">
        <label>Height (in)</label>
        <input type="number" value={height} onChange={e => setHeight(e.target.value)} />
      </div>
      <div className="row">
        <label>Material</label>
        <select value={material} onChange={e => setMaterial(e.target.value)}>
          <option value="wood">Wood</option>
          <option value="steel">Steel</option>
          <option value="fiberglass">Fiberglass</option>
        </select>
      </div>
      <div className="row">
        <label>Hardware</label>
        <div className="checkboxes">
          {hardwareList.map(h => (
            <label key={h} className="checkbox">
              <input type="checkbox" checked={!!hardware[h]} onChange={() => toggleHardware(h)} /> {h}
            </label>
          ))}
        </div>
      </div>

      <div className="estimate">
        {loading ? (<div className="muted">Calculating...</div>) : error ? (<div className="error">{error}</div>) : (
          <div className="price">Estimate: {estimate != null ? `$${estimate}` : '—'}</div>
        )}
      </div>
    </div>
  )
}
