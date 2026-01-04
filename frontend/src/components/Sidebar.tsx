import { LayoutDashboard, Users, DollarSign, Calendar, Shield } from 'lucide-react';
import type { Screen } from '../App';

interface SidebarProps {
  currentScreen: Screen;
  onNavigate: (screen: Screen) => void;
}

export function Sidebar({ currentScreen, onNavigate }: SidebarProps) {
  const navItems = [
    { id: 'dashboard' as Screen, label: 'Dashboard', icon: LayoutDashboard },
    { id: 'students' as Screen, label: 'Students', icon: Users },
    { id: 'financial' as Screen, label: 'Financial', icon: DollarSign },
    { id: 'calendar' as Screen, label: 'Calendar', icon: Calendar },
  ];

  return (
    <aside className="w-64 bg-blue-950 text-white flex flex-col">
      <div className="p-6 border-b border-blue-900">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-red-600 to-amber-500 rounded-lg flex items-center justify-center">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="text-white">Martial House</h2>
            <p className="text-blue-300 text-sm">Academy System</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentScreen === item.id;
            
            return (
              <li key={item.id}>
                <button
                  onClick={() => onNavigate(item.id)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-red-600 text-white'
                      : 'text-blue-200 hover:bg-blue-900 hover:text-white'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </button>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="p-4 border-t border-blue-900">
        <div className="text-blue-400 text-sm text-center">
          © 2024 Martial House
        </div>
      </div>
    </aside>
  );
}
