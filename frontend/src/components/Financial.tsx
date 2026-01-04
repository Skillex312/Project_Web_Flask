import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from './ui/table';
import { DollarSign, TrendingUp, AlertCircle, Clock, Download, Plus } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export function Financial() {
  const stats = [
    {
      title: 'Total Revenue (Month)',
      value: '$24,580',
      change: '+8.2% from last month',
      icon: DollarSign,
      color: 'bg-green-600',
    },
    {
      title: 'Outstanding Payments',
      value: '$2,160',
      change: '18 students overdue',
      icon: AlertCircle,
      color: 'bg-red-600',
    },
    {
      title: 'Instructor Salaries',
      value: '$8,400',
      change: '7 instructors',
      icon: Clock,
      color: 'bg-blue-950',
    },
    {
      title: 'Net Profit',
      value: '$16,180',
      change: '+12.4% from last month',
      icon: TrendingUp,
      color: 'bg-amber-500',
    },
  ];

  const revenueData = [
    { month: 'Jun', revenue: 18500 },
    { month: 'Jul', revenue: 19800 },
    { month: 'Aug', revenue: 21200 },
    { month: 'Sep', revenue: 20100 },
    { month: 'Oct', revenue: 22700 },
    { month: 'Nov', revenue: 24580 },
  ];

  const instructors = [
    { id: 1, name: 'Master Lee', discipline: 'Karate', hoursLogged: 120, hourlyRate: 35, totalSalary: 4200, status: 'Paid' },
    { id: 2, name: 'Master Chen', discipline: 'Taekwondo', hoursLogged: 100, hourlyRate: 35, totalSalary: 3500, status: 'Paid' },
    { id: 3, name: 'Sensei Rodriguez', discipline: 'Judo', hoursLogged: 60, hourlyRate: 30, totalSalary: 1800, status: 'Pending' },
    { id: 4, name: 'Coach Martinez', discipline: 'BJJ', hoursLogged: 45, hourlyRate: 30, totalSalary: 1350, status: 'Pending' },
  ];

  const overduePayments = [
    { student: 'Miguel Torres', amount: '$120', daysOverdue: 15, phone: '555-0103', lastContact: '2024-11-20' },
    { student: 'Diego Lopez', amount: '$120', daysOverdue: 35, phone: '555-0105', lastContact: '2024-11-10' },
    { student: 'Maria Gonzalez', amount: '$120', daysOverdue: 10, phone: '555-0108', lastContact: '2024-11-22' },
    { student: 'Roberto Diaz', amount: '$150', daysOverdue: 22, phone: '555-0201', lastContact: '2024-11-15' },
    { student: 'Carmen Ruiz', amount: '$120', daysOverdue: 8, phone: '555-0202', lastContact: '2024-11-23' },
  ];

  const recentPayments = [
    { student: 'Ana Rodriguez', amount: '$120', date: '2024-11-23', method: 'Credit Card', status: 'Completed' },
    { student: 'Carlos Mendez', amount: '$120', date: '2024-11-22', method: 'Cash', status: 'Completed' },
    { student: 'Sofia Garcia', amount: '$120', date: '2024-11-21', method: 'Credit Card', status: 'Completed' },
    { student: 'Luis Hernandez', amount: '$150', date: '2024-11-20', method: 'Bank Transfer', status: 'Completed' },
    { student: 'Isabella Martinez', amount: '$120', date: '2024-11-19', method: 'Credit Card', status: 'Completed' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-gray-900 mb-1">Financial Management</h1>
          <p className="text-gray-600">Track revenue, payments, and instructor salaries</p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline">
            <Download className="w-4 h-4 mr-2" />
            Export Report
          </Button>
          <Button className="bg-blue-950 hover:bg-blue-900">
            <Plus className="w-4 h-4 mr-2" />
            Record Payment
          </Button>
        </div>
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
                    <p className="text-gray-600 text-sm">{stat.change}</p>
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

      {/* Revenue Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Revenue Trend (Last 6 Months)</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={revenueData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip formatter={(value) => `$${value}`} />
              <Line type="monotone" dataKey="revenue" stroke="#1e3a8a" strokeWidth={3} dot={{ fill: '#1e3a8a', r: 6 }} />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Tabs for different financial views */}
      <Tabs defaultValue="instructors" className="space-y-4">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="instructors">Instructor Salaries</TabsTrigger>
          <TabsTrigger value="overdue">Overdue Payments</TabsTrigger>
          <TabsTrigger value="recent">Recent Payments</TabsTrigger>
        </TabsList>

        <TabsContent value="instructors">
          <Card>
            <CardHeader>
              <CardTitle>Instructor Hours & Salary</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="border rounded-lg overflow-hidden">
                <Table>
                  <TableHeader>
                    <TableRow className="bg-gray-50">
                      <TableHead>Instructor</TableHead>
                      <TableHead>Discipline</TableHead>
                      <TableHead>Hours Logged</TableHead>
                      <TableHead>Hourly Rate</TableHead>
                      <TableHead>Total Salary</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {instructors.map((instructor) => (
                      <TableRow key={instructor.id} className="hover:bg-gray-50">
                        <TableCell>
                          <div className="flex items-center gap-3">
                            <div className="w-10 h-10 bg-gradient-to-br from-blue-950 to-red-600 rounded-full flex items-center justify-center text-white">
                              {instructor.name.split(' ').map(n => n[0]).join('')}
                            </div>
                            <span className="text-gray-900">{instructor.name}</span>
                          </div>
                        </TableCell>
                        <TableCell>
                          <span className="text-gray-600">{instructor.discipline}</span>
                        </TableCell>
                        <TableCell>
                          <span className="text-gray-900">{instructor.hoursLogged}h</span>
                        </TableCell>
                        <TableCell>
                          <span className="text-gray-900">${instructor.hourlyRate}/h</span>
                        </TableCell>
                        <TableCell>
                          <span className="text-gray-900">${instructor.totalSalary}</span>
                        </TableCell>
                        <TableCell>
                          <Badge className={instructor.status === 'Paid' ? 'bg-green-100 text-green-800 hover:bg-green-100' : 'bg-amber-100 text-amber-800 hover:bg-amber-100'}>
                            {instructor.status}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-right">
                          <Button variant="ghost" size="sm" className="text-blue-950 hover:text-blue-900">
                            View Details
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="overdue">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Overdue Payments ({overduePayments.length})</CardTitle>
                <Button variant="outline" size="sm">
                  Send All Reminders
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {overduePayments.map((payment, index) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-red-50 border border-red-200 rounded-lg">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-red-600 rounded-full flex items-center justify-center text-white">
                        <AlertCircle className="w-5 h-5" />
                      </div>
                      <div>
                        <p className="text-gray-900">{payment.student}</p>
                        <p className="text-gray-600 text-sm">{payment.phone} • Last contact: {payment.lastContact}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-4">
                      <div className="text-right">
                        <p className="text-gray-900">{payment.amount}</p>
                        <p className="text-red-600 text-sm">{payment.daysOverdue} days overdue</p>
                      </div>
                      <Button size="sm" variant="outline" className="border-red-600 text-red-600 hover:bg-red-600 hover:text-white">
                        Send Reminder
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="recent">
          <Card>
            <CardHeader>
              <CardTitle>Recent Payments</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {recentPayments.map((payment, index) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                        <DollarSign className="w-5 h-5 text-green-600" />
                      </div>
                      <div>
                        <p className="text-gray-900">{payment.student}</p>
                        <p className="text-gray-600 text-sm">{payment.method}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-gray-900 mb-1">{payment.amount}</p>
                      <div className="flex items-center gap-2">
                        <Badge className="bg-green-100 text-green-800 hover:bg-green-100">
                          {payment.status}
                        </Badge>
                        <span className="text-gray-600 text-sm">{payment.date}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
