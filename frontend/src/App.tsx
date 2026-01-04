import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { Login } from './components/Login';
import { Dashboard } from './components/Dashboard';
import { StudentList } from './components/StudentList';
import { StudentProfile } from './components/StudentProfile';
import { Financial } from './components/Financial';
import { CalendarView } from './components/CalendarView';

export type Screen = 'login' | 'dashboard' | 'students' | 'profile' | 'financial' | 'calendar';

export default function App() {
  const [currentScreen, setCurrentScreen] = useState<Screen>('login');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [selectedStudentId, setSelectedStudentId] = useState<string | null>(null);

  const handleLogin = () => {
    setIsAuthenticated(true);
    setCurrentScreen('dashboard');
  };

  const handleNavigate = (screen: Screen) => {
    setCurrentScreen(screen);
  };

  const handleViewStudent = (studentId: string) => {
    setSelectedStudentId(studentId);
    setCurrentScreen('profile');
  };

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar currentScreen={currentScreen} onNavigate={handleNavigate} />
      
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        
        <main className="flex-1 overflow-y-auto p-8">
          {currentScreen === 'dashboard' && <Dashboard onNavigate={handleNavigate} />}
          {currentScreen === 'students' && <StudentList onViewStudent={handleViewStudent} />}
          {currentScreen === 'profile' && <StudentProfile studentId={selectedStudentId} onBack={() => setCurrentScreen('students')} />}
          {currentScreen === 'financial' && <Financial />}
          {currentScreen === 'calendar' && <CalendarView />}
        </main>
      </div>
    </div>
  );
}
