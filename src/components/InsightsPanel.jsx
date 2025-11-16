import React from 'react';
import { TrendingUp, AlertCircle, CheckCircle, Clock } from 'lucide-react';

export default function InsightsPanel({ insights }) {
  if (!insights || insights.error) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Insights</h2>
        <p className="text-gray-600">
          {insights?.error || 'No insights available. Please extract tasks first.'}
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center gap-2 mb-6">
        <TrendingUp className="w-6 h-6 text-primary-600" />
        <h2 className="text-xl font-semibold text-gray-800">Task Insights</h2>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-blue-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-blue-600">
            {insights.total_tasks}
          </div>
          <div className="text-sm text-gray-600">Total Tasks</div>
        </div>
        
        <div className="bg-red-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-red-600">
            {insights.by_priority?.critical || 0}
          </div>
          <div className="text-sm text-gray-600">Critical</div>
        </div>
        
        <div className="bg-orange-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-orange-600">
            {insights.by_priority?.high || 0}
          </div>
          <div className="text-sm text-gray-600">High Priority</div>
        </div>
        
        <div className="bg-amber-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-amber-600">
            {insights.overdue_tasks || 0}
          </div>
          <div className="text-sm text-gray-600">Overdue</div>
        </div>
      </div>

      {/* Source Breakdown */}
      {insights.by_source && (
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">By Source</h3>
          <div className="grid grid-cols-3 gap-3">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
              <span className="text-sm text-gray-600">Email</span>
              <span className="font-semibold text-gray-800">
                {insights.by_source.email || 0}
              </span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
              <span className="text-sm text-gray-600">Teams</span>
              <span className="font-semibold text-gray-800">
                {insights.by_source.teams || 0}
              </span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
              <span className="text-sm text-gray-600">Loop</span>
              <span className="font-semibold text-gray-800">
                {insights.by_source.loop || 0}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Upcoming Deadlines */}
      {insights.upcoming_deadlines && insights.upcoming_deadlines.length > 0 && (
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
            <Clock className="w-4 h-4" />
            Upcoming Deadlines (Next 3 Days)
          </h3>
          <ul className="space-y-2">
            {insights.upcoming_deadlines.map((deadline, index) => (
              <li
                key={index}
                className="text-sm text-gray-700 bg-yellow-50 p-2 rounded border-l-4 border-yellow-400"
              >
                {deadline}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Key Insights */}
      {insights.key_insights && insights.key_insights.length > 0 && (
        <div className="mb-6">
          <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
            <AlertCircle className="w-4 h-4" />
            Key Insights
          </h3>
          <ul className="space-y-2">
            {insights.key_insights.map((insight, index) => (
              <li key={index} className="text-sm text-gray-700 flex gap-2">
                <span className="text-primary-600">•</span>
                <span>{insight}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Recommendations */}
      {insights.recommendations && insights.recommendations.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
            <CheckCircle className="w-4 h-4" />
            Recommendations
          </h3>
          <ul className="space-y-2">
            {insights.recommendations.map((rec, index) => (
              <li
                key={index}
                className="text-sm text-gray-700 bg-green-50 p-2 rounded flex gap-2"
              >
                <span className="text-green-600">✓</span>
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
