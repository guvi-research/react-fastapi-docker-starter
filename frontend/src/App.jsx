import { useEffect, useState } from 'react'

export default function App() {
  const [health, setHealth] = useState(null)
  const [healthError, setHealthError] = useState('')
  const [job, setJob] = useState(null)
  const [jobError, setJobError] = useState('')
  const [pending, setPending] = useState(false)

  async function loadHealth() {
    try {
      const response = await fetch('/api/health')
      const body = await response.json()
      if (!response.ok) {
        const detail = body.detail?.detail || body.detail || response.statusText
        throw new Error(typeof detail === 'string' ? detail : 'Health check failed')
      }
      setHealth(body)
      setHealthError('')
    } catch (error) {
      setHealth(null)
      setHealthError(error.message)
    }
  }

  useEffect(() => {
    loadHealth()
  }, [])

  async function enqueueJob() {
    setPending(true)
    setJobError('')
    try {
      const response = await fetch('/api/jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: 'hello from the template' }),
      })
      const body = await response.json()
      if (!response.ok) {
        const detail = body.detail || response.statusText
        throw new Error(typeof detail === 'string' ? detail : 'Could not enqueue job')
      }
      setJob(body)
    } catch (error) {
      setJob(null)
      setJobError(error.message)
    } finally {
      setPending(false)
    }
  }

  return (
    <main>
      <p className="eyebrow">React · FastAPI · MongoDB · Redis · RQ</p>
      <h1>Quick project setup</h1>
      <p className="lede">
        This page calls the API through <code>/api</code>. Development proxies that
        path to FastAPI. Staging and production send it through nginx.
      </p>

      <section>
        <h2>API health</h2>
        {healthError ? <p className="error">{healthError}</p> : null}
        {health ? <pre>{JSON.stringify(health, null, 2)}</pre> : null}
        <button type="button" onClick={loadHealth}>
          Check again
        </button>
      </section>

      <section>
        <h2>Sample job</h2>
        <p>Enqueue a worker task that writes one document to MongoDB.</p>
        <button type="button" onClick={enqueueJob} disabled={pending}>
          {pending ? 'Queuing…' : 'Enqueue job'}
        </button>
        {jobError ? <p className="error">{jobError}</p> : null}
        {job ? (
          <p className="result">
            Job id <code>{job.job_id}</code> · {job.status}
          </p>
        ) : null}
      </section>
    </main>
  )
}
