import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { Toaster } from 'react-hot-toast'

import AppLayout from 'components/AppLayout'
import Login from 'pages/Login'
import Surveys from 'pages/Surveys'
import ProtectedRoute from 'components/ProtectedRoute'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ReactQueryDevtools initialIsOpen={false} />
      <BrowserRouter>
        <Routes>
          <Route
            element={
              <ProtectedRoute>
                <AppLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate replace to="surveys" />} />
            <Route path="surveys" element={<Surveys />} />
          </Route>

          <Route path="login" element={<Login />} />
          <Route path="*" element={<div>ooops, not found :/</div>} />
        </Routes>
      </BrowserRouter>

      <Toaster />
    </QueryClientProvider>
  )
}

export default App
