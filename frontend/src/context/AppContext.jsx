import { createContext, useContext, useState } from 'react'

const AppContext = createContext({})

export function AppProvider({ children }) {
  const [currentLessonId, setCurrentLessonId] = useState(
    () => localStorage.getItem('current_lesson_id') || null
  )

  function saveCurrentLesson(id) {
    if (id) {
      localStorage.setItem('current_lesson_id', id)
      setCurrentLessonId(id)
    }
  }

  return (
    <AppContext.Provider value={{ currentLessonId, saveCurrentLesson }}>
      {children}
    </AppContext.Provider>
  )
}

export const useApp = () => useContext(AppContext)
