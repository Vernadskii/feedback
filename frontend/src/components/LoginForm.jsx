/* eslint-disable jsx-a11y/label-has-associated-control */
/* eslint-disable react/button-has-type */

import Button from './Button'

function LoginForm() {
  return (
    <form className="m-auto mt-[210px] grid max-w-[320px] gap-3 rounded-lg border p-6">
      <div className="grid gap-2">
        <label htmlFor="email" className="text-base font-medium">
          Электронная почта
        </label>
        <input
          required
          type="email"
          id="email"
          placeholder="example@mail.ru"
          className="rounded-sm border px-4 py-2.5 text-base font-medium"
        />
      </div>
      <div className="grid gap-2">
        <label htmlFor="password" className="text-base font-medium">
          Пароль
        </label>
        <input
          required
          type="password"
          id="password"
          placeholder="Введите пароль"
          className="mb-1 rounded-sm border px-4 py-2.5 text-base font-medium"
        />
      </div>
      <Button variant="bluePrimary" fullWidth>
        Войти
      </Button>
    </form>
  )
}

export default LoginForm
