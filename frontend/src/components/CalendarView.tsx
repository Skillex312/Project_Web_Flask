import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { ChevronLeft, ChevronRight, Plus, Calendar as CalendarIcon } from 'lucide-react';

export function CalendarView() {
  const [currentWeek, setCurrentWeek] = useState(0);

  const weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  const timeSlots = [
    '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00',
    '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'
  ];

  const classes = [
    { day: 0, time: '06:00', duration: 1, title: 'Karate Basics', instructor: 'Master Lee', students: 15, level: 'Beginner', color: 'bg-blue-100 border-blue-500 text-blue-900' },
    { day: 0, time: '17:00', duration: 1.5, title: 'Taekwondo Advanced', instructor: 'Master Chen', students: 12, level: 'Advanced', color: 'bg-red-100 border-red-500 text-red-900' },
    { day: 0, time: '19:00', duration: 1, title: 'Judo Fundamentals', instructor: 'Sensei Rodriguez', students: 10, level: 'Intermediate', color: 'bg-amber-100 border-amber-500 text-amber-900' },
    
    { day: 1, time: '07:00', duration: 1, title: 'Morning Karate', instructor: 'Master Lee', students: 18, level: 'All Levels', color: 'bg-blue-100 border-blue-500 text-blue-900' },
    { day: 1, time: '16:00', duration: 1, title: 'Kids Taekwondo', instructor: 'Coach Martinez', students: 20, level: 'Kids', color: 'bg-purple-100 border-purple-500 text-purple-900' },
    { day: 1, time: '18:00', duration: 1.5, title: 'BJJ Training', instructor: 'Coach Martinez', students: 14, level: 'Intermediate', color: 'bg-green-100 border-green-500 text-green-900' },
    
    { day: 2, time: '06:00', duration: 1, title: 'Karate Basics', instructor: 'Master Lee', students: 15, level: 'Beginner', color: 'bg-blue-100 border-blue-500 text-blue-900' },
    { day: 2, time: '17:00', duration: 1.5, title: 'Taekwondo Advanced', instructor: 'Master Chen', students: 12, level: 'Advanced', color: 'bg-red-100 border-red-500 text-red-900' },
    { day: 2, time: '19:00', duration: 2, title: 'Tournament Prep', instructor: 'Master Lee', students: 8, level: 'Competition', color: 'bg-orange-100 border-orange-500 text-orange-900' },
    
    { day: 3, time: '07:00', duration: 1, title: 'Morning Karate', instructor: 'Master Lee', students: 18, level: 'All Levels', color: 'bg-blue-100 border-blue-500 text-blue-900' },
    { day: 3, time: '16:00', duration: 1, title: 'Kids Taekwondo', instructor: 'Coach Martinez', students: 20, level: 'Kids', color: 'bg-purple-100 border-purple-500 text-purple-900' },
    { day: 3, time: '18:00', duration: 1.5, title: 'BJJ Training', instructor: 'Coach Martinez', students: 14, level: 'Intermediate', color: 'bg-green-100 border-green-500 text-green-900' },
    
    { day: 4, time: '06:00', duration: 1, title: 'Karate Basics', instructor: 'Master Lee', students: 15, level: 'Beginner', color: 'bg-blue-100 border-blue-500 text-blue-900' },
    { day: 4, time: '17:00', duration: 1.5, title: 'Taekwondo Advanced', instructor: 'Master Chen', students: 12, level: 'Advanced', color: 'bg-red-100 border-red-500 text-red-900' },
    { day: 4, time: '19:00', duration: 1, title: 'Judo Fundamentals', instructor: 'Sensei Rodriguez', students: 10, level: 'Intermediate', color: 'bg-amber-100 border-amber-500 text-amber-900' },
    
    { day: 5, time: '09:00', duration: 2, title: 'Weekend Workshop', instructor: 'Master Lee & Master Chen', students: 25, level: 'All Levels', color: 'bg-indigo-100 border-indigo-500 text-indigo-900' },
    { day: 5, time: '14:00', duration: 3, title: 'Regional Tournament', instructor: 'All Instructors', students: 40, level: 'Competition', color: 'bg-rose-100 border-rose-500 text-rose-900' },
    
    { day: 6, time: '10:00', duration: 1.5, title: 'Sunday Open Mat', instructor: 'Open', students: 15, level: 'All Levels', color: 'bg-teal-100 border-teal-500 text-teal-900' },
  ];

  const getClassPosition = (timeStr: string) => {
    const hour = parseInt(timeStr.split(':')[0]);
    return (hour - 6) * 60;
  };

  const getClassHeight = (duration: number) => {
    return duration * 60;
  };

  const upcomingEvents = [
    { date: '2024-12-05', title: 'Belt Promotion Ceremony', type: 'Event', participants: 15 },
    { date: '2024-12-12', title: 'State Championship', type: 'Tournament', participants: 30 },
    { date: '2024-12-20', title: 'Year-End Celebration', type: 'Event', participants: 120 },
    { date: '2024-12-28', title: 'Winter Training Camp', type: 'Workshop', participants: 45 },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-gray-900 mb-1">Class Schedule</h1>
          <p className="text-gray-600">Weekly calendar of classes and special events</p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline">
            <CalendarIcon className="w-4 h-4 mr-2" />
            Export Schedule
          </Button>
          <Button className="bg-blue-950 hover:bg-blue-900">
            <Plus className="w-4 h-4 mr-2" />
            Add Class
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Calendar */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle>Week of November 25-31, 2024</CardTitle>
              <div className="flex gap-2">
                <Button variant="outline" size="icon" onClick={() => setCurrentWeek(currentWeek - 1)}>
                  <ChevronLeft className="w-4 h-4" />
                </Button>
                <Button variant="outline" size="sm">Today</Button>
                <Button variant="outline" size="icon" onClick={() => setCurrentWeek(currentWeek + 1)}>
                  <ChevronRight className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <div className="min-w-[800px]">
                {/* Week Header */}
                <div className="grid grid-cols-8 gap-2 mb-4">
                  <div className="text-center text-gray-600 text-sm"></div>
                  {weekDays.map((day, index) => (
                    <div key={day} className="text-center">
                      <p className="text-gray-900">{day}</p>
                      <p className="text-gray-600 text-sm">Nov {25 + index}</p>
                    </div>
                  ))}
                </div>

                {/* Calendar Grid */}
                <div className="relative">
                  <div className="grid grid-cols-8 gap-2">
                    {/* Time Column */}
                    <div className="space-y-[52px]">
                      {timeSlots.map((time) => (
                        <div key={time} className="text-gray-600 text-sm text-right pr-2 h-[60px]">
                          {time}
                        </div>
                      ))}
                    </div>

                    {/* Days */}
                    {weekDays.map((day, dayIndex) => (
                      <div key={day} className="relative border-l border-gray-200">
                        {/* Hour lines */}
                        <div className="absolute inset-0">
                          {timeSlots.map((time, index) => (
                            <div
                              key={time}
                              className="border-t border-gray-100 h-[60px]"
                              style={{ top: `${index * 60}px` }}
                            />
                          ))}
                        </div>

                        {/* Classes */}
                        {classes
                          .filter((c) => c.day === dayIndex)
                          .map((classItem, index) => (
                            <div
                              key={index}
                              className={`absolute left-1 right-1 rounded-lg p-2 border-l-4 ${classItem.color} shadow-sm hover:shadow-md transition-shadow cursor-pointer`}
                              style={{
                                top: `${getClassPosition(classItem.time)}px`,
                                height: `${getClassHeight(classItem.duration)}px`,
                              }}
                            >
                              <p className="text-xs mb-1">{classItem.title}</p>
                              <p className="text-xs opacity-80">{classItem.instructor}</p>
                              <p className="text-xs opacity-80">{classItem.students} students</p>
                            </div>
                          ))}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Upcoming Events Sidebar */}
        <Card>
          <CardHeader>
            <CardTitle>Upcoming Special Events</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {upcomingEvents.map((event, index) => (
                <div key={index} className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer">
                  <div className="flex items-start justify-between mb-2">
                    <Badge variant="outline" className="mb-2">
                      {event.type}
                    </Badge>
                    <span className="text-gray-600 text-sm">{event.date}</span>
                  </div>
                  <h3 className="text-gray-900 mb-1">{event.title}</h3>
                  <p className="text-gray-600 text-sm">{event.participants} participants</p>
                </div>
              ))}
            </div>

            <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h3 className="text-blue-950 mb-2">Legend</h3>
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-blue-100 border-l-4 border-blue-500 rounded"></div>
                  <span className="text-sm text-gray-600">Karate</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-red-100 border-l-4 border-red-500 rounded"></div>
                  <span className="text-sm text-gray-600">Taekwondo</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-amber-100 border-l-4 border-amber-500 rounded"></div>
                  <span className="text-sm text-gray-600">Judo</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-green-100 border-l-4 border-green-500 rounded"></div>
                  <span className="text-sm text-gray-600">BJJ</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-4 h-4 bg-purple-100 border-l-4 border-purple-500 rounded"></div>
                  <span className="text-sm text-gray-600">Kids Classes</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
