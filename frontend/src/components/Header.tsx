import { Bell, Search } from 'lucide-react';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Input } from './ui/input';
import { Button } from './ui/button';
import { Badge } from './ui/badge';

export function Header() {
  return (
    <header className="bg-white border-b border-gray-200 px-8 py-4">
      <div className="flex items-center justify-between">
        <div className="flex-1 max-w-xl">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <Input
              type="search"
              placeholder="Search students, classes, or instructors..."
              className="pl-10"
            />
          </div>
        </div>

        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" className="relative">
            <Bell className="w-5 h-5" />
            <Badge className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-red-600 text-white p-0 flex items-center justify-center">
              3
            </Badge>
          </Button>

          <div className="flex items-center gap-3 pl-4 border-l border-gray-200">
            <div className="text-right">
              <p className="text-gray-900">Admin User</p>
              <p className="text-gray-500 text-sm">Master Instructor</p>
            </div>
            <Avatar>
              <AvatarImage src="https://api.dicebear.com/7.x/avataaars/svg?seed=admin" />
              <AvatarFallback>AU</AvatarFallback>
            </Avatar>
          </div>
        </div>
      </div>
    </header>
  );
}
