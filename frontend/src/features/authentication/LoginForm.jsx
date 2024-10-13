/* eslint-disable jsx-a11y/label-has-associated-control */
/* eslint-disable react/button-has-type */

import { useState } from 'react'
import Button from '../../components/Button'
import { useLogin } from './useLogin'

function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const { login, isLoading } = useLogin()

  function handleSubmit(e) {
    e.preventDefault()
    if (!email || !password) return

    login(
      { email, password },
      {
        onSettled: () => {
          setEmail('')
          setPassword('')
        },
      }
    )
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="m-auto mt-[210px] grid max-w-[320px] gap-3 rounded-lg border p-6"
    >
      <div className="grid gap-2">
        <label htmlFor="email" className="text-base font-medium">
          Электронная почта
        </label>
        <input
          required
          type="email"
          id="email"
          placeholder="example@mail.ru"
          value={email}
          onChange={e => setEmail(e.target.value)}
          disabled={isLoading}
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
          value={password}
          onChange={e => setPassword(e.target.value)}
          disabled={isLoading}
          className="mb-1 rounded-sm border px-4 py-2.5 text-base font-medium"
        />
      </div>
      <Button variant="bluePrimary" disabled={isLoading} fullWidth>
        Войти
      </Button>
    </form>
  )
}

export default LoginForm
