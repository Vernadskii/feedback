import axios from 'axios'
import { decodeToken } from 'features/authentication/jwtToken'
import {
  setLocalStorageItem,
  getLocalStorageItem,
} from 'features/authentication/localStorage'

export async function login({ email, password }) {
  try {
    const { data } = await axios.post('/api/users/login', { email, password })
    const { token } = data
    setLocalStorageItem('token', token)

    const user = decodeToken(token)
    return user
  } catch (error) {
    throw new Error(error.message)
  }
}

export async function getCurrentUser() {
  const token = getLocalStorageItem('token')
  if (!token) return null

  const { id: userId } = decodeToken(token)

  try {
    const { data } = await axios.get(`/api/users/${userId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
    return data
  } catch (error) {
    throw new Error(error.message)
  }
}
