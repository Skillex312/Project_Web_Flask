import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Input } from './ui/input';
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
import { Search, UserPlus, Download, Filter, Loader2 } from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from './ui/select';
import { studentService } from '../services/studentService';
import { Student } from '../models/Student';

interface StudentListProps {
  onViewStudent: (studentId: string) => void;
}

export function StudentList({ onViewStudent }: StudentListProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadStudents();
  }, []);

  const loadStudents = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await studentService.getAll();
      
      if (response.success && response.data) {
        setStudents(response.data.students);
      } else {
        setError('Error al cargar estudiantes');
      }
    } catch (err) {
      console.error('Error loading students:', err);
      setError('Error de conexión con el servidor');
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status: string) => {
    const variants: { [key: string]: { className: string } } = {
      'Activo': { className: 'bg-green-100 text-green-800 hover:bg-green-100' },
      'Inactivo': { className: 'bg-gray-100 text-gray-800 hover:bg-gray-100' },
      'Active': { className: 'bg-green-100 text-green-800 hover:bg-green-100' },
      'Inactive': { className: 'bg-gray-100 text-gray-800 hover:bg-gray-100' },
    };
    return variants[status] || variants['Activo'];
  };

  const filteredStudents = students.filter(student => {
    const matchesSearch = student.nombre.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         student.rango.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         student.disciplinas.some(d => d.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesFilter = filterStatus === 'all' || 
                         (filterStatus === 'active' && student.estado === 'Activo') ||
                         (filterStatus === 'inactive' && student.estado === 'Inactivo');
    return matchesSearch && matchesFilter;
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-blue-950" />
      </div>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent className="pt-6">
          <div className="text-center text-red-600">{error}</div>
          <Button onClick={loadStudents} className="mt-4 mx-auto block">
            Reintentar
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-gray-900 mb-1">Student Management</h1>
          <p className="text-gray-600">Manage and track all academy students</p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline">
            <Download className="w-4 h-4 mr-2" />
            Export
          </Button>
          <Button className="bg-blue-950 hover:bg-blue-900">
            <UserPlus className="w-4 h-4 mr-2" />
            Add Student
          </Button>
        </div>
      </div>

      <Card>
        <CardHeader>
          <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
            <CardTitle>All Students ({filteredStudents.length})</CardTitle>
            <div className="flex gap-3 w-full sm:w-auto">
              <div className="relative flex-1 sm:flex-initial">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                <Input
                  placeholder="Search students..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-9 w-full sm:w-64"
                />
              </div>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger className="w-32">
                  <Filter className="w-4 h-4 mr-2" />
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="active">Active</SelectItem>
                  <SelectItem value="inactive">Inactive</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="border rounded-lg overflow-hidden">
            <Table>
              <TableHeader>
                <TableRow className="bg-gray-50">
                  <TableHead>Name</TableHead>
                  <TableHead>Rank</TableHead>
                  <TableHead>Discipline</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Condition</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredStudents.map((student) => (
                  <TableRow key={student.id} className="hover:bg-gray-50">
                    <TableCell>
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-blue-950 to-blue-700 rounded-full flex items-center justify-center text-white text-sm font-medium">
                          {student.nombre.split(' ').map(n => n[0]).join('').toUpperCase()}
                        </div>
                        <div>
                          <p className="text-gray-900 font-medium">{student.nombre}</p>
                          <p className="text-gray-500 text-sm">ID: {student.id}</p>
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <span className="text-gray-900">{student.rango || 'Sin rango'}</span>
                    </TableCell>
                    <TableCell>
                      <div className="flex flex-wrap gap-1">
                        {student.disciplinas.length > 0 ? (
                          student.disciplinas.map((disciplina, idx) => (
                            <Badge key={idx} variant="outline" className="text-xs">
                              {disciplina}
                            </Badge>
                          ))
                        ) : (
                          <span className="text-gray-500 text-sm">Sin disciplina</span>
                        )}
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge {...getStatusBadge(student.estado)}>
                        {student.estado}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline" className="text-gray-700">
                        {student.condicion}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => onViewStudent(student.id)}
                        className="text-blue-950 hover:text-blue-900 hover:bg-blue-50"
                      >
                        View Profile
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
