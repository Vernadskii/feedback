import { useNavigate } from 'react-router-dom'
import { useEffect } from 'react'
import { useUser } from '../features/authentication/useUser'

function ProtectedRoute({ children }) {
  const navigate = useNavigate()

  const { user, isLoading } = useUser()

  useEffect(() => {
    if (!user && !isLoading) navigate('/login')
  }, [user, isLoading, navigate])

  if (user) return children
}

export default ProtectedRoute
