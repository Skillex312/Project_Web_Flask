import { useState, useEffect } from 'react';
import { useAuth } from '../controllers/useAuth';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Card } from './ui/card';
import { Alert, AlertDescription } from './ui/alert';
import { Shield, AlertCircle, Loader2, CheckCircle } from 'lucide-react';
import { checkApiHealth } from '../services/api';

interface LoginProps {
  onLogin: () => void;
}

export function Login({ onLogin }: LoginProps) {
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const { login, loading, error } = useAuth(onLogin);

  /**
   * Verificar estado del backend al montar el componente
   */
  useEffect(() => {
    const checkBackend = async () => {
      const isOnline = await checkApiHealth();
      setBackendStatus(isOnline ? 'online' : 'offline');
    };
    
    checkBackend();
    
    // Verificar cada 30 segundos
    const interval = setInterval(checkBackend, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (backendStatus !== 'online') {
      return;
    }
    login(credentials);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-950 via-blue-900 to-blue-800 p-4">
      <Card className="w-full max-w-md p-8 shadow-2xl">
        <div className="flex flex-col items-center mb-8">
          <div className="w-20 h-20 bg-gradient-to-br from-blue-950 to-red-600 rounded-full flex items-center justify-center mb-4">
            <Shield className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-blue-950 mb-2">Martial House</h1>
          <p className="text-muted-foreground text-center">
            Sistema de Gestión de Academia
          </p>
        </div>

        {/* Estado del backend */}
        <div className="mb-4">
          {backendStatus === 'checking' && (
            <Alert className="bg-blue-50 border-blue-200">
              <Loader2 className="h-4 w-4 animate-spin text-blue-600" />
              <AlertDescription className="text-blue-700">
                Verificando conexión con el servidor...
              </AlertDescription>
            </Alert>
          )}
          
          {backendStatus === 'online' && (
            <Alert className="bg-green-50 border-green-200">
              <CheckCircle className="h-4 w-4 text-green-600" />
              <AlertDescription className="text-green-700">
                Conectado al servidor
              </AlertDescription>
            </Alert>
          )}
          
          {backendStatus === 'offline' && (
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                No se puede conectar al servidor. Verifica que el backend esté ejecutándose.
              </AlertDescription>
            </Alert>
          )}
        </div>

        {/* Mensaje de error */}
        {error && (
          <Alert variant="destructive" className="mb-4">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <Label htmlFor="username" className="text-gray-700">
              ID de Usuario
            </Label>
            <Input
              id="username"
              type="text"
              placeholder="Ingrese su ID de usuario"
              value={credentials.username}
              onChange={(e) =>
                setCredentials({ ...credentials, username: e.target.value })
              }
              required
              disabled={loading || backendStatus !== 'online'}
              className="border-gray-300 focus:border-blue-950"
            />
            <p className="text-xs text-gray-500">
              Ejemplo: EST001, INS001, ADM001, DBA001
            </p>
          </div>

          <div className="space-y-2">
            <Label htmlFor="password" className="text-gray-700">
              Contraseña
            </Label>
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              value={credentials.password}
              onChange={(e) =>
                setCredentials({ ...credentials, password: e.target.value })
              }
              required
              disabled={loading || backendStatus !== 'online'}
              className="border-gray-300 focus:border-blue-950"
            />
          </div>

          <Button
            type="submit"
            className="w-full bg-blue-950 hover:bg-blue-900 transition-colors"
            disabled={loading || backendStatus !== 'online'}
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Iniciando sesión...
              </>
            ) : (
              'Iniciar Sesión'
            )}
          </Button>

          <div className="text-center text-sm text-gray-600">
            <p>¿Olvidaste tu contraseña?</p>
            <a href="#" className="text-blue-950 hover:underline font-medium">
              Contacta al administrador
            </a>
          </div>
        </form>

        {/* Información de desarrollo */}
        {import.meta.env.DEV && (
          <div className="mt-6 p-4 bg-gray-100 rounded-lg text-xs">
            <p className="font-semibold text-gray-700 mb-2">🔧 Modo Desarrollo</p>
            <p className="text-gray-600">
              Backend: {import.meta.env.VITE_API_URL || 'http://localhost:5000/api'}
            </p>
            <p className="text-gray-600">
              Estado: {backendStatus}
            </p>
          </div>
        )}
      </Card>
    </div>
  );
}
