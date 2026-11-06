import CodeMirror from '@uiw/react-codemirror'
import { html } from '@codemirror/lang-html'
import { css } from '@codemirror/lang-css'
import { javascript } from '@codemirror/lang-javascript'
import { oneDark } from '@codemirror/theme-one-dark'
import { autocompletion } from '@codemirror/autocomplete'
import { useState } from 'react'

const LANG_MAP = {
  html: [html({ autoCloseTags: true }), css(), javascript()],
  css: [css()],
  js: [javascript({ jsx: false })],
}

export default function CodeEditor({ value, onChange, lang = 'html', height = '320px' }) {
  const [tab, setTab] = useState(lang)

  const extensions = [
    ...(LANG_MAP[tab] || LANG_MAP.html),
    autocompletion(),
  ]

  return (
    <div>
      {/* Language switcher */}
      <div style={{ display: 'flex', gap: 6, marginBottom: 8 }}>
        {['html', 'css', 'js'].map(l => (
          <button
            key={l}
            type="button"
            onClick={() => setTab(l)}
            style={{
              padding: '3px 12px',
              borderRadius: 6,
              border: 'none',
              cursor: 'pointer',
              fontSize: '0.8rem',
              fontWeight: 600,
              background: tab === l ? 'var(--primary)' : 'var(--surface-2)',
              color: tab === l ? '#fff' : 'var(--text-muted)',
            }}
          >
            {l.toUpperCase()}
          </button>
        ))}
        <span style={{ marginLeft: 'auto', fontSize: '0.75rem', color: 'var(--text-muted)', alignSelf: 'center' }}>
          Ctrl+Space = সাজেস্ট
        </span>
      </div>

      <CodeMirror
        value={value}
        height={height}
        extensions={extensions}
        theme={oneDark}
        onChange={val => onChange(val)}
        basicSetup={{
          lineNumbers: true,
          highlightActiveLine: true,
          bracketMatching: true,
          autocompletion: true,
          closeBrackets: true,
          indentOnInput: true,
          tabSize: 2,
        }}
        style={{
          borderRadius: 8,
          overflow: 'hidden',
          fontSize: '14px',
          border: '1px solid var(--border)',
        }}
      />
    </div>
  )
}
