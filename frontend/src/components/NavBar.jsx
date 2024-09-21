/* eslint-disable jsx-a11y/anchor-is-valid */

import Button from './Button'

function NavBar() {
  return (
    <nav className="flex justify-between border-b-[1px] pb-[7px]">
      <div className="flex items-center gap-6 pt-3">
        <a href="#" className="text-base font-medium">
          Все<span className="ml-1">9</span>
        </a>
        <a href="#" className="text-base font-medium">
          Завершенные<span className="ml-1">9</span>
        </a>
        <a href="#" className="text-base font-medium">
          Активные<span className="ml-1">9</span>
        </a>
        <a href="#" className="text-base font-medium">
          Отложенные<span className="ml-1">9</span>
        </a>
        <a href="#" className="border-l-[1px] pl-6 text-base font-medium">
          Черновики<span className="ml-1">9</span>
        </a>
      </div>
      <div className="flex items-start">
        <Button variant="bluePrimary">Новый опрос</Button>
      </div>
    </nav>
  )
}

export default NavBar
