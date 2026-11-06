import { useRef, useState } from 'react'
import Editor, { loader } from '@monaco-editor/react'

// Monaco CDN থেকে লোড করো (vite bundle করবে না)
loader.config({
  paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.52.2/min/vs' },
})

const LANG_MAP = { html: 'html', css: 'css', js: 'javascript' }

export default function CodeEditor({ value, onChange, lang = 'html', height = '380px' }) {
  const [tab, setTab] = useState(lang)
  const editorRef = useRef(null)

  function handleMount(editor, monaco) {
    editorRef.current = editor

    // HTML IntelliSense চালু করো
    monaco.languages.html.htmlDefaults.setOptions({
      suggest: { html5: true },
      format: { tabSize: 2, insertSpaces: true },
    })

    // CSS IntelliSense
    monaco.languages.css.cssDefaults.setOptions({ validate: true })

    // Auto-suggest trigger characters
    editor.updateOptions({
      suggestOnTriggerCharacters: true,
      quickSuggestions: {
        other: true,
        comments: false,
        strings: true,
      },
      wordBasedSuggestions: 'currentDocument',
      acceptSuggestionOnEnter: 'on',
      tabCompletion: 'on',
    })

    // মোবাইলে touch-এ suggest খোলো
    editor.onDidChangeModelContent(() => {
      const model = editor.getModel()
      if (!model) return
      const pos = editor.getPosition()
      const word = model.getWordUntilPosition(pos)
      if (word.word.length >= 1) {
        editor.trigger('keyboard', 'editor.action.triggerSuggest', {})
      }
    })

    // Focus করলে cursor শেষে যাও
    editor.focus()
  }

  return (
    <div>
      {/* Language tab switcher */}
      <div style={{ display: 'flex', gap: 6, marginBottom: 8, alignItems: 'center' }}>
        {['html', 'css', 'js'].map(l => (
          <button
            key={l}
            type="button"
            onClick={() => setTab(l)}
            style={{
              padding: '4px 14px',
              borderRadius: 6,
              border: 'none',
              cursor: 'pointer',
              fontSize: '0.82rem',
              fontWeight: 700,
              background: tab === l ? 'var(--primary)' : 'var(--surface-2, #f1f5f9)',
              color: tab === l ? '#fff' : 'var(--text-muted)',
              transition: 'background 0.15s',
            }}
          >
            {l.toUpperCase()}
          </button>
        ))}
        <span style={{ marginLeft: 'auto', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
          VS Code engine · tag লিখলেই সাজেস্ট আসবে
        </span>
      </div>

      {/* Monaco Editor */}
      <div style={{ borderRadius: 10, overflow: 'hidden', border: '1px solid var(--border)' }}>
        <Editor
          height={height}
          language={LANG_MAP[tab]}
          value={value}
          theme="vs-dark"
          onMount={handleMount}
          onChange={val => onChange(val ?? '')}
          loading={
            <div style={{
              height,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              background: '#1e1e1e',
              color: '#ccc',
              fontSize: '0.9rem',
            }}>
              Editor লোড হচ্ছে…
            </div>
          }
          options={{
            fontSize: 15,
            fontFamily: "'Fira Code', 'Cascadia Code', Consolas, monospace",
            fontLigatures: true,
            lineNumbers: 'on',
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            wordWrap: 'on',
            automaticLayout: true,
            tabSize: 2,
            insertSpaces: true,
            formatOnPaste: true,
            formatOnType: true,
            autoClosingBrackets: 'always',
            autoClosingTags: true,
            autoIndent: 'full',
            suggestFontSize: 14,
            suggestLineHeight: 24,
            parameterHints: { enabled: true },
            hover: { enabled: true },
            // মোবাইলের জন্য
            padding: { top: 12, bottom: 12 },
            smoothScrolling: true,
            cursorBlinking: 'smooth',
            cursorSmoothCaretAnimation: 'on',
            renderLineHighlight: 'line',
            // Suggest popup বড় রাখো
            suggest: {
              showClasses: true,
              showColors: true,
              showConstants: true,
              showConstructors: true,
              showEnums: true,
              showFields: true,
              showFiles: true,
              showFunctions: true,
              showInterfaces: true,
              showKeywords: true,
              showMethods: true,
              showModules: true,
              showOperators: true,
              showProperties: true,
              showReferences: true,
              showSnippets: true,
              showStructs: true,
              showTypeParameters: true,
              showUnits: true,
              showValues: true,
              showVariables: true,
              showWords: true,
              insertMode: 'replace',
              filterGraceful: true,
              snippetsPreventQuickSuggestions: false,
            },
          }}
        />
      </div>
    </div>
  )
}
