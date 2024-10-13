import { Outlet } from 'react-router-dom'
import MainNavBar from './MainNavBar'

function AppLayout() {
  return (
    <div>
      <MainNavBar />

      <main className="mx-20">
        <Outlet />
      </main>
    </div>
  )
}

export default AppLayout
