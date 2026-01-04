import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Progress } from './ui/progress';
import { ArrowLeft, Mail, Phone, MapPin, Calendar, Award, TrendingUp, Clock } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';

interface StudentProfileProps {
  studentId: string | null;
  onBack: () => void;
}

export function StudentProfile({ studentId, onBack }: StudentProfileProps) {
  // Mock student data
  const student = {
    id: studentId || '1',
    name: 'Carlos Mendez',
    rank: 'Blue Belt',
    nextRank: 'Purple Belt',
    discipline: 'Karate',
    status: 'Active',
    email: 'carlos.mendez@email.com',
    phone: '555-0101',
    address: '123 Main St, City, State 12345',
    joinDate: '2023-06-15',
    birthDate: '1995-03-20',
    emergencyContact: 'Maria Mendez - 555-0199',
    payment: 'Current',
    monthlyFee: '$120',
    nextPayment: '2024-12-15',
    
    // Progress tracking
    currentRankMonths: 8,
    requiredMonths: 12,
    progressPercentage: 67,
    
    // Training history
    totalClasses: 156,
    attendanceRate: 92,
    lastClass: '2024-11-22',
    
    // Belt progression
    beltHistory: [
      { rank: 'White Belt', date: '2023-06-15', instructor: 'Master Lee' },
      { rank: 'Yellow Belt', date: '2023-10-10', instructor: 'Master Lee' },
      { rank: 'Orange Belt', date: '2024-02-15', instructor: 'Master Chen' },
      { rank: 'Green Belt', date: '2024-06-20', instructor: 'Master Chen' },
      { rank: 'Blue Belt', date: '2024-10-05', instructor: 'Master Lee' },
    ],
    
    // Payment history
    paymentHistory: [
      { date: '2024-11-15', amount: '$120', method: 'Credit Card', status: 'Paid' },
      { date: '2024-10-15', amount: '$120', method: 'Credit Card', status: 'Paid' },
      { date: '2024-09-15', amount: '$120', method: 'Cash', status: 'Paid' },
      { date: '2024-08-15', amount: '$120', method: 'Credit Card', status: 'Paid' },
    ],
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Button variant="outline" size="icon" onClick={onBack}>
            <ArrowLeft className="w-4 h-4" />
          </Button>
          <div>
            <h1 className="text-gray-900 mb-1">Student Profile</h1>
            <p className="text-gray-600">Detailed information and progress tracking</p>
          </div>
        </div>
        <div className="flex gap-3">
          <Button variant="outline">Edit Profile</Button>
          <Button className="bg-blue-950 hover:bg-blue-900">Send Message</Button>
        </div>
      </div>

      {/* Profile Header Card */}
      <Card>
        <CardContent className="p-6">
          <div className="flex flex-col md:flex-row gap-6">
            <div className="w-32 h-32 bg-gradient-to-br from-blue-950 to-blue-700 rounded-full flex items-center justify-center text-white flex-shrink-0">
              <span className="text-5xl">{student.name.split(' ').map(n => n[0]).join('')}</span>
            </div>
            
            <div className="flex-1 space-y-4">
              <div>
                <h2 className="text-gray-900 mb-1">{student.name}</h2>
                <div className="flex flex-wrap gap-2">
                  <Badge className="bg-blue-950 hover:bg-blue-950">{student.rank}</Badge>
                  <Badge className="bg-amber-500 hover:bg-amber-500">{student.discipline}</Badge>
                  <Badge className="bg-green-100 text-green-800 hover:bg-green-100">{student.status}</Badge>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex items-center gap-2 text-gray-600">
                  <Mail className="w-4 h-4" />
                  <span>{student.email}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-600">
                  <Phone className="w-4 h-4" />
                  <span>{student.phone}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-600">
                  <MapPin className="w-4 h-4" />
                  <span>{student.address}</span>
                </div>
                <div className="flex items-center gap-2 text-gray-600">
                  <Calendar className="w-4 h-4" />
                  <span>Joined: {student.joinDate}</span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Progress Tracker */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            Rank Progress Tracker
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-600 mb-1">Current Rank</p>
              <p className="text-gray-900">{student.rank}</p>
            </div>
            <div className="text-center">
              <p className="text-gray-600 mb-1">Time in Current Rank</p>
              <p className="text-gray-900">{student.currentRankMonths} months</p>
            </div>
            <div className="text-right">
              <p className="text-gray-600 mb-1">Next Rank</p>
              <p className="text-gray-900">{student.nextRank}</p>
            </div>
          </div>
          
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span className="text-gray-600">Progress to {student.nextRank}</span>
              <span className="text-gray-900">{student.currentRankMonths} / {student.requiredMonths} months</span>
            </div>
            <Progress value={student.progressPercentage} className="h-3" />
            <p className="text-gray-600 text-sm">
              {student.requiredMonths - student.currentRankMonths} months remaining to be eligible for promotion
            </p>
          </div>

          <div className="grid grid-cols-3 gap-4 pt-4 border-t">
            <div className="text-center">
              <div className="flex items-center justify-center gap-2 text-blue-950 mb-1">
                <Clock className="w-4 h-4" />
                <span className="text-gray-900">{student.totalClasses}</span>
              </div>
              <p className="text-gray-600 text-sm">Total Classes</p>
            </div>
            <div className="text-center">
              <div className="flex items-center justify-center gap-2 text-green-600 mb-1">
                <Award className="w-4 h-4" />
                <span className="text-gray-900">{student.attendanceRate}%</span>
              </div>
              <p className="text-gray-600 text-sm">Attendance Rate</p>
            </div>
            <div className="text-center">
              <div className="flex items-center justify-center gap-2 text-amber-500 mb-1">
                <Calendar className="w-4 h-4" />
                <span className="text-gray-900 text-sm">{student.lastClass}</span>
              </div>
              <p className="text-gray-600 text-sm">Last Class</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Tabs for History */}
      <Tabs defaultValue="belt-progression" className="space-y-4">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="belt-progression">Belt Progression</TabsTrigger>
          <TabsTrigger value="payment-history">Payment History</TabsTrigger>
        </TabsList>
        
        <TabsContent value="belt-progression">
          <Card>
            <CardHeader>
              <CardTitle>Belt Progression Timeline</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {student.beltHistory.map((belt, index) => (
                  <div key={index} className="flex items-start gap-4 relative">
                    {index !== student.beltHistory.length - 1 && (
                      <div className="absolute left-4 top-10 w-0.5 h-full bg-gray-200" />
                    )}
                    <div className="w-8 h-8 bg-blue-950 rounded-full flex items-center justify-center text-white flex-shrink-0 relative z-10">
                      <Award className="w-4 h-4" />
                    </div>
                    <div className="flex-1 bg-gray-50 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-gray-900">{belt.rank}</h3>
                        <Badge variant="outline">{belt.date}</Badge>
                      </div>
                      <p className="text-gray-600 text-sm">Awarded by: {belt.instructor}</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        
        <TabsContent value="payment-history">
          <Card>
            <CardHeader>
              <CardTitle>Payment History</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {student.paymentHistory.map((payment, index) => (
                  <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                        <span className="text-green-600">$</span>
                      </div>
                      <div>
                        <p className="text-gray-900">{payment.amount}</p>
                        <p className="text-gray-600 text-sm">{payment.method}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <Badge className="bg-green-100 text-green-800 hover:bg-green-100 mb-1">
                        {payment.status}
                      </Badge>
                      <p className="text-gray-600 text-sm">{payment.date}</p>
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
