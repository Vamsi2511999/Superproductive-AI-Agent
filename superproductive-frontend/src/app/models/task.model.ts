export interface Task {
  id: string | number;
  title: string;
  source?: string; // email | todo | teams
  sourceRef?: string; // optional reference (subject/sender)
  eta?: string | null; // ISO date string
  priority?: 'High' | 'Medium' | 'Low';
  status?: 'Pending' | 'Done' | 'InProgress';
  extractedFrom?: string; // raw text source snippet
}