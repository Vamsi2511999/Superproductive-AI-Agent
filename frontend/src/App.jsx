import React, { useState, useEffect } from 'react';
import {
  RefreshCw,
  Sparkles,
  ListTodo,
  BarChart3,
  MessageSquare,
} from 'lucide-react';
import TaskCard from './components/TaskCard';
import TaskFilters from './components/TaskFilters';
import ChatInterface from './components/ChatInterface';
import InsightsPanel from './components/InsightsPanel';
import { taskService, insightsService } from './services/api';

function App() {
  const [tasks, setTasks] = useState([]);
  const [filteredTasks, setFilteredTasks] = useState([]);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('tasks'); // tasks, chat, insights
  const [extractionStatus, setExtractionStatus] = useState(null);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      const data = await taskService.getAllTasks();
      setTasks(data);
      setFilteredTasks(data);
    } catch (error) {
      console.error('Error loading tasks:', error);
    }
  };

  const handleExtractTasks = async () => {
    setLoading(true);
    setExtractionStatus('Extracting tasks from all sources...');
    try {
      const result = await taskService.extractTasks();
      setExtractionStatus(
        `Extracted ${result.total_tasks} tasks: ${result.by_source.email} from emails, ${result.by_source.teams} from Teams, ${result.by_source.loop} from Loop`
      );
      await loadTasks();
    } catch (error) {
      console.error('Error extracting tasks:', error);
      setExtractionStatus('Error extracting tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handlePrioritizeTasks = async () => {
    if (tasks.length === 0) {
      alert('Please extract tasks first!');
      return;
    }
    setLoading(true);
    setExtractionStatus('AI is prioritizing your tasks...');
    try {
      await taskService.prioritizeTasks();
      await loadTasks();
      setExtractionStatus('Tasks prioritized successfully!');
    } catch (error) {
      console.error('Error prioritizing tasks:', error);
      setExtractionStatus('Error prioritizing tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = async (filters) => {
    try {
      // Remove empty filters
      const activeFilters = Object.fromEntries(
        Object.entries(filters).filter(([_, v]) => v !== '')
      );

      if (Object.keys(activeFilters).length === 0) {
        setFilteredTasks(tasks);
        return;
      }

      const data = await taskService.filterTasks(activeFilters);
      setFilteredTasks(data);
    } catch (error) {
      console.error('Error filtering tasks:', error);
    }
  };

  const handleStatusChange = async (taskId, newStatus) => {
    try {
      await taskService.updateTaskStatus(taskId, newStatus);
      await loadTasks();
    } catch (error) {
      console.error('Error updating task status:', error);
    }
  };

  const loadInsights = async () => {
    try {
      const data = await insightsService.getInsights();
      setInsights(data);
    } catch (error) {
      console.error('Error loading insights:', error);
    }
  };

  useEffect(() => {
    if (activeTab === 'insights' && tasks.length > 0) {
      loadInsights();
    }
  }, [activeTab, tasks.length]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Sparkles className="w-8 h-8 text-primary-600" />
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  Superproductive AI Agent
                </h1>
                <p className="text-sm text-gray-600">
                  Unified Task Intelligence & Workflow Automation
                </p>
              </div>
            </div>
            <div className="flex gap-3">
              <button
                onClick={handleExtractTasks}
                disabled={loading}
                className="btn-primary flex items-center gap-2 disabled:opacity-50"
              >
                <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
                Extract Tasks
              </button>
              <button
                onClick={handlePrioritizeTasks}
                disabled={loading || tasks.length === 0}
                className="btn-secondary flex items-center gap-2 disabled:opacity-50"
              >
                <BarChart3 className="w-5 h-5" />
                Prioritize
              </button>
            </div>
          </div>
          {extractionStatus && (
            <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg text-sm text-blue-800">
              {extractionStatus}
            </div>
          )}
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex gap-8">
            <button
              onClick={() => setActiveTab('tasks')}
              className={`flex items-center gap-2 py-4 px-2 border-b-2 font-medium text-sm transition ${
                activeTab === 'tasks'
                  ? 'border-primary-600 text-primary-600'
                  : 'border-transparent text-gray-600 hover:text-gray-800 hover:border-gray-300'
              }`}
            >
              <ListTodo className="w-5 h-5" />
              Tasks ({filteredTasks.length})
            </button>
            <button
              onClick={() => setActiveTab('chat')}
              className={`flex items-center gap-2 py-4 px-2 border-b-2 font-medium text-sm transition ${
                activeTab === 'chat'
                  ? 'border-primary-600 text-primary-600'
                  : 'border-transparent text-gray-600 hover:text-gray-800 hover:border-gray-300'
              }`}
            >
              <MessageSquare className="w-5 h-5" />
              AI Chat
            </button>
            <button
              onClick={() => setActiveTab('insights')}
              className={`flex items-center gap-2 py-4 px-2 border-b-2 font-medium text-sm transition ${
                activeTab === 'insights'
                  ? 'border-primary-600 text-primary-600'
                  : 'border-transparent text-gray-600 hover:text-gray-800 hover:border-gray-300'
              }`}
            >
              <BarChart3 className="w-5 h-5" />
              Insights
            </button>
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'tasks' && (
          <>
            <TaskFilters onFilterChange={handleFilterChange} />

            {filteredTasks.length === 0 ? (
              <div className="text-center py-12">
                <ListTodo className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-700 mb-2">
                  No Tasks Found
                </h3>
                <p className="text-gray-600 mb-4">
                  {tasks.length === 0
                    ? 'Click "Extract Tasks" to start analyzing your data sources.'
                    : 'Try adjusting your filters to see more tasks.'}
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {filteredTasks.map((task) => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    onStatusChange={handleStatusChange}
                  />
                ))}
              </div>
            )}
          </>
        )}

        {activeTab === 'chat' && <ChatInterface />}

        {activeTab === 'insights' && <InsightsPanel insights={insights} />}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-600">
            Powered by AI • Integrating Outlook, Teams, and Microsoft Loop
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
