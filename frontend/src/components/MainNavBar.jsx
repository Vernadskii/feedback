/* eslint-disable react/button-has-type */

import { NavLink } from 'react-router-dom'
import Button from './Button'

function MainNavBar() {
  return (
    <nav className="mx-20 mb-6 flex items-center justify-between">
      <div className="flex items-center justify-between gap-4 py-4">
        <NavLink to="/surveys" className="text-base font-semibold">
          Опросы
        </NavLink>
        <NavLink to="/users" className="text-base font-semibold">
          Пользователи
        </NavLink>
        <NavLink to="/blacklist" className="text-base font-semibold">
          Черные списки
        </NavLink>
      </div>
      <div>
        <Button variant="blueSecondary">Даниил Ковалев</Button>
      </div>
    </nav>
  )
}

export default MainNavBar
