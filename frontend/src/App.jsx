/* eslint-disable import/no-extraneous-dependencies */
import { Navigate, Route, Routes } from 'react-router-dom'
import AppLayout from 'components/AppLayout'
import Login from 'pages/Login'
import Surveys from 'pages/Surveys'

function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<Navigate replace to="surveys" />} />
        <Route path="surveys" element={<Surveys />} />
      </Route>

      <Route path="login" element={<Login />} />
      <Route path="*" element={<div>ooops, not found :/</div>} />
    </Routes>
  )
}

export default App
