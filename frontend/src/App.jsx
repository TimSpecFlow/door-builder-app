import React, { useState, useEffect, useCallback, useRef } from 'react'

function useDebouncedEffect(fn, deps, delay) {
  useEffect(() => {
    const id = setTimeout(() => fn(), delay)
    return () => clearTimeout(id)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...(deps || []), delay])
}

export default function App() {
  // Door Slab Dimensions
  const [width, setWidth] = useState(36)
  const [height, setHeight] = useState(80)
  const [thickness, setThickness] = useState('1-3/4')
  
  // Frame/Jamb Specifications
  const [jambWidth, setJambWidth] = useState(4.5)
  const [jambMaterial, setJambMaterial] = useState('wood')
  
  // Rough Opening
  const [roughOpeningWidth, setRoughOpeningWidth] = useState(38)
  const [roughOpeningHeight, setRoughOpeningHeight] = useState(82)
  
  // Door Configuration
  const [doorType, setDoorType] = useState('interior')
  const [swingDirection, setSwingDirection] = useState('left-inswing')
  const [material, setMaterial] = useState('wood')
  const [panelStyle, setPanelStyle] = useState('flat')
  
  // Glass/Lite Options
  const [hasGlass, setHasGlass] = useState(false)
  const [glassType, setGlassType] = useState('clear')
  const [litePattern, setLitePattern] = useState('none')
  
  // Hardware Prep
  const [hingeCount, setHingeCount] = useState(3)
  const [hingePosition, setHingePosition] = useState('standard')
  const [boreSize, setBoreSize] = useState('2-1/8')
  const [backset, setBackset] = useState('2-3/8')
  const [prepType, setPrepType] = useState('single-bore')
  
  // Hardware Selection - Extended with SecLock product categories
  const [hardware, setHardware] = useState({
    hinges: true,
    handle: true,
    lockset: false,
    deadbolt: false,
    doorCloser: false,
    kickplate: false,
    weatherstrip: false,
    threshold: false,
    // Electronic Access
    electric_strike: false,
    maglock: false,
    keypad: false,
    // Exit Devices
    panic: false,
    // Accessories
    auto_operator: false,
    ic_core: false
  })
  
  // Fire Rating
  const [fireRating, setFireRating] = useState('none')
  
  // Specialty Door Requirements (ASSA ABLOY DSS)
  const [specialtyRequirements, setSpecialtyRequirements] = useState({
    acoustical: false,
    bulletResistant: false,
    blastResistant: false,
    hurricaneResistant: false,
    attackResistant: false,
    floodResistant: false,
    leadLined: false,
    emiShielding: false
  })
  
  // Finishing
  const [finish, setFinish] = useState('unfinished')
  const [finishColor, setFinishColor] = useState('')
  
  const [estimate, setEstimate] = useState(null)
  const [estimateBreakdown, setEstimateBreakdown] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  
  // Product Recommendations
  const [recommendations, setRecommendations] = useState(null)
  const [loadingRecs, setLoadingRecs] = useState(false)
  const [showRecommendations, setShowRecommendations] = useState(false)
  
  // PDF Quote
  const [generatingPdf, setGeneratingPdf] = useState(false)
  
  // AI Upload states
  const [uploadMode, setUploadMode] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadResult, setUploadResult] = useState(null)
  const [dragActive, setDragActive] = useState(false)
  const fileInputRef = useRef(null)
  
  // Collapsible sections
  const [expandedSections, setExpandedSections] = useState({
    dimensions: true,
    frame: true,
    configuration: true,
    specialty: false,
    glass: false,
    hardwarePrep: false,
    hardwareSelection: true,
    finishing: false,
    recommendations: true
  })

  const toggleSection = (section) => {
    setExpandedSections(prev => ({ ...prev, [section]: !prev[section] }))
  }

  const compute = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const body = {
        width: Number(width),
        height: Number(height),
        thickness,
        jambWidth: Number(jambWidth),
        jambMaterial,
        roughOpeningWidth: Number(roughOpeningWidth),
        roughOpeningHeight: Number(roughOpeningHeight),
        doorType,
        swingDirection,
        material,
        panelStyle,
        hasGlass,
        glassType: hasGlass ? glassType : null,
        litePattern: hasGlass ? litePattern : null,
        hingeCount: Number(hingeCount),
        hingePosition,
        boreSize,
        backset,
        prepType,
        hardware: Object.keys(hardware).filter(h => hardware[h]),
        fireRating,
        finish,
        finishColor: finish !== 'unfinished' ? finishColor : null
      }

      const res = await fetch('/api/estimate/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
      if (!res.ok) throw new Error('Estimate request failed')
      const data = await res.json()
      setEstimate(data.estimate)
      setEstimateBreakdown(data.breakdown)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [width, height, thickness, jambWidth, jambMaterial, roughOpeningWidth, roughOpeningHeight,
      doorType, swingDirection, material, panelStyle, hasGlass, glassType, litePattern,
      hingeCount, hingePosition, boreSize, backset, prepType, hardware, fireRating, finish, finishColor])

  useDebouncedEffect(() => { compute() }, [width, height, thickness, material, hardware, hasGlass, fireRating, finish], 350)

  function toggleHardware(name) {
    setHardware(h => ({ ...h, [name]: !h[name] }))
  }

  // Format hardware names for display
  function formatHardwareName(name) {
    const nameMap = {
      'hinges': 'Hinges',
      'handle': 'Handle/Lever',
      'lockset': 'Lockset',
      'deadbolt': 'Deadbolt',
      'doorCloser': 'Door Closer',
      'kickplate': 'Kick Plate',
      'weatherstrip': 'Weatherstripping',
      'threshold': 'Threshold',
      'electric_strike': 'Electric Strike',
      'maglock': 'Magnetic Lock',
      'keypad': 'Keypad Lock',
      'panic': 'Panic/Exit Device',
      'auto_operator': 'Auto Operator (ADA)',
      'ic_core': 'Interchangeable Core'
    }
    return nameMap[name] || name.replace(/([A-Z])/g, ' $1').replace(/_/g, ' ').replace(/^./, s => s.toUpperCase())
  }

  // Toggle specialty requirements
  function toggleSpecialty(name) {
    setSpecialtyRequirements(s => ({ ...s, [name]: !s[name] }))
  }

  // Format specialty requirement names for display
  function formatSpecialtyName(name) {
    const nameMap = {
      'acoustical': 'Acoustical (STC Rated)',
      'bulletResistant': 'Bullet Resistant',
      'blastResistant': 'Blast Resistant',
      'hurricaneResistant': 'Hurricane/Tornado Resistant',
      'attackResistant': 'Attack/Forced Entry Resistant',
      'floodResistant': 'Flood Resistant',
      'leadLined': 'Lead-Lined (Radiation)',
      'emiShielding': 'EMI/RFI Shielding'
    }
    return nameMap[name] || name
  }

  // Fetch product recommendations
  async function fetchRecommendations() {
    setLoadingRecs(true)
    setShowRecommendations(true)
    
    try {
      const body = {
        width: Number(width),
        height: Number(height),
        thickness,
        doorType,
        material,
        hasGlass,
        glassType: hasGlass ? glassType : null,
        hardware: Object.keys(hardware).filter(h => hardware[h]),
        fireRating,
        prepType,
        // Specialty requirements for ASSA ABLOY DSS doors
        ...specialtyRequirements
      }

      const res = await fetch('/api/recommendations/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })
      
      if (!res.ok) throw new Error('Failed to fetch recommendations')
      const data = await res.json()
      setRecommendations(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoadingRecs(false)
    }
  }

  // Generate PDF Quote and Save to CRM
  async function downloadQuote() {
    setGeneratingPdf(true)
    setError(null)
    
    try {
      const specs = {
        width: Number(width),
        height: Number(height),
        thickness,
        jambWidth: Number(jambWidth),
        jambMaterial,
        roughOpeningWidth: Number(roughOpeningWidth),
        roughOpeningHeight: Number(roughOpeningHeight),
        doorType,
        swingDirection,
        material,
        panelStyle,
        hasGlass,
        glassType: hasGlass ? glassType : null,
        litePattern: hasGlass ? litePattern : null,
        hingeCount: Number(hingeCount),
        hingePosition,
        boreSize,
        backset,
        prepType,
        hardware: Object.keys(hardware).filter(h => hardware[h]),
        fireRating,
        finish,
        finishColor: finish !== 'unfinished' ? finishColor : null
      }

      const body = {
        specs,
        estimate: {
          estimate: estimate,
          breakdown: estimateBreakdown || {}
        },
        recommendations: recommendations?.distributors?.flatMap(d => d.recommendations) || []
      }

      const res = await fetch('/api/generate-quote/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      })

      if (!res.ok) throw new Error('Failed to generate quote')

      // Download the PDF
      const blob = await res.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'SpecFlow_Quote.pdf'
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)

      // Save to CRM (Excel)
      await fetch('/api/save-to-crm/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          specs,
          estimate: estimate,
          breakdown: estimateBreakdown || {}
        })
      })

    } catch (err) {
      setError('Failed to generate PDF: ' + err.message)
    } finally {
      setGeneratingPdf(false)
    }
  }

  // Auto-calculate rough opening
  useEffect(() => {
    setRoughOpeningWidth(Number(width) + 2)
    setRoughOpeningHeight(Number(height) + 2.5)
  }, [width, height])

  // AI Measurement Parser
  async function parseImage(file) {
    setUploading(true)
    setUploadResult(null)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('image', file)

      const res = await fetch('/api/parse-measurements/', {
        method: 'POST',
        body: formData
      })

      const data = await res.json()
      
      if (data.success && data.measurements) {
        setUploadResult(data)
        
        // Auto-fill the form with extracted measurements
        const m = data.measurements
        if (m.width) setWidth(m.width)
        if (m.height) setHeight(m.height)
        if (m.thickness) setThickness(m.thickness)
        if (m.jambWidth) setJambWidth(m.jambWidth)
        if (m.roughOpeningWidth) setRoughOpeningWidth(m.roughOpeningWidth)
        if (m.roughOpeningHeight) setRoughOpeningHeight(m.roughOpeningHeight)
        if (m.doorType) setDoorType(m.doorType)
        if (m.swingDirection) setSwingDirection(m.swingDirection)
        if (m.material) {
          const mat = m.material.toLowerCase()
          if (['wood', 'steel', 'fiberglass', 'aluminum', 'composite'].includes(mat)) {
            setMaterial(mat)
          }
        }
        if (m.panelStyle) setPanelStyle(m.panelStyle)
        if (m.hasGlass !== undefined) setHasGlass(m.hasGlass)
        if (m.glassType) setGlassType(m.glassType)
        if (m.hingeCount) setHingeCount(m.hingeCount)
        if (m.boreSize) setBoreSize(m.boreSize)
        if (m.backset) setBackset(m.backset)
        if (m.fireRating) setFireRating(m.fireRating)
        
        if (m.hardware && m.hardware.length > 0) {
          const newHardware = { ...hardware }
          Object.keys(newHardware).forEach(k => newHardware[k] = false)
          m.hardware.forEach(h => {
            const hw = h.toLowerCase()
            if (hw.includes('hinge')) newHardware.hinges = true
            if (hw.includes('handle') || hw.includes('lever') || hw.includes('knob')) newHardware.handle = true
            if (hw.includes('lockset') || hw.includes('lock set')) newHardware.lockset = true
            if (hw.includes('deadbolt') || hw.includes('dead bolt')) newHardware.deadbolt = true
            if (hw.includes('closer')) newHardware.doorCloser = true
            if (hw.includes('kick')) newHardware.kickplate = true
            if (hw.includes('weather')) newHardware.weatherstrip = true
            if (hw.includes('threshold') || hw.includes('sill')) newHardware.threshold = true
          })
          setHardware(newHardware)
        }
        
        setUploadMode(false)
      } else {
        setUploadResult(data)
        setError(data.error || 'Could not parse measurements from image')
      }
    } catch (err) {
      setError('Failed to process image: ' + err.message)
    } finally {
      setUploading(false)
    }
  }

  function handleFileSelect(e) {
    const file = e.target.files?.[0]
    if (file) parseImage(file)
  }

  function handleDrag(e) {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  function handleDrop(e) {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    const file = e.dataTransfer.files?.[0]
    if (file && file.type.startsWith('image/')) {
      parseImage(file)
    } else {
      setError('Please upload an image file (JPG, PNG, etc.)')
    }
  }

  const SectionHeader = ({ id, title, icon }) => (
    <div className="section-header" onClick={() => toggleSection(id)}>
      <span className="section-icon">{icon}</span>
      <h2>{title}</h2>
      <span className={`chevron ${expandedSections[id] ? 'open' : ''}`}>▼</span>
    </div>
  )

  return (
    <div className="container">
      <h1>Door Spec Builder</h1>
      
      {/* AI Upload Toggle */}
      <div className="ai-toggle">
        <button 
          className={`toggle-btn ${uploadMode ? 'active' : ''}`}
          onClick={() => setUploadMode(!uploadMode)}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>
            <circle cx="12" cy="13" r="4"/>
          </svg>
          {uploadMode ? 'Manual Entry' : 'AI Scan Measurements'}
        </button>
      </div>

      {uploadMode ? (
        /* AI Upload Zone */
        <div 
          className={`upload-zone ${dragActive ? 'drag-active' : ''} ${uploading ? 'uploading' : ''}`}
          onDragEnter={handleDrag}
          onDragOver={handleDrag}
          onDragLeave={handleDrag}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />
          
          {uploading ? (
            <div className="upload-content">
              <div className="spinner"></div>
              <p>Analyzing measurements...</p>
              <span className="upload-hint">AI is reading your document</span>
            </div>
          ) : (
            <div className="upload-content">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="17 8 12 3 7 8"/>
                <line x1="12" y1="3" x2="12" y2="15"/>
              </svg>
              <p>Drop image or click to upload</p>
              <span className="upload-hint">
                Supports handwritten notes, spec sheets, blueprints
              </span>
            </div>
          )}
        </div>
      ) : (
        /* Manual Entry Form */
        <div className="form-sections">
          
          {/* Door Slab Dimensions */}
          <section className="form-section">
            <SectionHeader id="dimensions" title="Door Slab Dimensions" icon="📐" />
            {expandedSections.dimensions && (
              <div className="section-content">
                <div className="row-grid">
                  <div className="field">
                    <label>Width (in)</label>
                    <input type="number" value={width} onChange={e => setWidth(e.target.value)} />
                  </div>
                  <div className="field">
                    <label>Height (in)</label>
                    <input type="number" value={height} onChange={e => setHeight(e.target.value)} />
                  </div>
                  <div className="field">
                    <label>Thickness</label>
                    <select value={thickness} onChange={e => setThickness(e.target.value)}>
                      <option value="1-3/8">1-3/8" (Interior)</option>
                      <option value="1-3/4">1-3/4" (Exterior)</option>
                      <option value="2">2" (Heavy Duty)</option>
                      <option value="2-1/4">2-1/4" (Commercial)</option>
                    </select>
                  </div>
                </div>
                <div className="hint">Standard sizes: 24", 28", 30", 32", 36" wide × 80" tall</div>
              </div>
            )}
          </section>

          {/* Frame/Jamb Specifications */}
          <section className="form-section">
            <SectionHeader id="frame" title="Frame & Jamb" icon="🚪" />
            {expandedSections.frame && (
              <div className="section-content">
                <div className="row-grid">
                  <div className="field">
                    <label>Jamb Width (in)</label>
                    <input type="number" step="0.125" value={jambWidth} onChange={e => setJambWidth(e.target.value)} />
                  </div>
                  <div className="field">
                    <label>Jamb Material</label>
                    <select value={jambMaterial} onChange={e => setJambMaterial(e.target.value)}>
                      <option value="wood">Wood</option>
                      <option value="mdf">MDF</option>
                      <option value="steel">Steel</option>
                      <option value="aluminum">Aluminum</option>
                      <option value="composite">Composite</option>
                    </select>
                  </div>
                </div>
                <div className="row-grid">
                  <div className="field">
                    <label>Rough Opening Width</label>
                    <input type="number" step="0.25" value={roughOpeningWidth} onChange={e => setRoughOpeningWidth(e.target.value)} />
                  </div>
                  <div className="field">
                    <label>Rough Opening Height</label>
                    <input type="number" step="0.25" value={roughOpeningHeight} onChange={e => setRoughOpeningHeight(e.target.value)} />
                  </div>
                </div>
                <div className="hint">Jamb width should match wall thickness (2x4 wall ≈ 4.5")</div>
              </div>
            )}
          </section>

          {/* Door Configuration */}
          <section className="form-section">
            <SectionHeader id="configuration" title="Door Configuration" icon="⚙️" />
            {expandedSections.configuration && (
              <div className="section-content">
                <div className="row-grid">
                  <div className="field">
                    <label>Door Type</label>
                    <select value={doorType} onChange={e => setDoorType(e.target.value)}>
                      <option value="interior">Interior</option>
                      <option value="exterior-entry">Exterior Entry</option>
                      <option value="exterior-patio">Patio Door</option>
                      <option value="closet">Closet</option>
                      <option value="barn">Barn Door</option>
                      <option value="pocket">Pocket Door</option>
                      <option value="bifold">Bifold</option>
                      <option value="commercial">Commercial</option>
                    </select>
                  </div>
                  <div className="field">
                    <label>Swing Direction</label>
                    <select value={swingDirection} onChange={e => setSwingDirection(e.target.value)}>
                      <option value="left-inswing">Left Hand Inswing</option>
                      <option value="right-inswing">Right Hand Inswing</option>
                      <option value="left-outswing">Left Hand Outswing</option>
                      <option value="right-outswing">Right Hand Outswing</option>
                    </select>
                  </div>
                </div>
                <div className="row-grid">
                  <div className="field">
                    <label>Material</label>
                    <select value={material} onChange={e => setMaterial(e.target.value)}>
                      <option value="wood">Solid Wood</option>
                      <option value="wood-hollow">Hollow Core Wood</option>
                      <option value="steel">Steel</option>
                      <option value="fiberglass">Fiberglass</option>
                      <option value="aluminum">Aluminum</option>
                      <option value="composite">Composite</option>
                    </select>
                  </div>
                  <div className="field">
                    <label>Panel Style</label>
                    <select value={panelStyle} onChange={e => setPanelStyle(e.target.value)}>
                      <option value="flat">Flat/Flush</option>
                      <option value="2-panel">2 Panel</option>
                      <option value="4-panel">4 Panel</option>
                      <option value="6-panel">6 Panel</option>
                      <option value="shaker">Shaker</option>
                      <option value="craftsman">Craftsman</option>
                      <option value="french">French</option>
                      <option value="louvered">Louvered</option>
                    </select>
                  </div>
                </div>
                <div className="field">
                  <label>Fire Rating</label>
                  <select value={fireRating} onChange={e => setFireRating(e.target.value)}>
                    <option value="none">None</option>
                    <option value="20-min">20 Minute</option>
                    <option value="45-min">45 Minute</option>
                    <option value="60-min">60 Minute (1 Hour)</option>
                    <option value="90-min">90 Minute</option>
                  </select>
                </div>
              </div>
            )}
          </section>

          {/* Specialty Requirements - ASSA ABLOY DSS */}
          <section className="form-section">
            <SectionHeader id="specialty" title="Specialty Door Requirements" icon="🛡️" />
            {expandedSections.specialty && (
              <div className="section-content">
                <p className="section-description">
                  Select specialty requirements for doors requiring enhanced protection. 
                  Products from ASSA ABLOY Door Security Solutions (Ceco Door, Curries, Baron).
                </p>
                <div className="hardware-grid">
                  {Object.keys(specialtyRequirements).map(s => (
                    <label key={s} className={`checkbox hardware-item ${specialtyRequirements[s] ? 'selected' : ''}`}>
                      <input type="checkbox" checked={!!specialtyRequirements[s]} onChange={() => toggleSpecialty(s)} />
                      <span className="hardware-name">{formatSpecialtyName(s)}</span>
                    </label>
                  ))}
                </div>
                <div className="hint">Specialty doors available for commercial/industrial applications with specific protection needs.</div>
              </div>
            )}
          </section>

          {/* Glass/Lite Options */}
          <section className="form-section">
            <SectionHeader id="glass" title="Glass / Lite Options" icon="🪟" />
            {expandedSections.glass && (
              <div className="section-content">
                <div className="field checkbox-field">
                  <label className="checkbox">
                    <input type="checkbox" checked={hasGlass} onChange={e => setHasGlass(e.target.checked)} />
                    Include Glass Panel
                  </label>
                </div>
                {hasGlass && (
                  <div className="row-grid">
                    <div className="field">
                      <label>Glass Type</label>
                      <select value={glassType} onChange={e => setGlassType(e.target.value)}>
                        <option value="clear">Clear</option>
                        <option value="frosted">Frosted</option>
                        <option value="textured">Textured</option>
                        <option value="rain">Rain Glass</option>
                        <option value="low-e">Low-E</option>
                        <option value="tempered">Tempered</option>
                        <option value="impact">Impact Resistant</option>
                      </select>
                    </div>
                    <div className="field">
                      <label>Lite Pattern</label>
                      <select value={litePattern} onChange={e => setLitePattern(e.target.value)}>
                        <option value="full">Full Lite</option>
                        <option value="half">Half Lite</option>
                        <option value="3/4">3/4 Lite</option>
                        <option value="1/4">1/4 Lite</option>
                        <option value="9-lite">9 Lite</option>
                        <option value="15-lite">15 Lite</option>
                        <option value="sidelight">Sidelight</option>
                        <option value="fanlight">Fanlight/Transom</option>
                      </select>
                    </div>
                  </div>
                )}
              </div>
            )}
          </section>

          {/* Hardware Prep */}
          <section className="form-section">
            <SectionHeader id="hardwarePrep" title="Hardware Prep" icon="🔧" />
            {expandedSections.hardwarePrep && (
              <div className="section-content">
                <div className="row-grid">
                  <div className="field">
                    <label>Hinge Count</label>
                    <select value={hingeCount} onChange={e => setHingeCount(e.target.value)}>
                      <option value="2">2 Hinges</option>
                      <option value="3">3 Hinges (Standard)</option>
                      <option value="4">4 Hinges (Heavy)</option>
                    </select>
                  </div>
                  <div className="field">
                    <label>Hinge Position</label>
                    <select value={hingePosition} onChange={e => setHingePosition(e.target.value)}>
                      <option value="standard">Standard (7", 11", 11" from top)</option>
                      <option value="commercial">Commercial (10" spacing)</option>
                      <option value="custom">Custom</option>
                    </select>
                  </div>
                </div>
                <div className="row-grid">
                  <div className="field">
                    <label>Bore Size</label>
                    <select value={boreSize} onChange={e => setBoreSize(e.target.value)}>
                      <option value="2-1/8">2-1/8" (Standard)</option>
                      <option value="1-1/2">1-1/2" (Deadbolt only)</option>
                      <option value="none">No Bore</option>
                    </select>
                  </div>
                  <div className="field">
                    <label>Backset</label>
                    <select value={backset} onChange={e => setBackset(e.target.value)}>
                      <option value="2-3/8">2-3/8" (Residential)</option>
                      <option value="2-3/4">2-3/4" (Commercial)</option>
                      <option value="5">5" (Commercial Heavy)</option>
                    </select>
                  </div>
                </div>
                <div className="field">
                  <label>Lock Prep Type</label>
                  <select value={prepType} onChange={e => setPrepType(e.target.value)}>
                    <option value="single-bore">Single Bore (Handle only)</option>
                    <option value="double-bore">Double Bore (Handle + Deadbolt)</option>
                    <option value="mortise">Mortise Lock</option>
                    <option value="panic">Panic Hardware</option>
                    <option value="none">No Prep</option>
                  </select>
                </div>
              </div>
            )}
          </section>

          {/* Hardware Selection */}
          <section className="form-section">
            <SectionHeader id="hardwareSelection" title="Hardware Selection" icon="🔩" />
            {expandedSections.hardwareSelection && (
              <div className="section-content">
                <div className="hardware-category">
                  <h4>Basic Hardware</h4>
                  <div className="hardware-grid">
                    {['hinges', 'handle', 'lockset', 'deadbolt', 'doorCloser', 'kickplate'].map(h => (
                      <label key={h} className="checkbox hardware-item">
                        <input type="checkbox" checked={!!hardware[h]} onChange={() => toggleHardware(h)} />
                        <span className="hardware-name">{formatHardwareName(h)}</span>
                      </label>
                    ))}
                  </div>
                </div>
                
                <div className="hardware-category">
                  <h4>Weatherproofing</h4>
                  <div className="hardware-grid">
                    {['weatherstrip', 'threshold'].map(h => (
                      <label key={h} className="checkbox hardware-item">
                        <input type="checkbox" checked={!!hardware[h]} onChange={() => toggleHardware(h)} />
                        <span className="hardware-name">{formatHardwareName(h)}</span>
                      </label>
                    ))}
                  </div>
                </div>
                
                <div className="hardware-category">
                  <h4>Electronic Access Control</h4>
                  <div className="hardware-grid">
                    {['electric_strike', 'maglock', 'keypad'].map(h => (
                      <label key={h} className="checkbox hardware-item">
                        <input type="checkbox" checked={!!hardware[h]} onChange={() => toggleHardware(h)} />
                        <span className="hardware-name">{formatHardwareName(h)}</span>
                      </label>
                    ))}
                  </div>
                </div>
                
                <div className="hardware-category">
                  <h4>Exit & Safety Devices</h4>
                  <div className="hardware-grid">
                    {['panic', 'auto_operator'].map(h => (
                      <label key={h} className="checkbox hardware-item">
                        <input type="checkbox" checked={!!hardware[h]} onChange={() => toggleHardware(h)} />
                        <span className="hardware-name">{formatHardwareName(h)}</span>
                      </label>
                    ))}
                  </div>
                </div>
                
                <div className="hardware-category">
                  <h4>Key Control</h4>
                  <div className="hardware-grid">
                    {['ic_core'].map(h => (
                      <label key={h} className="checkbox hardware-item">
                        <input type="checkbox" checked={!!hardware[h]} onChange={() => toggleHardware(h)} />
                        <span className="hardware-name">{formatHardwareName(h)}</span>
                      </label>
                    ))}
                  </div>
                </div>
                
                <div className="hint">Select hardware to include in your quote. Prices from SecLock distributor catalog.</div>
              </div>
            )}
          </section>

          {/* Finishing */}
          <section className="form-section">
            <SectionHeader id="finishing" title="Finishing" icon="🎨" />
            {expandedSections.finishing && (
              <div className="section-content">
                <div className="row-grid">
                  <div className="field">
                    <label>Finish</label>
                    <select value={finish} onChange={e => setFinish(e.target.value)}>
                      <option value="unfinished">Unfinished</option>
                      <option value="primed">Primed</option>
                      <option value="painted">Painted</option>
                      <option value="stained">Stained</option>
                      <option value="pre-finished">Pre-Finished</option>
                    </select>
                  </div>
                  {finish !== 'unfinished' && finish !== 'primed' && (
                    <div className="field">
                      <label>Color / Stain</label>
                      <input type="text" value={finishColor} onChange={e => setFinishColor(e.target.value)} placeholder="e.g., White, Espresso" />
                    </div>
                  )}
                </div>
              </div>
            )}
          </section>
        </div>
      )}

      {/* Upload Result */}
      {uploadResult && uploadResult.success && (
        <div className="upload-result success">
          <div className="result-header">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <polyline points="22 4 12 14.01 9 11.01"/>
            </svg>
            <span>Measurements Extracted</span>
            <span className={`confidence ${uploadResult.confidence}`}>{uploadResult.confidence} confidence</span>
          </div>
          {uploadResult.measurements.notes && (
            <p className="result-notes">{uploadResult.measurements.notes}</p>
          )}
          {uploadResult.raw_text && (
            <details className="raw-text">
              <summary>View extracted text</summary>
              <pre>{uploadResult.raw_text}</pre>
            </details>
          )}
        </div>
      )}

      <div className="estimate">
        {loading ? (<div className="muted">Processing specifications...</div>) : error ? (<div className="error">{error}</div>) : null}
      </div>

      {/* Action Buttons */}
      <div className="action-buttons">
        <div className="recommendations-cta">
          <button 
            className="recommendations-btn"
            onClick={fetchRecommendations}
            disabled={loadingRecs}
          >
            {loadingRecs ? (
              <>
                <div className="spinner-small"></div>
                Finding Products...
              </>
            ) : (
              <>
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="11" cy="11" r="8"/>
                  <path d="m21 21-4.35-4.35"/>
                </svg>
                Find Recommended Products
              </>
            )}
          </button>
          <span className="recommendations-hint">Get matching hardware from top distributors</span>
        </div>

        {estimate != null && (
          <div className="quote-cta">
            <button 
              className="quote-btn"
              onClick={downloadQuote}
              disabled={generatingPdf}
            >
              {generatingPdf ? (
                <>
                  <div className="spinner-small"></div>
                  Generating PDF...
                </>
              ) : (
                <>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                    <line x1="12" y1="18" x2="12" y2="12"/>
                    <polyline points="9 15 12 18 15 15"/>
                  </svg>
                  Generate Internal Quote
                </>
              )}
            </button>
            <span className="quote-hint">Creates PDF and saves project to CRM</span>
          </div>
        )}
      </div>

      {/* Product Recommendations */}
      {showRecommendations && recommendations && (
        <div className="recommendations-section">
          <h2>🛒 Recommended Products</h2>
          <p className="recommendations-count">
            Found {recommendations.total_recommendations} products from {recommendations.distributors.length} distributor(s)
          </p>
          
          {recommendations.distributors.map(distributor => (
            <div key={distributor.id} className="distributor-block">
              <div className="distributor-header">
                <h3>{distributor.name}</h3>
                <a href={distributor.website} target="_blank" rel="noopener noreferrer" className="distributor-link">
                  Visit Website →
                </a>
              </div>
              
              <div className="products-grid">
                {distributor.recommendations.map((product, idx) => (
                  <div key={idx} className="product-card">
                    <div className="product-category">{product.category}</div>
                    <h4 className="product-name">{product.name}</h4>
                    <p className="product-description">{product.description}</p>
                    
                    {product.model_numbers && product.model_numbers.length > 0 && (
                      <div className="product-models">
                        <span className="label">Models:</span> {product.model_numbers.join(', ')}
                      </div>
                    )}
                    
                    {product.features && product.features.length > 0 && (
                      <ul className="product-features">
                        {product.features.slice(0, 3).map((feature, i) => (
                          <li key={i}>{feature}</li>
                        ))}
                      </ul>
                    )}
                    
                    <div className="product-footer">
                      {product.price_range && (
                        <span className="product-price">{product.price_range}</span>
                      )}
                      <a href={product.url} target="_blank" rel="noopener noreferrer" className="product-link">
                        View Details
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
