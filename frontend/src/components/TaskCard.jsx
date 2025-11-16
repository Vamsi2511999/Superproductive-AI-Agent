import React from 'react';
import { Calendar, Mail, MessageSquare, ListTodo } from 'lucide-react';
import { format } from 'date-fns';

const priorityColors = {
  critical: 'bg-red-100 text-red-800 border-red-300',
  high: 'bg-orange-100 text-orange-800 border-orange-300',
  medium: 'bg-yellow-100 text-yellow-800 border-yellow-300',
  low: 'bg-green-100 text-green-800 border-green-300',
};

const sourceIcons = {
  email: <Mail className="w-4 h-4" />,
  teams: <MessageSquare className="w-4 h-4" />,
  loop: <ListTodo className="w-4 h-4" />,
};

const sourceColors = {
  email: 'text-blue-600',
  teams: 'text-purple-600',
  loop: 'text-green-600',
};

export default function TaskCard({ task, onStatusChange }) {
  const handleStatusChange = (e) => {
    onStatusChange(task.id, e.target.value);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-5 border-l-4 border-primary-500 hover:shadow-lg transition-shadow">
      {/* Header */}
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-gray-800 mb-1">
            {task.title}
          </h3>
          <p className="text-sm text-gray-600">{task.description}</p>
        </div>
        <span
          className={`px-3 py-1 rounded-full text-xs font-semibold border ${
            priorityColors[task.priority]
          }`}
        >
          {task.priority.toUpperCase()}
        </span>
      </div>

      {/* Metadata */}
      <div className="flex flex-wrap gap-3 text-sm text-gray-600 mb-3">
        {/* Source */}
        <div className={`flex items-center gap-1 ${sourceColors[task.source_type]}`}>
          {sourceIcons[task.source_type]}
          <span className="capitalize">{task.source_type}</span>
        </div>

        {/* Due Date */}
        {task.due_date && (
          <div className="flex items-center gap-1">
            <Calendar className="w-4 h-4" />
            <span>
              {format(new Date(task.due_date), 'MMM dd, yyyy')}
            </span>
          </div>
        )}

        {/* Assigned To */}
        {task.assigned_to && (
          <div className="text-gray-700">
            <span className="font-medium">Assigned:</span> {task.assigned_to}
          </div>
        )}
      </div>

      {/* Status Selector */}
      <div className="mt-3 pt-3 border-t border-gray-200">
        <label className="text-xs text-gray-600 mb-1 block">Status:</label>
        <select
          value={task.status}
          onChange={handleStatusChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-primary-500"
        >
          <option value="pending">Pending</option>
          <option value="in-progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>
      </div>

      {/* Priority Reasoning (if available) */}
      {task.metadata?.priority_reasoning && (
        <div className="mt-3 p-2 bg-blue-50 rounded text-xs text-gray-700">
          <span className="font-semibold">AI Insight:</span>{' '}
          {task.metadata.priority_reasoning}
        </div>
      )}
    </div>
  );
}
