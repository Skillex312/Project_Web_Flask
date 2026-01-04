import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Users, DollarSign, Calendar, TrendingUp, AlertCircle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import type { Screen } from '../App';

interface DashboardProps {
  onNavigate: (screen: Screen) => void;
}

export function Dashboard({ onNavigate }: DashboardProps) {
  const stats = [
    {
      title: 'Total Active Students',
      value: '248',
      change: '+12 this month',
      icon: Users,
      color: 'bg-blue-950',
      trend: 'up'
    },
    {
      title: 'Payments Overdue',
      value: '18',
      change: 'Requires attention',
      icon: AlertCircle,
      color: 'bg-red-600',
      trend: 'warning'
    },
    {
      title: 'Upcoming Classes',
      value: '32',
      change: 'This week',
      icon: Calendar,
      color: 'bg-amber-500',
      trend: 'neutral'
    },
    {
      title: 'Monthly Revenue',
      value: '$24,580',
      change: '+8% from last month',
      icon: DollarSign,
      color: 'bg-green-600',
      trend: 'up'
    },
  ];

  const rankDistribution = [
    { rank: 'White Belt', students: 45 },
    { rank: 'Yellow Belt', students: 38 },
    { rank: 'Orange Belt', students: 32 },
    { rank: 'Green Belt', students: 28 },
    { rank: 'Blue Belt', students: 24 },
    { rank: 'Purple Belt', students: 18 },
    { rank: 'Brown Belt', students: 14 },
    { rank: 'Black Belt', students: 12 },
    { rank: 'Red Belt', students: 8 },
  ];

  const disciplineData = [
    { name: 'Karate', value: 98, color: '#1e3a8a' },
    { name: 'Taekwondo', value: 72, color: '#dc2626' },
    { name: 'Judo', value: 45, color: '#f59e0b' },
    { name: 'BJJ', value: 33, color: '#16a34a' },
  ];

  const recentActivities = [
    { student: 'Carlos Mendez', action: 'Promoted to Blue Belt', time: '2 hours ago', type: 'promotion' },
    { student: 'Ana Rodriguez', action: 'Payment received - $120', time: '4 hours ago', type: 'payment' },
    { student: 'Miguel Torres', action: 'Missed class - Karate Advanced', time: '1 day ago', type: 'absence' },
    { student: 'Sofia Garcia', action: 'New enrollment - Taekwondo', time: '2 days ago', type: 'enrollment' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-gray-900 mb-1">Dashboard Overview</h1>
          <p className="text-gray-600">Welcome back! Here's what's happening today.</p>
        </div>
        <Button className="bg-blue-950 hover:bg-blue-900">
          <TrendingUp className="w-4 h-4 mr-2" />
          Generate Report
        </Button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <Card key={stat.title} className="hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="text-gray-600 mb-2">{stat.title}</p>
                    <p className="text-gray-900 mb-1">{stat.value}</p>
                    <p className={`text-sm ${
                      stat.trend === 'up' ? 'text-green-600' : 
                      stat.trend === 'warning' ? 'text-red-600' : 
                      'text-gray-600'
                    }`}>
                      {stat.change}
                    </p>
                  </div>
                  <div className={`${stat.color} w-12 h-12 rounded-lg flex items-center justify-center`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Rank Distribution Chart */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Student Rank Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={rankDistribution}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="rank" angle={-45} textAnchor="end" height={100} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="students" fill="#1e3a8a" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Discipline Distribution */}
        <Card>
          <CardHeader>
            <CardTitle>Students by Discipline</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={disciplineData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {disciplineData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activities */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Activities</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recentActivities.map((activity, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                <div className="flex items-center gap-4">
                  <div className={`w-2 h-2 rounded-full ${
                    activity.type === 'promotion' ? 'bg-amber-500' :
                    activity.type === 'payment' ? 'bg-green-600' :
                    activity.type === 'absence' ? 'bg-red-600' :
                    'bg-blue-950'
                  }`} />
                  <div>
                    <p className="text-gray-900">{activity.student}</p>
                    <p className="text-gray-600">{activity.action}</p>
                  </div>
                </div>
                <div className="text-gray-500 text-sm">{activity.time}</div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
