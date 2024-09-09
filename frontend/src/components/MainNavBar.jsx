/* eslint-disable react/button-has-type */
/* eslint-disable jsx-a11y/anchor-is-valid */

import Button from './Button'

function MainNavBar() {
  return (
    <nav className="mx-20 mb-6 flex items-center justify-between">
      <div className="flex items-center justify-between gap-4 py-4">
        <a href="#" className="text-base font-semibold">
          Опросы
        </a>
        <a href="#" className="text-base font-semibold">
          Пользователи
        </a>
        <a href="#" className="text-base font-semibold">
          Черные списки
        </a>
      </div>
      <div>
        <Button variant="blueSecondary">Даниил Ковалев</Button>
      </div>
    </nav>
  )
}

export default MainNavBar
